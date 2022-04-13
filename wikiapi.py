import wikipedia
import spacy
import sys

def main():
	wikipedia.set_lang("nl")
	nlp = spacy.load('nl_core_news_sm')

	r_pages = wikipedia.random(10) # max 10
	for p in r_pages:
		try:
			summary = wikipedia.summary(p, sentences=1)
		except wikipedia.exceptions.DisambiguationError as e:
			continue

		doc = nlp(summary)

		# print (f"{p}\n\n{summary}\n\n")

		# for token in doc:
		# 	if token.text == '.':
		# 		print (f"{token.text} <{token.pos_}>")
		# 		break
		# 	else:
		# 		print (f"{token.text} <{token.pos_}>", end=' ')

		# match summary.split():
		# 	case [_, 'is', 'een', _, 'uit', 'de', *rest]:
		# 		print ('-- --- -- soms -- --- --')
		# 		print (p)
		# 		print (' '.join(rest))
		# 		print ('-- --- -- soms -- --- --')
		# 	case [_, _, 'is', 'een', _, 'uit', 'de', *rest]:
		# 		print ('-- --- -- bio -- --- --')
		# 		print (p)
		# 		print (' '.join(rest))
		# 		print ('-- --- -- bio -- --- --')
		# 	case [_, _, _, 'is', 'een', _, 'uit', 'de', *rest]:
		# 		print ('-- --- -- ook -- --- --')
		# 		print (p)
		# 		print (' '.join(rest))
		# 		print ('-- --- -- ook -- --- --')
		# 	case [_, _, 'is', 'een', _, 'in', 'de', *rest]: # 'taxonomische', 'indeling'
		# 		print ('-- --- -- nog -- --- --')
		# 		print (p)
		# 		print (' '.join(rest))
		# 		print ('-- --- -- nog -- --- --')
		# 	case [_, _, 'is', 'een', _, _, _, 'uit', 'de', *rest]: # 'taxonomische', 'indeling'
		# 		print ('-- --- -- kort -- --- --')
		# 		print (p)
		# 		print (' '.join(rest))
		# 		print ('-- --- -- kort -- --- --')
		# 	case [_, _, 'is', 'een', _, _, _, 'uit', 'de', *rest]: # 'taxonomische', 'indeling'
		# 		print ('-- --- -- lang -- --- --')
		# 		print (p)
		# 		print (' '.join(rest))
		# 		print ('-- --- -- lang -- --- --')
		# 	case _:
		# 		print (p)
		# 		print (summary)
		# print('\n')

def thank():
	wikipedia.donate()
	# your favorite web browser will open to the donations page of the Wikimedia project
	# because without them, none of this would be possible

if __name__ == "__main__":
	sys.exit(main())
