import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_leads():
    # RSS feeds are much harder to block than HTML pages
    url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
    
    try:
        response = requests.get(url, timeout=15)
        # We use 'xml' parser for RSS feeds
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        leads = []
        for item in items:
            title = item.find('title').get_text() if item.find('title') else "N/A"
            link = item.find('link').get_text() if item.find('link') else "N/A"
            pub_date = item.find('pubDate').get_text() if item.find('pubDate') else "N/A"
            
            leads.append({
                "Title": title,
                "Link": link,
                "Date_Posted": pub_date,
                "Scraped_At": datetime.now().strftime("%Y-%m-%d")
            })

        if leads:
            df = pd.DataFrame(leads)
            df.to_csv("daily_leads.csv", index=False)
            print(f"Success! Found {len(leads)} leads via RSS.")
        else:
            print("RSS feed was empty.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_leads()
