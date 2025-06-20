import requests
from bs4 import BeautifulSoup

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

url = 'https://habr.com/ru/articles/'


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', class_='tm-articles-list__item')

        for article in articles:
                title_elem = article.find('h2', class_='tm-title')
                if not title_elem:
                        continue
                title = title_elem.text.strip()
                link_elem = title_elem.find('a', class_='tm-title__link')
                if not link_elem:
                        continue
                link = url
                time_elem = article.find('time')
                date = time_elem['datetime'] if time_elem else 'No date'
                preview_text = []
                preview_elem = article.find('div', class_='article-formatted-body')
                if preview_elem:
                        preview_text.append(preview_elem.text.strip().lower())
                hubs = article.find_all('a', class_='tm-article-snippet__hubs-item-link')
                preview_text.extend([hub.text.strip().lower() for hub in hubs])
                full_text = ' '.join(preview_text)
                if any(keyword.lower() in full_text for keyword in KEYWORDS):
                        print(f"{date} – {title} – {link}")

except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
except Exception as e:
        print(f"Произошла ошибка: {e}")
