#! python3
import math
import time
import csv
import codecs
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def remove_stop_words(text):
	stops = set(stopwords.words("english"))

	#adding words to the set
	stops.add('</s>')
	stops.add('the')
	stops.add('and')
	stops.add('a')
	stops.add('that')
	stops.add('is')
	stops.add('as')

	#adding prepositions to the set
	stops.add('about')
	stops.add('above')
	stops.add('across')
	stops.add('after')
	stops.add('against')
	stops.add('along')
	stops.add('among')
	stops.add('around')
	stops.add('at')
	stops.add('because')
	stops.add('before')
	stops.add('behind')
	stops.add('below')
	stops.add('beneath')
	stops.add('besides')
	stops.add('beside')
	stops.add('between')
	stops.add('but')
	stops.add('by')
	stops.add('concerning')
	stops.add('despite')
	stops.add('down')
	stops.add('during')
	stops.add('except')
	stops.add('excepting')
	stops.add('for')
	stops.add('from')
	stops.add('in')
	stops.add('inside')
	stops.add('in spite')
	stops.add('into')
	stops.add('like')
	stops.add('near')
	stops.add('of')
	stops.add('off')
	stops.add('on')
	stops.add('onto')
	stops.add('out')
	stops.add('outside')
	stops.add('over')
	stops.add('past')
	stops.add('regarding')
	stops.add('since')
	stops.add('through')
	stops.add('throughout')
	stops.add('to')
	stops.add('toward')
	stops.add('under')
	stops.add('underneath')
	stops.add('up')
	stops.add('upon')
	stops.add('with')
	stops.add('within')
	stops.add('without')

	#removing all punctuation from the dataset
	stops.add("'")
	stops.add('"')
	stops.add('.')
	stops.add('/')
	stops.add('\\')
	stops.add('?')
	stops.add('<')
	stops.add('>')
	stops.add('`')
	stops.add('~')
	stops.add('!')
	stops.add('@')
	stops.add('#')
	stops.add('%')
	stops.add('^')
	stops.add('&')
	stops.add('*')
	stops.add('(')
	stops.add(')')
	stops.add('-')
	stops.add('_')
	stops.add('_')
	stops.add('+')
	stops.add('=')

	word_tokens = word_tokenize(text) 

	filtered_sentence = [w for w in word_tokens] 

	filtered_sentence_str = ''

	for word in filtered_sentence:
		if word.lower() in stops:
			pass
		else:
			filtered_sentence_str+= word.lower().strip('"').strip("'").strip('.').strip('/').strip('\\').strip('?').strip('<').strip('>').strip('`').strip('~').strip('!').strip('@').strip('#').strip('$').strip('%').strip('^').strip('&').strip('*').strip('(').strip(')').strip('+').strip('=')
			filtered_sentence_str+= ' '

	return(filtered_sentence_str)

def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)

def main():	

	start = time.time()

	#nltk.download('stopwords')
	#nltk.download('punkt')

	reader = csv.reader(codecs.open('pitchfork_review_text.csv', 'rU', 'utf-16'))

	ID = "rVpch"
	counter = 0

	text_header = ['Text','ID']
	meta_header = ['ID', 'Artist', 'Album', 'Genre', 'Reviewed By', 'Reviewed Date', 'Review Link', 'Score']

	with open("review_text_stopped_labled.csv", 'w', newline = '') as outfile:
		text_writer = csv.writer(outfile)
		text_writer.writerow(text_header)

		with open("review_meta_stopped_labled.csv", 'w', newline = '') as meta_out:
			meta_writer = csv.writer(meta_out)
			meta_writer.writerow(meta_header)
			for row in reader:
				counter += 1
				if counter == 1:
					pass
				else:
					artist = str(remove_non_ascii(row[0]).encode('ascii'))
					album = str(remove_non_ascii(row[1]).encode('ascii'))
					genre = str(remove_non_ascii(row[2]).encode('ascii'))
					reviewer = str(remove_non_ascii(row[3]).encode('ascii'))
					reviewed_date = str(remove_non_ascii(row[4]).encode('ascii'))
					reviewed_link = str(remove_non_ascii(row[5]).encode('ascii'))
					review_score = str(remove_non_ascii(row[6]).encode('ascii'))
					review_text = str(remove_non_ascii(row[7]).encode('ascii'))

					ID_write = str(ID) + "__" + "{:05}".format(counter)

					label = "__label__{} ".format(ID_write)

					review_text_no_stops = str(label) + ' ' + str(remove_stop_words(review_text))

					text_row = []
					text_row.append(review_text_no_stops)
					text_row.append(ID_write)

					meta_row = []
					meta_row.append(ID_write)
					meta_row.append(artist)
					meta_row.append(album)
					meta_row.append(genre)
					meta_row.append(reviewer)
					meta_row.append(reviewed_date)
					meta_row.append(reviewed_link)
					meta_row.append(review_score)

					text_writer.writerow(text_row)
					meta_writer.writerow(meta_row)

					#print("Row: {}: {}".format(counter, label))

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