from  newspaper import Article

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

