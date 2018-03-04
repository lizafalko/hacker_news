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


def extract_data(athing):
	# принимаем новость в формате html и возвращаем ее же, но в виде словаря с полями author, text и т.д.
	parsable_athing = BeautifulSoup(athing, 'html.parser')

	return {
		"author": extract_author(parsable_athing),
		"title": extract_title(parsable_athing),
		"url": extract_url(parsable_athing),
		"comments": extract_comments(parsable_athing),
		"points": extract_points(parsable_athing) 
	}


def extract_news(n_pages):
	host = "https://news.ycombinator.com/newest"	# откуда берем новости
	request_text = requests.get(host).text
	request_html = BeautifulSoup(request_text, 'html.parser')

	news_table = request_html.find("table", {"class": "itemlist"})
	news_table_contents = ''.join(map(str, news_table.contents))	# удаляем <table> и </table>
	news_list = news_table_contents.split('<tr class="spacer" style="height:5px"></tr>')[:-1]	# избавились от <tr> More...

	return list(map(extract_data, news_list))


pprint(extract_news(2))
