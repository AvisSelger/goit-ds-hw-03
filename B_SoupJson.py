import requests
from bs4 import BeautifulSoup
import json

def fetch_quotes():
    base_url = "http://quotes.toscrape.com"
    page_url = "/page/1/"
    authors_info = {}
    quotes = []

    while page_url:
        response = requests.get(base_url + page_url)
        soup = BeautifulSoup(response.text, "html.parser")

        for quote_block in soup.select('.quote'):
            text = quote_block.find(class_='text').get_text(strip=True)
            author = quote_block.find(class_='author').get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote_block.find_all('a', class_='tag')]
            
            quotes.append({
                "tags": tags,
                "author": author,
                "quote": text
            })

            if author not in authors_info:
                author_page_link = quote_block.find('a')['href']
                author_response = requests.get(base_url + author_page_link)
                author_soup = BeautifulSoup(author_response.text, "html.parser")
                
                fullname = author_soup.find(class_='author-title').get_text(strip=True)
                born_date = author_soup.find(class_='author-born-date').get_text(strip=True)
                born_location = author_soup.find(class_='author-born-location').get_text(strip=True)
                description = author_soup.find(class_='author-description').get_text(strip=True).replace('\n', ' ').strip()
                
                authors_info[author] = {
                    "fullname": fullname,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description
                }

        next_btn = soup.select_one('.pager .next > a')
        page_url = next_btn['href'] if next_btn else None

    return quotes, list(authors_info.values())

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    quotes, authors = fetch_quotes()
    save_to_json(quotes, 'quotes.json')
    save_to_json(authors, 'authors.json')

if __name__ == "__main__":
    main()
