import requests
from bs4 import BeautifulSoup

# Declare URL address for Webtoon
url = "https://comic.naver.com/webtoon/list.nhn?titleId=675554"
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

# Get Webtoon title and assigned link information
def cartoon_title_link():
    cartoons = soup.find_all("td", attrs={"class":"title"})
    rates = soup.find_all("div", attrs={"class":"rating_type"})
    for line in range(len(cartoons)):
        cartoons_list = cartoons[line].a.get_text()
        link_list = cartoons[line].a["href"]
        rate_list = rates[line].find("strong").get_text()
        print("웹툰정보:", cartoons_list,'\n', "Link:""https://comic.naver.com/" + link_list, '\n',
              "평점:", rate_list,"점")
cartoon_title_link()
