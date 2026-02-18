import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_leads():
    # Switching to a more stable, scraper-friendly target
    url = "https://weworkremotely.com/categories/remote-programming-jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print("Access denied by the website.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        leads = []

        # This site uses standard list items for jobs
        jobs = soup.find_all('li', class_=['feature', 'regular'])

        for job in jobs:
            try:
                title_elem = job.find('span', class_='title')
                company_elem = job.find('span', class_='company')
                link_tag = job.find('a', href=True)

                if title_elem and company_elem and link_tag:
                    # Clean the strings and build the full URL
                    full_link = link_tag['href']
                    if not full_link.startswith('http'):
                        full_link = "https://weworkremotely.com" + full_link
                    
                    leads.append({
                        "Title": title_elem.get_text(strip=True),
                        "Company": company_elem.get_text(strip=True),
                        "Link": full_link,
                        "Date": datetime.now().strftime("%Y-%m-%d")
                    })
            except Exception:
                continue

        if leads:
            df = pd.DataFrame(leads)
            df.to_csv("daily_leads.csv", index=False)
            print(f"Success! Found {len(leads)} leads.")
        else:
            print("No leads found. Site structure might have changed.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_leads()
