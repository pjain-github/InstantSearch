import requests
from bs4 import BeautifulSoup
from datetime import datetime

class WebScrapper:

    def __init__(self):
        pass

    def get_text(self, url):
        response = requests.get(url)

        text = ''

        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.content, 'html.parser')

            # Getting title of the page
            title = soup.title.string if soup.title else "No title found"

            text = title + '\n'

            # Getting text from webpage
            try:
                text_content = [p.get_text(strip=True) for p in soup.find_all('p')]
                for text_part in text_content:
                    text = text + text_part + '\n'

            except Exception as e:
                print("Failed to get text")
                # Extract all the text from the webpage
                text = text + soup.get_text()

        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

        metadata = {
            'SOURCE': url,  # You might want to add the file path as the source
            'DATE': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format the date as per your preference
        }

        return text, metadata