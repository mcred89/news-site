from bs4 import BeautifulSoup
import requests
from utils import get_summary

print('==========================================================')

site = 'https://www.reuters.com'

source = requests.get(site).text

soup = BeautifulSoup(source, 'lxml')

first_story_container = soup.find('h2', class_="story-title")
first_story = first_story_container.a

print(first_story.text)
print(get_summary(site + first_story['href']))
print('==========================================================')

second_story_container = soup.find('div', class_="news-headline-list")
second_story_link = second_story_container.find('a')
second_story_title = second_story_container.find('h3', class_="story-title")

print(second_story_title.text.strip())
print(get_summary(site + second_story_link['href']))
print('==========================================================')