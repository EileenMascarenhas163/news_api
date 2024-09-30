import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

def scrape_google_news_technology():
    url = "https://news.google.com/topics/CAAqBwgKMAp7BwiwwMDqAw?hl=en-US&gl=US&ceid=US:en"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    for item in soup.find_all('article'):
        headline = item.find('h3')
        if headline:
            link = headline.find('a')['href']
            full_link = f"https://news.google.com{link[1:]}"
            articles.append({
                "title": headline.get_text(),
                "link": full_link
            })
    
    return articles

@app.get("/news/technology")
def get_technology_news():
    articles = scrape_google_news_technology()
    return articles

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
