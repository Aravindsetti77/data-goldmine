import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_leads():
    # Example: Scraping a niche news or job site
    url = "https://remoteok.com/remote-junior-jobs" 
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    leads = []
    # This logic changes based on the website's HTML
    for job in soup.find_all('tr', class_='job'):
        title = job.find('h2').text.strip() if job.find('h2') else "N/A"
        company = job.find('h3').text.strip() if job.find('h3') else "N/A"
        link = "https://remoteok.com" + job.find('a', class_='preventLink')['href']
        
        leads.append({"Title": title, "Company": company, "Link": link, "Date": datetime.now()})
    
    # Save to CSV
    df = pd.DataFrame(leads)
    df.to_csv("daily_leads.csv", index=False)
    print(f"Saved {len(leads)} leads to daily_leads.csv")

if __name__ == "__main__":
    scrape_leads()