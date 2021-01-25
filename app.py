from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from keyphrase_extr import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)   #


class Article(db.Model):  # data base class
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(300), nullable=False)
	text = db.Column(db.Text, nullable=False)
	phrases = db.Column(db.Text, nullable=True)
	date = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f'<Article {self.id}>'


@app.route('/posts')  # get all text post
def posts():
	articles = Article.query.order_by(Article.date.desc()).all()  # all data from db
	return render_template('posts.html', articles=articles)


@app.route('/all_keys')  # show top phrases from text
def get_keys_top():
	keys_all = Article.query.order_by(Article.date.desc()).all()
	keys_all = get_top_phrases(keys_all)
	return render_template('all_keys.html', title="all keys", keys=keys_all)


@app.route('/posts/<int:id>')  # post keyphrase
def post_detail(id):
	article = Article.query.get(id)  # get data
	title = article.title
	keys = get_keyphrase(article.text)
	save_keyphrase(keys, id)
	return render_template('post_keyphrases.html', keys=keys, title=title, id=id)


@app.route('/posts/<int:id>/del')  # deleted post
def post_delete(id):
	article = Article.query.get_or_404(id)
	try:
		db.session.delete(article)
		db.session.commit()
		return redirect('/')
	except:
		return 'Something’s not right \ntext not delet'


@app.route('/posts/<string:key>')  # chekc if wiki link exist for keyphrase
def key_detal(key):
	page = check_wiki_page_exst(key)
	return render_template('chek_wiki.html', key=key.upper(), page=page)


@app.route('/', methods=['POST', 'GET'])  # main page add new text and save to data base
def create_article():
	if request.method == "POST":
		title = request.form['title']
		text = request.form['text']

		article = Article(title=title, text=text)

		try:
			db.session.add(article)  # add new text to data base
			db.session.commit()
			return redirect('/posts')
		except:
			return 'Something’s not right \nTry again'

	else:
		return render_template("create-article.html")


def save_keyphrase(keys_p, id):  # save key phrases list
	article = Article.query.get(id)

	if article.phrases:
		return

	article.phrases = '\n'.join([e[0] for e in keys_p])

	try:
		db.session.add(article)
		db.session.commit()
		return
	except:
		return 'Something’s not right \nTry again'


if __name__ == '__main__':
	app.run(debug=True)