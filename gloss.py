from flask import Flask, redirect, render_template, request, session
#from io import StringIO
from forms import TestType
import random
app=Flask(__name__)

app.config['SECRET_KEY'] = '1b56d60b2cec942c6b4ed6d90fdd4b81'

@app.route('/')
@app.route('/accueil')
def menu():
	return redirect('/accueil/1')

@app.route('/accueil/<int:i>')
def accueil(i):
	# Page d'accueil (sheet)
	if i > 14: i = 14
	if i < 1: i = 1

	if i < 14: n = i+1
	else: n = 1
	if i > 1: p = i-1
	else: p = 14 

	english = []
	french = []
	important = []
	with open(f'static/page{i}.csv', encoding="utf-8") as f:
		for line in f:
			a = line.split(';')
			english.append(a[0])
			french.append(a[1])
			important.append(a[2])
	tosend = english + french + important
	l = int(len(tosend)/3)

	return render_template('accueil.html', page=i, previouspage=p, nextpage=n, listed=tosend, lenght=l)



@app.route('/test', methods=['GET', 'POST'])
def test():
	form = TestType()
	if form.validate_on_submit():
		if form.radio.data == 'page': n = form.select.data
		elif form.radio.data == 'whole': n = form.nbmot.data
		return redirect(f'/go/{form.radio.data}&n={n}&imp={form.important.data}')
	return render_template('test.html', form=form)

@app.route('/go/<t>&n=<int:n>&imp=<imp>')
def go(t, n, imp):
	if t == 'page': # test sur un page au choix
		if n == 0: n = random.randint(1, 14)
		wordsTest = []
		corTest = []
		nbmots = 0
		with open(f'static/page{n}.csv', encoding="utf-8") as mf:
			for line in mf:
				a = line.split(';')
				if imp == 'False' or (imp == 'True' and str(a[2])[:-1] == 'True'): # seulement les mots importants (*)
					wordsTest.append(a[1])
					corTest.append(a[0])
					nbmots += 1
		ziped = list(zip(wordsTest, corTest))
		random.shuffle(ziped)
		wordsTest, corTest = zip(*ziped)
		session['evalF'] = wordsTest
		session['evalE'] = corTest
		session['page'] = n
		session['nbmots'] = nbmots
		session['type'] = 'page'
		return render_template('pageTest.html', words=wordsTest, page=n, nbmot=nbmots)

	if t == 'whole': # test sur l'intégralité
		wordsTest = []
		corTest = []
		for i in range(n):
			b = []
			page = random.randint(1, 14) # page aléatoire
			with open(f'static/page{page}.csv', encoding="utf-8") as mf:
				mf = mf.read()
				mf = mf.split('\n')
				for l in mf:
					a = l.split(';')
					if imp == 'False' or (imp == 'True' and a[2] == 'True'): b.append(l)
			line = random.randint(1, len(b))-1 # ligne aléatoire
			wordsTest.append(b[line].split(';')[1])
			corTest.append(b[line].split(';')[0])
		session['evalF'] = wordsTest
		session['evalE'] = corTest
		session['nbmots'] = n
		session['type'] = 'whole'
		return render_template('wholeTest.html', words=wordsTest, nbmot=n)


@app.route('/results', methods=['GET', 'POST'])
def results():
	user_answers = []
	if request.method == 'POST':
		for i in range(51):
			try: user_answers.append(request.form.get(str(i)))
			except Exception: pass
	return render_template('results.html', type=session.get('type'), fr=session.get('evalF'), user=user_answers, en=session.get('evalE'), page=session.get('page'), nbmot=session.get('nbmots'))

@app.route('/recherche')
def recherche():
	return render_template('recherche.html', result=0)
@app.route('/recherche', methods=['POST'])
def seeker():
	word = request.form['text']
	tosend = []
	e = []
	f = []
	imp = []
	for i in range(1, 15):
		with open(f'static/page{i}.csv', encoding="utf-8") as mf:
			for line in mf:
				if word.lower() in line.lower():
					a = line.split(';')
					e.append(a[0])
					f.append(a[1])
					imp.append(a[2])
	tosend = e + f + imp
	if len(tosend) > 0: m = 1
	else: m = -1
	l = int(len(tosend)/3)
	return render_template('recherche.html', result=m, listed=tosend, lenght=l, word=word)
	# m = -1 : no result
	# m = 0  : no request
	# m = 1  : results


@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def error_page(error):
	return "Code d'erreur {}".format(error.code), error.code


if __name__ == '__main__':
	app.run(debug = True)