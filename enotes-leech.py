import itertools
import string
import sys
import json
import re

from bs4 import BeautifulSoup
import requests

# Your enotes.com username and password
USERNAME = None
PASSWORD = None


def main():
	session = requests.Session()

	login_url = "https://www.enotes.com/jax/index.php/users/login" \
	            "?eventHandler=handleLogin"
	result = session.post(login_url,
		                  data={"login": USERNAME, "password": PASSWORD})
	if b'<a href="/logout">Sign Out</a>' not in result.content:
		exit("ERROR: could not sign in!")

	if len(sys.argv) < 2:  # crawl all the guides
		guides = find_all_guides()
		guides_file = open("guides.json", "w")
		json.dump(guides, guides_file)
		guides_file.flush()
		guides_file.close()
	else:  # load the guides from the json file (the first argument)
		with open(sys.argv[1]) as guides_file:
			guides = json.load(guides_file)
			print("file loaded: {} topics is found.".format(len(guides)))

	for completed, guide in enumerate(guides):
		print("\rdownloading guides: {} out of {} completed "\
			  "(now downloading '{}')...\033[K" \
			  .format(completed, len(guides), guide), end="")

		result = session.get(guides[guide] + "/completePDF")
		if result.status_code != 200:
			result = session.get(guides[guide] + "/etext/pdf/complete")
			if result.status_code != 200:
				print('ERROR: could not download "{}" ({})' \
					  .format(guide, guides[guide]))
				break

		content_disposition = result.headers["content-disposition"]
		filename = re.findall("filename=(.+)", content_disposition)[0]

		pdf = open(filename, "wb")
		pdf.write(result.content)
		pdf.flush()
		pdf.close()


def find_all_guides():
	guides = {}
	for letter in string.ascii_lowercase:
		# Increase the page number until the page is not found (404)
		for page in itertools.count(start=1):
			print("\rcrawling topics: letter '{}' page {}...\033[K" \
				  .format(letter, page), end="")

			url = "https://www.enotes.com/topics/alpha/{letter}?pg={page}"
			result = requests.get(url.format(letter=letter, page=page))
			
			# The page is not found. Stop increasing the page number, and
			# increase the letter.
			if result.status_code == 404: 
				break

			soup = BeautifulSoup(result.content, "html.parser")
			guide_URL_scheme = "https://www.enotes.com{}"
			for link in soup.find_all("a", itemprop="item"):
				guides[link.text] = guide_URL_scheme.format(link["href"])

	print("\ncrawling completed: {} topics is found.".format(len(guides)))
	return guides


if __name__ == '__main__':
	main()
