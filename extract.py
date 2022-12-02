# hardcoded
from bs4 import BeautifulSoup
import requests
import urllib3
import numpy as np
import pandas as pd
import re
urllib3.disable_warnings()


def get_doc(url):
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    return doc


def get_number_of_reviews(doc):
    return len(doc.select("div.lister-item"))


def get_review_text(doc, rows):
    arr = []
    for row in range(1, rows + 1):
      curr_item = doc.select(
            f"div.lister > div.lister-list > div:nth-child({row}) > div.review-container > div.lister-item-content > div.content > div.text")
      if len(curr_item) > 0:
          curr_item = curr_item[0]
          curr_item = str(curr_item).split("</div>")[0]
          curr_item = str(curr_item).split("\">")[1]
          curr_item = curr_item.replace('<br/>',"")
          arr.append(curr_item)
      else:
          arr.append("")

    return arr


def get_review_rating(doc, rows):
    arr = []
    for row in range(1, rows + 1):
        curr_item = doc.select(
            f"div.lister > div.lister-list > div:nth-child({row}) > div > div.lister-item-content > div.ipl-ratings-bar > span > span:nth-child(2)")
        if len(curr_item) > 0:
            curr_item = curr_item[0]
            curr_item = str(curr_item).split("</span>")[0]
            curr_item = str(curr_item).split(">")[1]
            arr.append(curr_item)
        else:
            arr.append("0")

    return arr

def get_review_headers(doc, rows):
    arr = []
    for row in range(1, rows + 1):
        curr_item = doc.select(
            f"#main > section > div.lister > div.lister-list > div:nth-child({row}) > div.review-container > div.lister-item-content > a")
        if len(curr_item) > 0:
            curr_item = curr_item[0]
            curr_item = str(curr_item).split("</a>")[0]
            curr_item = str(curr_item).split(">")[1]
            arr.append(curr_item)
        else:
            arr.append("100")
    return arr


urls = [f"https://www.imdb.com/title/tt9114286/reviews?ref_=tt_urv",f"https://www.imdb.com/title/tt9764362/reviews?ref_=tt_urv"
        ,f"https://www.imdb.com/title/tt6443346/reviews?ref_=tt_urv",f"https://www.imdb.com/title/tt10731256/reviews?ref_=tt_urv"
        ,f"https://www.imdb.com/title/tt1596342/reviews?ref_=tt_urv",f"https://www.imdb.com/title/tt9411972/reviews?ref_=tt_urv"
        ,f"https://www.imdb.com/title/tt15474916/reviews?ref_=tt_urv",f"https://www.imdb.com/title/tt14715170/reviews?ref_=tt_urv"
        ,f"https://www.imdb.com/title/tt9288822/reviews?ref_=tt_urv",f"https://www.imdb.com/title/tt10999120/reviews?ref_=tt_urv"]

movies = pd.read_csv("com.csv")

len_url = movies.size
print(len_url)
for i in range(0,100):
    arr = []
    print(movies["title"][i])
    doc = get_doc(movies["title"][i])
    rows = get_number_of_reviews(doc)
    arr.append(get_review_headers(doc,rows))
    arr.append(get_review_text(doc, rows))
    arr.append(get_review_rating(doc, rows))
    nparr = np.asarray(arr)
    df = pd.DataFrame({'header':nparr[0], 'text':nparr[1],'rating':nparr[2]})
    docname = str(i + 1)
    df.to_csv('com'+ docname +'.csv', index=False, na_rep='Unknown')

