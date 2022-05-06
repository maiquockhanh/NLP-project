from serpapi import GoogleSearch
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

def searchGG(query, num):
  params = {
      "engine": "google",
      "q": query,
      "google_domain": "google.com",
      "num": num,
      "api_key": 'b490e6c22c280d23132f88cd00598d80440b34c62dff5795eae5c1396525e191'
  }

  client = GoogleSearch(params)
  data = client.get_dict()
  db = [dt['link'] for dt in data['organic_results'] 
        if not ('pdf' in dt['link'] 
                or '.aspx' in dt['link']  
                or 'qcc' in dt['link']
                or 'shtml' in dt['link']
                or 'pdxscholar' in dt['link']
                or 'cgi' in dt['link']
                or 'www1' in dt['link']
        )]

  return pd.DataFrame (db, columns = ['link'])

def getContents(link_list):
  content_list = []
  for link in link_list:
    print(link)
    try:
      html = requests.get(link)
      text_html = text_from_html(html.text)
    #   text = ''
    #   for word in word_tokenize(text_html):
    #     if(word != "'s" or word != '.'):
    #       text += ' '
    #     text += word
        
      content_list.append(text_html)
    except:
      content_list.append('')

  return content_list

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)
  