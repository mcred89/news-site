from  newspaper import Article

url='https://www.reuters.com/article/us-venezuela-politics/trump-says-u-s-military-intervention-in-venezuela-an-option-russia-objects-idUSKCN1PS0DK'

article = Article(url)

article.download()

article.parse()

article.nlp()

print(f'SUMMARY: {article.summary}')