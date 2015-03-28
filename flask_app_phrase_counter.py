from flask import Flask, render_template, request, session
from phrase_counter import extract_phrases
from collections import Counter
import csv, json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/input')
def input():
	session.pop('txtinput', None)
	session.pop('howmany', None)
	return render_template('input.html')


@app.route('/output', methods=['POST'])
def output():
	session['txtinput'] = request.form['txtinput']
	session['howmany'] = int(request.form['howmany'])
	
	phrase_counter = Counter()
	sent_dict = {}
	
	extract_phrases(session['txtinput'], phrase_counter, sent_dict, 2)
	phrases = []
	for key, value in phrase_counter.most_common(session['howmany']):
		phrases.append((key, value))
	session['phrases'] = phrases
	
	phrase_file = csv.writer(open('data/phrases.csv', 'w'))
	phrase_file.writerows(phrases)
	
	for key in sent_dict:
		sent_dict[key] = list(sent_dict[key])
	
	sent_file = csv.writer(open('data/sent_dict.csv', 'w'))
	for key in sent_dict:
		sent_file.writerow([key, json.dumps(sent_dict[key])])

	return render_template('output.html', phrases=phrases, sent_dict=sent_dict)


@app.route('/output/phrase/<phrase>', methods=['GET'])
def output_phrase(phrase):
	infile = csv.reader(open('data/sent_dict.csv'))
	sentences = []
	for row in infile:
		if row[0] == phrase:
			sentences.extend(json.loads(row[1]))
	return render_template('phrases.html', phrase=phrase, sentences=sentences)














if __name__ == '__main__':
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run(debug=True)
