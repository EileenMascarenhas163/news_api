import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

def scrape_google_news_technology():
    # URL of the technology section of Google News
    url = "https://news.google.com/topics/CAAqKQgKIiNDQkFTRkFvTEwyY3ZNVEl3ZVhKMk5tZ1NCV1Z1TFVkQ0tBQVAB?hl=en-IN&gl=IN&ceid=IN%3Aen"
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
    for item in soup.find_all('a', attrs={'class': 'JtKRv'}):
        # Extracting the title and the link
        title = item.get_text()
        link = item['href']
        
        # The link is relative, so we need to append the base URL
        full_link = f"https://news.google.com{link[1:]}"
        image_tag = item.find_previous('img',attrs={'class':'Quavad vwBmvb'})  # Adjust to the correct  # if it was inside the structure item.find
        image_url = image_tag['src'] if image_tag else 'No image available' 
        full_link_image = f"https://news.google.com/{image_url[1:]}"
        # Adding the title and link to the articles list

        time = item.find_next('time',attrs={'class':'hvbAAd'})
        time_text = time.get_text()

        articles.append({"title": title, "link": full_link , "image_url" : full_link_image,'time':time_text})
    
    return articles

@app.get("/")
def read_root():
    # Calling the scrape function to get the articles
    articles = scrape_google_news_technology()
    
    # Return the articles as JSON response
    return {"articles": articles}
