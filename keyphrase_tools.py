import RAKE
import wikipediaapi


def get_keyphrase(user_text):  # get keyphrase from text end send keywords list to saver
	rake_obj = RAKE.Rake("SmartStoplist.txt")
	keywords = rake_obj.run(user_text)
	return '\n'.join(e[0] for e in keywords)


def check_wiki_page_exst(word):  # check if keyphrase exist and return bool condition
	wiki_page = wikipediaapi.Wikipedia('en').page(word)
	if not wiki_page.exists():
		return None  # wikipedia page not exist
	return wiki_page.fullurl  # get url


def get_top_phrases(list_all):  # get sorted top list
	doc = {}
	for lst in list_all:
		for key in lst.phrase.split('\n'):
			doc[key] = doc.get(key, 0) + 1
	return sorted(doc.items(), key=lambda x: x[1], reverse=1)
