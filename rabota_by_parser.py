import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
headers = {"User-Agent": ua.chrome}

url = "https://rabota.by/search/vacancy?text=python&from=suggest_post&area=1002"
req = requests.get(url, headers=headers)

soup = BeautifulSoup(req.text, "lxml")

vacancy = soup.find_all("div", class_="serp-item")
data = []

for vac in vacancy:
    print(vac.text)
