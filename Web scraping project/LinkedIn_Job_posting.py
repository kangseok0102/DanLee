from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import time

browser = webdriver.Chrome()
browser.maximize_window()

def selenium_job_search():
    url = "https://www.linkedin.com/jobs/jobs-in-union-ky?trk=homepage-basic_intent-module-jobs&position=1&pageNum=0"
    browser.get(url)

    job_type = browser.find_element_by_xpath("/html/body/header/nav/section/section[2]/form/section[1]/input")
    job_location = browser.find_element_by_xpath("/html/body/header/nav/section/section[2]/form/section[2]/input")
    job_type.send_keys("software engineer")
    job_location.clear()
    job_location.send_keys("United States", Keys.ENTER)

def requests_data_collect():
    selenium_job_search()
    interval = 2
    more_jobs = browser.find_element_by_xpath("//*[@id='main-content']/div/section/button")
    prev_height = browser.execute_script("return document.body.scrollHeight")
    count = 0
    while True:
        count+=1
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(interval)
        curr_height = browser.execute_script("return document.body.scrollHeight")
        if prev_height == curr_height and more_jobs:
            more_jobs.click()
        if count == 70:
            break
        prev_height = curr_height

    soup = BeautifulSoup(browser.page_source, "lxml")
    all_data = soup.find_all("div", attrs={"class": "result-card__contents job-result-card__contents"})

    with open('Software Engineer Seeker Company List.csv', 'w', encoding = 'utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Job Title', 'Company', 'Location', 'Job Post'])

        for jobs in all_data:
            job_title = jobs.find("h3", attrs={"class": "result-card__title job-result-card__title"}).get_text().split('\t')
            company_name = jobs.find("h4", attrs={"class": "result-card__subtitle job-result-card__subtitle"}).get_text().split('\t')
            company_loc = jobs.find("span", attrs={"class": "job-result-card__location"}).get_text().split('\t')
            job_posted_date = jobs.find("div", attrs={"class": "result-card__meta job-result-card__meta"}).find("time").get_text().split('\t')
            data = job_title, company_name, company_loc, job_posted_date
            writer.writerow(data)

