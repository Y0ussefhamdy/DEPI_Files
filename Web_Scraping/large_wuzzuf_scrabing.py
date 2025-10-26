from bs4 import BeautifulSoup as bs
import requests
import csv
import time


# SETTINGS

base_url = "https://wuzzuf.net/a/Engineering-Construction-Civil-Architecture-Jobs-in-Egypt?start="
pages_to_scrape = 10  # you can change this (each page ≈ 15–20 jobs)
delay_seconds = 3  # wait between requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/125.0.0.0 Safari/537.36"
}



# STORAGE LISTS

job_titles = []
company_names = []
locations = []
posting_dates = []
experience_levels = []
requirements_list = []
links = []



# SCRAPE MULTIPLE PAGES

for page in range(pages_to_scrape):
    url = f"{base_url}{page}"
    print(f" Scraping page {page + 1} → {url}")
    response = requests.get(url, headers=headers)
    soup = bs(response.content, "html.parser")

    # Find all job cards
    job_cards = soup.find_all("div", class_="css-1gatmva")
    print(f"   Found {len(job_cards)} jobs on this page")

    for card in job_cards:
        title_tag = card.find("h2")
        company_tag = card.find("a", class_="css-17s97q8") or card.find("a", class_="css-1rd3vky")
        location_tag = card.find("span", class_="css-5wys0k") or card.find("span", class_="css-1t5f0fr")
        post_tag = card.find("div", class_="css-4c4ojb")

        if title_tag:
            job_titles.append(title_tag.text.strip())
            link = title_tag.find("a")["href"]
            if link.startswith("/"):
                link = "https://wuzzuf.net" + link
            links.append(link)
        else:
            job_titles.append("Not found")
            links.append("")

        company_names.append(company_tag.text.strip() if company_tag else "Not specified")
        locations.append(location_tag.text.strip() if location_tag else "Not specified")
        posting_dates.append(post_tag.text.strip() if post_tag else "Not specified")

    time.sleep(delay_seconds)



# SCRAPE DETAILS FROM EACH JOB PAGE

print("\n Scraping individual job pages for experience & requirements...\n")

for i, link in enumerate(links):
    print(f"   ({i+1}/{len(links)}) {link}")
    if not link:
        experience_levels.append("Not specified")
        requirements_list.append("Not specified")
        continue

    try:
        job_response = requests.get(link, headers=headers)
        job_soup = bs(job_response.content, "html.parser")

        # Experience section
        exp = job_soup.find("span", string=lambda s: s and "Experience Needed" in s)
        experience_levels.append(exp.text.strip() if exp else "Not specified")

        # Requirements section
        reqs = job_soup.find("div", {"class": "css-1t5f0fr"})
        if reqs:
            req_items = reqs.find_all("li")
            requirements_text = " | ".join([item.text.strip() for item in req_items])
        else:
            requirements_text = "Not specified"
        requirements_list.append(requirements_text)

        time.sleep(delay_seconds)
    except Exception as e:
        print(f"Error scraping {link}: {e}")
        experience_levels.append("Error")
        requirements_list.append("Error")



# SAVE TO CSV

file_name = "wuzzuf_engineering_jobs.csv"
with open(file_name, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Job Title", "Company Name", "Location",
        "Experience Level", "Posting Date", "Requirements", "Link"
    ])
    for i in range(len(job_titles)):
        writer.writerow([
            job_titles[i], company_names[i], locations[i],
            experience_levels[i], posting_dates[i],
            requirements_list[i], links[i]
        ])

print(f"\nDone! Scraped {len(job_titles)} job records.")
print(f"Data saved to: {file_name}")
