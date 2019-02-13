import newspaper

articles_per_site = 2

url='https://www.reuters.com/article/us-venezuela-politics/trump-says-u-s-military-intervention-in-venezuela-an-option-russia-objects-idUSKCN1PS0DK'

article = newspaper.Article(url)

article.download()

article.parse()

article.nlp()

#print(f'SUMMARY: {article.summary}')

news_sources = ['https://www.reuters.com', 'https://www.apnews.com/']

for source in news_sources:
    site = newspaper.build(source, memoize_articles=False)
    articles = site.articles
    print(articles[0].url)