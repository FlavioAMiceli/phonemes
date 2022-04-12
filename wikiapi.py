import wikipedia as wiki
import spacy
import sys

def main():
	wiki.set_lang("nl")
	nlp = spacy.load('nl_core_news_sm')

	r_pages = [wiki.random(1) for i in range(10)]
	for p in r_pages:
		try:
			summary = wiki.page(p).summary
		except:
			p = wiki.suggest(p)
			summary = wiki.page().summary

		doc = nlp(summary)
		print (f"{p}\n\n{summary}\n")
		for token in doc:
			if token.text == '.':
				print (f"{token.text} <{token.pos_}>")
				break
			else:
				print (f"{token.text} <{token.pos_}>", end=' ')

if __name__ == "__main__":
	sys.exit(main())
