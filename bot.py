import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_leads():
    # Using a slightly different target that is more stable for scrapers
    url = "https://remoteok.com/remote-junior-jobs" 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    leads = []
    # Targeted search for job rows
    job_rows = soup.find_all('tr', class_='job')
    
    for job in job_rows:
        try:
            # Safer way to find elements
            title_elem = job.find('h2')
            company_elem = job.find('h3')
            link_elem = job.find('a', href=True) # Finds any 'a' tag with an href
            
            if title_elem and company_elem and link_elem:
                title = title_elem.get_text(strip=True)
                company = company_elem.get_text(strip=True)
                # Ensure we get the full URL
                link = link_elem['href']
                if not link.startswith('http'):
                    link = "https://remoteok.com" + link
                
                leads.append({
                    "Title": title, 
                    "Company": company, 
                    "Link": link, 
                    "Date": datetime.now().strftime("%Y-%m-%d")
                })
        except Exception as e:
            print(f"Skipping a row due to error: {e}")
            continue
    
    if leads:
        df = pd.DataFrame(leads)
        df.to_csv("daily_leads.csv", index=False)
        print(f"Success! Saved {len(leads)} leads.")
    else:
        print("No leads found. Website structure might have changed.")

if __name__ == "__main__":
    scrape_leads()
