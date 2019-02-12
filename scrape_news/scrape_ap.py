from bs4 import BeautifulSoup
import requests
from utils import get_summary

print('==========================================================')

site = 'https://www.apnews.com'

source = requests.get(site).text

soup = BeautifulSoup(source, 'lxml')

first_story = soup.find('a', class_="headline")

print(first_story.text)
print(get_summary(site + first_story['href']))
print('==========================================================')

second_story_container = soup.find('div', class_="RelatedStory")
second_story_link = second_story_container.a
second_story_title = second_story_container.find('div', class_="headline")

print(second_story_title.text)
print(get_summary(site + second_story_link['href']))
print('==========================================================')