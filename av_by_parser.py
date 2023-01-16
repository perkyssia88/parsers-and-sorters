import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv
import json


def get_parse(iterations):
    data = []
    for i in range(iterations):
        url = f"https://cars.av.by/filter?brands[0][brand]=1039&brands[0][model]=2281&page={i + 1}"
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, "lxml")
        cars = soup.find_all("div", class_="listing-item")
        for car in cars:
            link = "https://cars.av.by" + car.find("a", class_="listing-item__link").get("href")
            model = car.find("span", class_="link-text").text
            performance = car.find(
                "div", class_="listing-item__params").text.replace(u'\xa0', ' ').replace(u'\u2009', '')
            price_rub = car.find("div", class_="listing-item__prices").find(
                "div", class_="listing-item__price").text.replace(u'\xa0', ' ').replace(u'\u2009', '')
            price_usd = car.find("div", class_="listing-item__prices").find(
                "div", class_="listing-item__priceusd").text.replace(u'\xa0', ' ').replace(u'\u2009', '')
            try:
                description = car.find("div", class_="listing-item__message").text.replace("\n", " ")
            except:
                description = "-"
            city = car.find("div", class_="listing-item__info").find("div", class_="listing-item__location").text
            date = car.find("div", class_="listing-item__info").find("div", class_="listing-item__date").text

            data.append([link, model, performance, price_rub, price_usd, description, city, date])

            """По сортировке, не решена проблема неверного отображения четырехзначных
            цен относительно остальной таблицы.
            Уточнить этот вопрос у Романа.
            """
    sort_choice = input("Для сортировки по цене в BYN нажмите - 1, "
                        "в USD нажмите - 2: ")

    sort_reverse = input("Для сортировки по возрастанию нажмите - 1, "
                         "по убыванию - 2: ")
    # сортируем экземпляр класса list - data
    try:
        sort_choice = int(sort_choice)
        sort_reverse = int(sort_reverse)
    except ValueError:
        print("Введены неверные значения")
    else:
        if 0 < sort_choice <= 2 and 0 < sort_reverse <= 2:
            sort_choice += 2
            sort_reverse -= 1
        else:
            print("Введены неверные значения, будет произведена "
                  "сортировка по цене в USD по возрастанию")
            sort_choice = 4
            sort_reverse = 0

    data.sort(key=lambda i: i[sort_choice], reverse=sort_reverse)
    return data


ua = UserAgent()
headers = {'User-Agent': ua.chrome}
try:
    iterations = int(input("Со скольких страниц собрать информацию? "))
except ValueError:
    iterations = 5
    print("Введено неверное значение, информация будет собрана с 5-ти страниц.")
parse = get_parse(iterations)

"""
Блок сохранения csv и json файлов, по сути готов
"""
# save csv
with open("av.csv", "w", encoding="utf-8", newline="") as avc:
    av_writer = csv.writer(avc, delimiter=";")
    for row in parse:
        av_writer.writerow(row)

# save json
js_data = dict(zip([str(_) for _ in range(len(parse))], [_ for _ in parse]))
with open("av.json", "w", encoding="utf-8") as avj:
    json.dump(js_data, avj, ensure_ascii=False)

# # проверка количества объектов для записи csv и json(должны быть одинаковыми)
# print(len(parse))
# print(len(parse))
