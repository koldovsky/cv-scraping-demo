import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL of the job vacancies page
url = "https://jobs.dou.ua/vacancies/?category=Marketing"

# Custom headers with a common browser user-agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Create a session to maintain cookies and headers across requests
session = requests.Session()
session.headers.update(headers)

try:
    # Send a GET request using the session
    response = session.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all job listings
        job_listings = soup.find_all('li', class_='l-vacancy')

        # Prepare lists to store the extracted data
        job_titles = []
        companies = []
        locations = []
        links = []

        for job in job_listings:
            # Extract job title
            title_tag = job.find('a', class_='vt')
            title = title_tag.text.strip() if title_tag else "Not specified"
            job_titles.append(title)

            # Extract company name
            company_tag = job.find('a', class_='company')
            company = company_tag.text.strip() if company_tag else "Not specified"
            companies.append(company)

            # Extract location
            location_tag = job.find('span', class_='cities')
            location = location_tag.text.strip() if location_tag else "Not specified"
            locations.append(location)

            # Extract job link
            link = title_tag['href'] if title_tag and title_tag.has_attr('href') else "Not specified"
            links.append(link)

        # Create a DataFrame
        jobs_df = pd.DataFrame({
            'Job Title': job_titles,
            'Company': companies,
            'Location': locations,
            'Link': links
        })

        # Save to a CSV file
        jobs_df.to_csv('marketing_jobs.csv', index=False)
        print("Data saved to marketing_jobs.csv")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")
