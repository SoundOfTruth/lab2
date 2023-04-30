from aiogram import Bot, Dispatcher, executor, types
from config import token, cookies
import requests
from bs4 import BeautifulSoup
bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("Введите название препарата")

@dp.message_handler()
async def answer(message: types.Message):
    response = requests.get("https://apteka-ot-sklada.ru/catalog?q=беродуал", cookies=cookies)
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.findAll('div', attrs={"itemprop": "itemListElement"})
    print(response.status_code)
    for i in range(len(result)):
        try:
            name = result[i].find(attrs={"itemprop": "name"}).text
            price = result[i].find("span", class_="ui-link__text").text.replace('\n  ', '').replace("аптеках", "аптеках ")
            link = "https://apteka-ot-sklada.ru" + result[i].find('a').get('href') + '/pharmacies'
            answers = name + "\n" + price + '\n' + link
            await message.answer(answers)
        except AttributeError: pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)