import requests
from bs4 import BeautifulSoup


KEYWORDS = ['дизайн', 'фото', 'web', 'python']


URL = 'https://habr.com/ru/articles/'

def fetch_articles(url):
    try:
      
        response = requests.get(url)
        response.raise_for_status()  
        response.encoding = 'utf-8'  
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []


        for article in soup.find_all('article'):
            title_tag = article.find('h2')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag.find('a')['href']
                date_tag = article.find('time')
                date = date_tag['title'] if date_tag else 'Не указана'
                
            
                preview_text = article.find('div', class_='post-preview__text').get_text(strip=True) if article.find('div', class_='post-preview__text') else ''
                
                if any(keyword.lower() in (title + preview_text).lower() for keyword in KEYWORDS):
                    articles.append((date, title, link))
        
        return articles
    except requests.RequestException as e:
        print(f"Ошибка при получении статей: {e}")
        return []

def main():
    articles = fetch_articles(URL)
    

    print("Подходящие статьи:")
    for date, title, link in articles:
        print(f"{date} – {title} – {link}")

if __name__ == "__main__":
    main()
