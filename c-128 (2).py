from wsgiref import headers
from attr import attrs
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser = webdriver.Chrome("C:/Users/amber/Desktop/C-127/chromedriver.exe")
browser.get(START_URL)
time.sleep(10)
def scrape():
    headers = ["star_name","distance","mass","radius","hyperlink","star_type","star_radius","orbital_radius","orbital_period","eccentricity"]
    stars_data = []
    for i in range(0, 428):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs={"class", "exostars"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag=li_tags[0]
            temp_list.append("https://exostars.nasa.gov"+hyperlink_li_tag.find_all("a",href=True)[0]["href"])
            stars_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    with open("scrapper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(stars_data)

def scrape_more_data(hyperlink):
    page=requests.get(hyperlink)
    soup=BeautifulSoup(page.content,"html.parser")
    for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
        td_tags=tr_tag.find_all("td")
        temp_list=[]
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
            except:
                temp_list.append("")
        new_stars_data.append(temp_list)
    pass
scrape()
for data in stars_data:
    scrape_more_data(data[5])

