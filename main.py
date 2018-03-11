import requests
import string
from pprint import pprint
from bs4 import BeautifulSoup


def extract_author(athing):
	# возвращаем автора из новости
	return athing.find("a", {"class": "hnuser"}).contents[0]


def extract_title(athing):
	# возвращаем заголовок из новости
	return athing.find("a", {"class": "storylink"}).contents[0]


def extract_points(athing):
	# возвращаем количество голосов из новости
	return int(athing.find("span", {"class": "score"}).contents[0].strip(string.ascii_letters))


def extract_comments(athing):
	# возвращаем количество комментариев из новости
	contents = athing.find("td", {"class": "subtext"}).contents[-2].contents[0]
	return 0 if contents == "discuss" else int(contents.strip(string.ascii_letters))


def extract_url(athing):
	# возвращаем url из новости если он есть, иначе возвращаем None
	url = athing.find("a", "storylink")["href"]
	return url if url.find("http") == 0 else None


def extract_id(athing):
	return int(athing.find("tr", {"class": "athing"})["id"])


def extract_data(athing):
	# принимаем новость в формате html и возвращаем ее же, но в виде словаря с полями author, text и т.д.
	parsable_athing = BeautifulSoup(athing, 'html.parser')

	return {
		"id": extract_id(parsable_athing),
		"author": extract_author(parsable_athing),
		"title": extract_title(parsable_athing),
		"url": extract_url(parsable_athing),
		"comments": extract_comments(parsable_athing),
		"points": extract_points(parsable_athing) 
	}


def extract_news_by_start_item(start = 0):

	# Получить 30 новостей, начиная с определенной новости

	host = "https://news.ycombinator.com/newest?next=" + str(start)	# откуда берем новости
	request_text = requests.get(host).text
	request_html = BeautifulSoup(request_text, 'html.parser')

	news_table = request_html.find("table", {"class": "itemlist"})
	news_table_contents = ''.join(map(str, news_table.contents))	# удаляем <table> и </table>
	news_list = news_table_contents.split('<tr class="spacer" style="height:5px"></tr>')[:-1]	# избавились от <tr> More...

	news = list(map(extract_data, news_list))

	return news


def extract_news(n_pages):
	news = []

	for i in range(n_pages):
		
		last_item_id = 0
		
		if len(news) != 0:
			last_item_id = news[-1]["id"]

		news = news + extract_news_by_start_item(last_item_id)

	return news


pprint(extract_news(2))
