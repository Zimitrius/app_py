import RAKE
import wikipediaapi


def get_keyphrase(user_text):  # get keyphrase from text end send keywords list to saver
	rake_obj = RAKE.Rake("SmartStoplist.txt")
	keywords = rake_obj.run(user_text)
	return keywords


def check_wiki_page_exst(word):  # check if keyphrase exist and return bool condition
	wiki_wiki = wikipediaapi.Wikipedia('en')
	page_check = wiki_wiki.page(word)
	status = page_check.exists()
	if status:
		return page_check.fullurl  # get url
	return None  # wikipedia page not exist


def get_top_phrases(list_all):
	doc = {}
	for lst in list_all:
		for key in lst.phrases.split('\n'):
			doc[key] = doc.get(key, 0) + 1
	return sorted(doc.items(), key=lambda x: x[1], reverse=1)