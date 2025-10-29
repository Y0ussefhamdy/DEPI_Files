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
company = soup.find_all("a", class_="css-o171kl") 
location = soup.find_all("span", class_="css-16x61xq") 
type = soup.find_all("span", class_="css-uc9rga") 
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


    experience = job_soup.find("span", class_="css-2rozun")
    # find the <ul>
    requirements = job_soup.find("div", class_="css-1lqavbg")
    

    # find all <li> items inside it
    lis = requirements.find_all("li")

    requirements_list.append([li.get_text(strip=True) for li in lis])

    experience_levels.append(experience.get_text(strip=True) if experience else "Not specified")


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
print("Data saved to wuzzuf_scraping.csv")