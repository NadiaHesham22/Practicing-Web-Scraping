import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

result=requests.get("https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&q=python")

job_title_list=[]

company_name_list=[]

location_name_list=[]

job_skill_list=[]

links=[]

salary=[]

src=result.content
#print(src)

soup=BeautifulSoup(src,"lxml")
#print(soup)

job_titles=soup.find_all("h2",{"class":"css-m604qf"})

company_names=soup.find_all("a",{"class":"css-17s97q8"})

location_names=soup.find_all("span",{"class":"css-5wys0k"})

job_skills=soup.find_all("div",{"class":"css-y4udm8"})


for i in range(len(job_titles)):
    job_title_list.append(job_titles[i].text)
    links.append(job_titles[i].find("a").attrs['href'])
    company_name_list.append(company_names[i].text)
    location_name_list.append(location_names[i].text)
    job_skill_list.append(job_skills[i].text)

    for link in links:
        result=requests.get(link)
        src=result.content
        soup=BeautifulSoup(src,"lxml")
        salaries=soup.find("div",{"class":"matching-requirement-icon-container","data-toggle":"tooltip","data-placement":"top"})
        salary.append(salaries.text.strip())


file_list=[job_title_list,company_name_list,location_name_list,job_skill_list,salary]
exported=zip_longest(*file_list)

with open("C:/Users/Dell/Documents/jobset.csv","w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["job title","company name","location","skills","salary"])
    wr.writerows(exported)


print(salary)