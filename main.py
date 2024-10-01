import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

def scrape_google_news_technology():
    # URL of the technology section of Google News
    url = "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen"
    
    # Sending a GET request to the URL
    response = requests.get(url)
    
    # Checking if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve news, status code: {response.status_code}")
        return []
    
    # Parsing the content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # List to hold the extracted articles
    articles = []
    
    # Loop through all article links in the technology section
    for item in soup.find_all('a', attrs={'class': 'DY5T1d'}):
        # Extracting the title and the link
        title = item.get_text()
        link = item['href']
        
        # The link is relative, so we need to append the base URL
        full_link = f"https://news.google.com{link[1:]}"
        
        # Adding the title and link to the articles list
        articles.append({"title": title, "link": full_link})
    
    return articles

@app.get("/")
def read_root():
    # Calling the scrape function to get the articles
    articles = scrape_google_news_technology()
    
    # Return the articles as JSON response
    return {"articles": articles}
