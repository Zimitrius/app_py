import RAKE
import wikipediaapi


def get_keyphrase(user_text):
	rake_obj = RAKE.Rake("SmartStoplist.txt")
	keywords = rake_obj.run(user_text)
	return [e[0] for e in set(keywords)]


def check_wiki_page_exst(word):
	wiki_page = wikipediaapi.Wikipedia('en').page(word)
	if not wiki_page.exists():
		return '0'
	return wiki_page.fullurl


def get_top_phrases(list_all):
	doc = {}
	for lst in list_all:
		for key in lst.phrase.split('\n'):
			doc[key] = doc.get(key, 0) + 1
	return sorted(doc.items(), key=lambda x: x[1], reverse=1)
