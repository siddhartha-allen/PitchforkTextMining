#! python3
import math
import time
import re
import unicodecsv as csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

def main():	

	start = time.time()

	errored_links = 0

	with open('pitchfork_review_data.csv', 'wb') as outfile:
		writer = csv.writer(outfile, encoding='utf-16')
		header = ["Artist", "Album", "Genres", "Reviewer", "Reviewed On", "Review Link"]
		writer.writerow(header)

		#Iterating through 800 pages of reviews. This should give us ~8,000 reviews to work with
		for num in range(1, 1001):
			collect_urls_link = "https://pitchfork.com/reviews/albums/?page={}".format(num)

			try:
				pull_site = urlopen(collect_urls_link)
				soup = BeautifulSoup(pull_site, 'lxml')

				print("Collecting data on page {}".format(num))

				#Pulling Review Data
				for a in soup.find_all('div', class_ = 'review'):
					#Getting Review Urls
					href_data = a.find('a', class_ = 'review__link')
					href = href_data['href']

					#Album Artist
					artist = a.find('ul', class_ = 'artist-list review__title-artist').text

					#Album Title
					title = a.find('h2', class_ = 'review__title-album').text

					#Genre | Reviewer | Publication Date
					Review_Meta = a.find_all('div', class_ = 'review__meta')

					for data in Review_Meta:
						#Genre
						genre_data = data.find_all('li', class_ = 'genre-list__item')
						genre_list = re.findall(r'\?genre=[a-zA-z]*.>([a-zA-z\/]*)', str(genre_data))
						genrestr = '~'.join(genre_list)

						#Reviewer
						reviewer_data = data.find('a', class_ = 'linked display-name display-name--linked')
						reviewer = re.findall(r'<\/span>([a-zA-z ]*)', str(reviewer_data))
						reviewer = reviewer[0]

						#Publication Date
						publication_date_data = data.find(class_ = 'pub-date')
						publication_date = publication_date_data['datetime']

					#Making Sure we have the links correct
					text_link = "https://pitchfork.com{}".format(href)
					#Filtering out the links without reviews
					if href[:17] == "/reviews/albums/?":
						pass
					elif href[:23] == "/reviews/albums/popular":
						pass
					elif text_link == "https://pitchfork.com/reviews/albums/":
						pass
					elif href[:16] == "/reviews/albums/":
						good_link = text_link

					write_row = [artist, title, genrestr, reviewer, publication_date, good_link]
					writer.writerow(write_row)

			except Exception as e:
				errored_links += 1
				pass

	print("{} Links had Errors".format(errored_links))

	finish = time.time()

	elapsed = finish - start
	hours = int(math.floor((elapsed)/3600))
	minutes = int(math.floor((elapsed/60) - (hours*60)))
	seconds = int(math.floor(elapsed - (hours*3600) - (minutes*60)))

	print("\n")
	print("-------------------------------------------------------------------------------")
	print('Time Elapsed: {} hours, {} minutes and {} seconds.'.format(hours, minutes, seconds))
	print("-------------------------------------------------------------------------------")

if __name__ == '__main__':
	main()