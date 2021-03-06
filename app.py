from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import keyphrase_tools

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):  # data base class
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(300), nullable=False)
	text = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime, default=datetime.utcnow)

	# keys = db.relationship('Post', backref='Article', uselist=False)

	def __repr__(self):
		return f'<Article {self.id}>'


class Keys(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	phrase = db.Column(db.Text, nullable=True)
	wiki_page = db.Column(db.Text, nullable=True)

	# article_id = db.Column(db.Integer(), db.ForeignKey('Article.id'))

	def __repr__(self):
		return f'<Keys {self.id}>'


@app.route('/all_keys')  # show top phrases from text
def get_keys_top():
	keys_all = Keys.query.order_by(Keys.id).all()
	keys_all = keyphrase_tools.get_top_phrases(keys_all)
	return render_template('all_keys.html', title="all keys", keys=keys_all)


@app.route('/posts/<int:id>', methods=['POST', 'GET'])  # post keyphrase
def post_detail(id):
	if request.method == 'POST':
		return post_delete(id)
	kp = Keys.query.get(id)  # get data
	keys = zip(kp.phrase.split('\n'), kp.wiki_page.split(' '))
	return render_template('post_keyphrases.html', keys=keys, id=id, )


@app.route('/posts')  # get all text post
def posts():
	try:
		articles = Article.query.order_by(Article.date.desc()).all()  # all data from db
	except:
		articles = []
	return render_template('posts.html', articles=articles)


@app.route('/', methods=['POST', 'GET'])  # main page add new text and save to data base
def create_article():
	if request.method == "POST":
		text = request.form['text']
		title = request.form['title']
		phrase = keyphrase_tools.get_keyphrase(text)
		wiki_info = ' '.join(keyphrase_tools.check_wiki_page_exst(key) for key in phrase)
		article = Article(title=title, text=text)
		keys = Keys(phrase='\n'.join(phrase), wiki_page=wiki_info)
		try:
			db.session.add(keys)
			db.session.add(article)
			db.session.commit()
			return redirect('/posts')
		except:
			return 'Something’s not right \nTry again'
	return render_template("create-article.html")


@app.after_request
def after_request(response):
	print("after_request() called")
	return response


def post_delete(id):
	article: object = Article.query.get_or_404(id)
	keys = Keys.query.get_or_404(id)
	try:
		db.session.delete(keys)
		db.session.delete(article)
		db.session.commit()
		return redirect('/')
	except:
		return 'Something’s not right \ntext not deleted'


if __name__ == '__main__':
	app.run(debug=True)
