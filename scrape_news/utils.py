from  newspaper import Article

def get_summary(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    return article.summary

