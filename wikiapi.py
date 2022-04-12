import wikipedia as wiki
import spacy
import sys

def main():
	wiki.set_lang("nl")
	nlp = spacy.load('nl_core_news_sm')

	r_pages = [wiki.random(1) for i in range(1)]
	for p in r_pages:
		summary = wiki.summary(p, sentences=1)
		doc = nlp(summary)

		print (f"{p}\n\n{summary}\n\n")

		for token in doc:
			if token.text == '.':
				print (f"{token.text} <{token.pos_}>")
				break
			else:
				print (f"{token.text} <{token.pos_}>", end=' ')

if __name__ == "__main__":
	sys.exit(main())
