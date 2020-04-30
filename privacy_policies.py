from bs4 import BeautifulSoup
import urllib.request as urllib2
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
import os


def write_links():
    url = 'https://caprivacy.github.io/caprivacy/full/'
    file_name = 'privacy_links.txt'
    file = open(file_name, 'w')

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')


    for link in soup.find_all('a'):
        x = link.get('href')
        if x != "":
            file.write(x + '\n')


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def get_text_from_link(link):
    soup = BeautifulSoup(link, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def write_policies_to_files():
    f = open("privacy_links.txt", "r")
    for url in f.readlines():
        try:
            company = re.findall('https://(.*).com', url)
            company2 = re.findall('www.(.*)', company[0])

            if len(company2) > 0:
                company = company2

            fileName = 'privacy_texts/' + company[0] + '.txt'
            file = open(fileName,'w')


            driver = webdriver.Chrome(executable_path='/Users/abbykrishnan/Downloads/chromedriver')
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            file.write(get_text_from_link(html))
        except:
            print("problem with", url)
            continue

def print_exs(key_word):
    for fileName in os.listdir('/Users/abbykrishnan/Documents/Spring 2020/Research/privacy-crawler/privacy_texts'):
        if '.DS_Store' in fileName:
            continue
        file = open('privacy_texts/' + fileName,'r')
        data = file.read().replace('\n', '')

        regex = '[^.]* {term}[^.]*\.'.format(term=key_word)
        results = re.findall(regex, data.lower())

        if len(results) > 0:
            print (fileName, results)
if __name__ == '__main__':
    print_exs("financial incentive")






