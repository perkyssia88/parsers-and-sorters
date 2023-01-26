import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import csv
import time


async def get_page(pages_num):
    async with ClientSession() as session:
        url = f"https://cars.av.by/filter?brands[0][brand]=1039&brands[0][model]=2281&page={pages_num}"
        ua = UserAgent()
        headers = {'User-Agent': ua.chrome}
        async with session.get(url=url, headers=headers) as response:
            text_response = await response.text()
            soup = BeautifulSoup(text_response, "lxml")
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


async def main(pages_num):
    tasks = []
    for i in range(pages_num):
        tasks.append(asyncio.create_task(get_page(i + 1)))

    for task in tasks:
        await task


def get_pages_num():
    while True:
        try:
            pages_num = int(input("Введите количество обрабатываемых страниц: "))
            if pages_num > 20:
                pages_num = 20
            break
        except ValueError:
            print("Введено не числовое значение, попробуйте еще раз")
    return pages_num


def sort_data(data):
    """
    По сортировке, не решена проблема неверного отображения четырехзначных
    цен относительно остальной таблицы.
    Уточнить этот вопрос у Романа.
    """
    while True:
        # sort_choice = input("Для сортировки по цене в BYN нажмите - 1, "
        #                     "в USD нажмите - 2: ")
        # sort_reverse = input("Для сортировки по возрастанию нажмите - 1, "
        #                      "по убыванию - 2: ")
        # для тестовой части оставлю фиксированные значения
        sort_choice = 2
        sort_reverse = 1
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
            break

    return data.sort(key=lambda i: i[sort_choice], reverse=sort_reverse)


def write_files(data):
    # save csv
    with open("av.csv", "w", encoding="utf-8", newline="") as av_c:
        av_writer = csv.writer(av_c, delimiter=";")
        for row in data:
            av_writer.writerow(row)

    # save json
    js_data = dict(zip([str(_) for _ in range(len(data))], [_ for _ in data]))
    with open("av.json", "w", encoding="utf-8") as av_j:
        json.dump(js_data, av_j, ensure_ascii=False)


data = []

print(time.strftime("%X"))
asyncio.run(main(get_pages_num()))
sort_data(data)
write_files(data)
print(time.strftime("%X"))
