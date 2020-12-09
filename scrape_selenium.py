from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime, timedelta
from selenium import webdriver

driver = webdriver.Chrome()


csv_file = open("indeed.csv", 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['job_title', 'company_name', 'location', 'salary', 'date_of_post', 'summary', 'job_link'])


position = "web developer"
position = position.replace(" ","+")

location = "bangalore"
location = location.replace(" ","+")



def extraction(section):
	company = section.a

	try:
		job_title = company['title']
	except Exception as e:
		job_title = section.h2.text

	job_link = company['href']
	job_link = "https://in.indeed.com" + job_link

	company_name = section.find('span', class_="company")
	company_name = company_name.text
	company_name = company_name.strip()

	try:
		salary = section.find('span', class_="salaryText").text
		# salary = salary.split(" ")[0]
		salary = salary.replace("₹",'INR ')
		# salary = salary .replace(',','')
		salary = salary.strip()
	except Exception as e:
		salary = None
	

	try:
		date_of_post = section.find('span', class_="date").text
		date_of_post = int(date_of_post[:1])
		date_of_post = datetime.today() - timedelta(days=date_of_post)
		date_of_post = date_of_post.date()
	except Exception as e:
		date_of_post = datetime.today().date()

	try:
		location = section.find('div', class_="location")
		location = location.text
	except Exception as e:
		location = None
	

	try:
		summary = section.find('div', class_='summary')
		summary = summary.li.text
	except Exception as e:
		summary = None

	return job_title, company_name, location, salary, date_of_post, summary, job_link




def get_url(i):
		url = f"https://in.indeed.com/jobs?q={position}&l={location}&start={i}"
		return url


for i in range(0, 990, 10):

	driver.get(get_url(i))

	soup = BeautifulSoup(driver.page_source, 'lxml')
	# print(soup.prettify())


	for section in soup.find_all('div', class_="jobsearch-SerpJobCard"):
		# print(section.prettify())

		print(extraction(section))

		print()

		csv_writer.writerow(extraction(section))


	print("Page: ",(i/10) + 1)

csv_file.close()










