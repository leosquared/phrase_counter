import nltk, re, string, csv, sys
from nltk.util import ngrams
from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import stopwords
from collections import Counter

unwanted = [string.punctuation] + stopwords.words('english')

def untokenize(ngram):
	ngram = [str(word) for word in ngram]
	return ' '.join(ngram)

def extract_phrases(text, phrase_counter, sent_dict, length):
	text = text.encode('ascii', 'ignore')
	for sent in nltk.sent_tokenize(text):
		words = WhitespaceTokenizer().tokenize(sent.lower())
		for phrase in ngrams(words, length):
			if not all(word in unwanted for word in phrase):
				phrase_counter[untokenize(phrase)] += 1
				sent_dict.setdefault(untokenize(phrase), set()).update([sent])

# phrase_counter = Counter()
# sent_dict = {}
# 
# with open(sys.argv[1]) as sentencesfile:
# 	column = int(raw_input('which column?\n'))
# 	reader = csv.reader(sentencesfile)
# 	reader.next()
# 	for sentence in reader:
# 		extract_phrases(sentence[column], phrase_counter, sent_dict, 2)
# 		extract_phrases(sentence[column], phrase_counter, sent_dict, 1)
# 
# most_common_phrases = phrase_counter.most_common(100)
# 
# for key, value in most_common_phrases:
# 	print '{0:<5}'.format(value), key
# 
# phrase_select = raw_input('type in a particular word to see sample sentences\n')
# 
# with open('sentences_with_{0}.txt'.format(phrase_select), 'w') as outfile:
# 	for sent in sent_dict.get(phrase_select):
# 		print sent, '\n'
# 		outfile.write(sent+'\n')
# 
# 			