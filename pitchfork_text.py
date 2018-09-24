#! python3
import math
import time
import re
import csv
import unicodecsv
import codecs
import string
from urllib.request import urlopen
from bs4 import BeautifulSoup

def main():	

	start = time.time()

	#Reading out the csv written by the pitchfork.py file
	reader = csv.reader(codecs.open('pitchfork_review_data.csv', 'rU', 'utf-16'))
	total_file_rows = sum(1 for row in reader)

	reader = csv.reader(codecs.open('pitchfork_review_data.csv', 'rU', 'utf-16'))
	rowcount = 0

	#Going to increment through the review data file, pull the text from the links in the file, and write them to a new file
	with open('pitchfork_review_text.csv', 'wb') as outfile:
		writer = unicodecsv.writer(outfile, encoding='utf-16')
		for row in reader:
			if rowcount == 0:
				rowcount = 1
				header = []
				for i in row:
					header.append(i)
				header.append("Score")
				header.append("ReviewText")
				writer.writerow(header)
			else:
				print("Pulling review for site {}/{}".format(rowcount,total_file_rows))

				for i in range(0, len(row)):
					try:
						review_link = row[i]
						pull_site = urlopen(review_link)
						soup = BeautifulSoup(pull_site, 'lxml')
						break
					except Exception as e:
						pass

				review_text = ''

				#Pulling the review score from the webpage
				score = soup.find(class_ = 'score').text

				#Pulling the review text from the webpage
				for text in soup.find_all('p', href=False):
					review = text.getText()
					review.strip("\n").strip("\r")
					printable = set(string.printable)
					newreview = lambda x: x in printable, review
					review+=' '
					review_text+=str(review)
				newrow = row
				newrow.append(score)
				newrow.append(review_text)
				writer.writerow(newrow)
				newrow = []
				rowcount += 1

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