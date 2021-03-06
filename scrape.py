from bs4 import BeautifulSoup
import requests
from  newspaper import Article
import boto3

def get_summary(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    return article.summary

def make_news_summary(outputs, site, link, index, headline):
    outputs['news'][site][index]['headline'] = headline
    outputs['news'][site][index]['link'] = link
    outputs['news'][site][index]['summary'] = get_summary(link)
    return outputs


def get_ap(outputs):
    outputs['news']['AP'] = [{}, {}]
    url = 'https://www.apnews.com'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    first_story = soup.find('a', class_="headline")
    outputs = make_news_summary(
        outputs, 'AP', url + first_story['href'],
        0, first_story.text)

    second_story_container = soup.find('div', class_="RelatedStory")
    second_story_link = second_story_container.a
    second_story_title = second_story_container.find(attrs={"data-key": "related-story-headline"})
    outputs = make_news_summary(
        outputs, 'AP', url + second_story_link['href'],
        1, second_story_title.text)

    return outputs

def get_reuters(outputs):
    outputs['news']['Reuters'] = [{}, {}]
    url = 'https://www.reuters.com'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    first_story_container = soup.find('section', id="topStory")
    first_story = first_story_container.find('h2', class_="story-title")
    outputs = make_news_summary(
        outputs, 'Reuters', url + first_story.a['href'],
        0, first_story.text)

    second_story_container = soup.find('div', class_="news-headline-list")
    second_story_link = second_story_container.find('a')
    second_story_title = second_story_container.find('h3', class_="story-title")
    outputs = make_news_summary(
        outputs, 'Reuters', url + second_story_link['href'],
        1, second_story_title.text.strip())

    return outputs

def news_run(outputs):
    outputs['news'] = {}
    outputs = get_ap(outputs)
    outputs = get_reuters(outputs)
    return outputs

def supreme_court_run(outputs):
    url = 'https://www.supremecourt.gov/'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    count = 0

    for day in soup.find_all(id='opinionsbyday'):
        outputs.append({})
        date = day.find('span', class_="soday").text
        outputs[count][date] = []
        names = 0
        for ruling in day.find_all('div', class_="casenamerow"):
            outputs[count][date].append({})
            outputs[count][date][names]['case'] = ruling.span.text
            names += 1
        summaries = 0
        for summary in day.find_all('div', class_="casedetail"):
            outputs[count][date][summaries]['summary'] = summary.span.text
            summaries += 1
        opinions = 0
        for opinion in day.find_all('a', target="_blank"):
            link = url + opinion['href']
            outputs[count][date][opinions]['link'] = link
            opinions += 1
        count += 1
        if count == 3:
            break
    return outputs

def congress_run(outputs):
    url = 'https://www.congress.gov/search?pageSize=25&pageSort=dateOfIntroduction:desc&q={%22source%22:%22legislation%22,%22bill-status%22:%22passed-one%22,%22type%22:%22bills%22}'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    count = 0

    for bill in soup.find_all('li', class_='expanded'):
        outputs.append({})
        heading = bill.find('span', class_="result-heading")
        link = heading.a['href']
        outputs[count]['link'] = link
        title = bill.find('span', class_="result-title").text
        outputs[count]['title'] = title
        bill_source = requests.get(link).text
        bill_soup = BeautifulSoup(bill_source, 'lxml')
        summary_section = bill_soup.find('div', id="bill-summary")
        if not summary_section:
            outputs[count]['summary'] = 'No summary available'
        else:
            summary = []
            for summary_line in summary_section.find_all('p'):
                if not summary_line.a:
                    summary.append(summary_line.text)
            summary = ' '.join(summary)
            if summary == '':
                outputs[count]['summary'] = 'No summary available'
            else:
                outputs[count]['summary'] = summary
        count += 1
    return outputs

def scrape_all():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('news-site')

    new_outputs = {}
    new_outputs = news_run(new_outputs)
    table.put_item(
        Item={'page': 'news',
              'content': new_outputs})

    sp_outputs = []
    sp_outputs = supreme_court_run(sp_outputs)
    table.put_item(
        Item={'page': 'supreme_court',
              'content': sp_outputs})

    congress_outputs = []
    congress_outputs = congress_run(congress_outputs)
    table.put_item(
        Item={'page': 'congress',
              'content': congress_outputs})  

if __name__ == "__main__":
    scrape_all()