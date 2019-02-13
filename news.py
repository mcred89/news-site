from bs4 import BeautifulSoup
import requests
from utils import make_news_summary


def get_ap(outputs):
    outputs['news']['ap'] = [{}, {}]
    url = 'https://www.apnews.com'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    first_story = soup.find('a', class_="headline")
    outputs = make_news_summary(
        outputs, 'ap', url + first_story['href'],
        0, first_story.text)

    second_story_container = soup.find('div', class_="RelatedStory")
    second_story_link = second_story_container.a
    second_story_title = second_story_container.find('div', class_="headline")
    outputs = make_news_summary(
        outputs, 'ap', url + second_story_link['href'],
        1, second_story_title.text)

    return outputs

def get_reuters(outputs):
    outputs['news']['reuters'] = [{}, {}]
    url = 'https://www.reuters.com'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    first_story_container = soup.find('section', id="topStory")
    first_story = first_story_container.find('h2', class_="story-title")
    print(url + first_story.a['href'])
    outputs = make_news_summary(
        outputs, 'reuters', url + first_story.a['href'],
        0, first_story.text)

    second_story_container = soup.find('div', class_="news-headline-list")
    second_story_link = second_story_container.find('a')
    second_story_title = second_story_container.find('h3', class_="story-title")
    outputs = make_news_summary(
        outputs, 'reuters', url + second_story_link['href'],
        1, second_story_title.text.strip())

    return outputs

def run(outputs):
    outputs['news'] = {}
    outputs = get_ap(outputs)
    outputs = get_reuters(outputs)
    return outputs