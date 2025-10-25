from bs4 import BeautifulSoup as bs
import requests 
import csv
import time


url = 'https://wuzzuf.net/a/Engineering-Construction-Civil-Architecture-Jobs-in-Egypt?ref=browse-jobs'
response = requests.get(url)
soup = bs(response.content, 'html.parser')

time.sleep(3)

jop_titles = []
company_names = []
locations = []
job_types = []
experience_levels = []
posting_dates = [] 
requirements_list = []
links = []  

title = soup.find_all("h2", class_="css-193uk2c") 
company = soup.find_all("a", class_="css-ipsyv7") 
location = soup.find_all("span", class_="css-16x61xq") 
type = soup.find_all("span", class_="eoyjyou0") 
posted_in = soup.find_all("div", class_="css-eg55jf")

for details in range(len(title)):
    jop_titles.append(title[details].text.strip())
    company_names.append(company[details].text.strip())
    locations.append(location[details].text.strip())
    job_types.append(type[details].text.strip())
    posting_dates.append(posted_in[details].text.strip())
    links.append(title[details].find('a')['href'])

for link in links:
    job_response = requests.get(link)
    job_soup = bs(job_response.content, 'html.parser')


    exp = job_soup.find("span", {"class": "css-47jx3m"})
    experience_levels.append(exp.text.strip() if exp else "Not specified")

    reqs = job_soup.find("div", {"class": "css-1t5f0fr"}) 
    if reqs:
        req_items = reqs.find_all("li")
        requirements_text = " | ".join([item.text.strip() for item in req_items])
    else:
        requirements_text = "Not specified"
    requirements_list.append(requirements_text)

    time.sleep(2)


with open('wuzzuf_scraping.csv','w') as file:
    writer = csv.writer(file)
    writer.writerow([
        'Job Title', 'Company Name', 'Location', 'Job Type',
        'Experience Level', 'Posting Date', 'Requirements', 'Link'
    ])
    for i in range(len(jop_titles)):
        writer.writerow([
            jop_titles[i], company_names[i], locations[i],
            job_types[i], experience_levels[i], posting_dates[i],
            requirements_list[i], links[i]
        ])
print("Data saved to wuzzuf_engineering_jobs.csv")