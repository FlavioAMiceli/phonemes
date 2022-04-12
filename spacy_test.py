import spacy
import sys

def main():
	nlp = spacy.load('nl_core_news_sm')
	doc1 = nlp("Siccia orbiculata is een vlinder uit de familie spinneruilen (Erebidae), onderfamilie beervlinders (Arctiinae). De wetenschappelijke naam van de soort is voor het eerst geldig gepubliceerd in 2007 door Kühne. Deze nachtvlinder komt voor in tropisch Afrika.")
	doc2 = nlp("Acolastus minimus is een keversoort uit de familie bladkevers (Chrysomelidae). De wetenschappelijke naam van de soort werd in 1917 gepubliceerd door Jacobson.")
	doc3 = nlp("Salasaca spinea is een vlinder uit de familie van de spanners (Geometridae). De wetenschappelijke naam van de soort is voor het eerst geldig gepubliceerd in 1983 door Rindge.")


	for token in doc1:
		if token.text == '.':
			print (f"{token.pos_}")
			break
		else:
			print (f"{token.pos_}", end=' ')

	for token in doc2:
		if token.text == '.':
			print (f"{token.pos_}")
			break
		else:
			print (f"{token.pos_}", end=' ')

	for token in doc3:
		if token.text == '.':
			print (f"{token.pos_}")
			break
		else:
			print (f"{token.pos_}", end=' ')

	# for token in doc:
	# 	# print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
	#     #         token.shape_, token.is_alpha, token.is_stop)
	#
	# 	print(token.text, token.pos_)

	return 0

if __name__ == "__main__":
	sys.exit(main())

# Siccia <PROPN> orbiculata <VERB> is <AUX> een <DET> vlinder <NOUN> uit <ADP> de <DET> familie <NOUN> spinneruilen <VERB> ( <PUNCT> Erebidae <PROPN> ) <PUNCT> , <PUNCT> onderfamilie <NOUN> beervlinders <ADJ> ( <PUNCT> Arctiinae <PROPN> ) <PUNCT> . <PUNCT>
# PROPN VERB AUX DET NOUN ADP DET NOUN VERB PUNCT PROPN PUNCT PUNCT NOUN ADJ PUNCT PROPN PUNCT PUNCT

# Acolastus <PROPN> minimus <PROPN> is <AUX> een <DET> keversoort <NOUN> uit <ADP> de <DET> familie <NOUN> bladkevers <VERB> ( <PUNCT> Chrysomelidae <PROPN> ) <PUNCT> . <PUNCT>
# PROPN PROPN AUX DET NOUN ADP DET NOUN VERB PUNCT PROPN PUNCT PUNCT

# Salasaca <PROPN> spinea <SYM> is <AUX> een <DET> vlinder <NOUN> uit <ADP> de <DET> familie <NOUN> van <ADP> de <DET> spanners <NOUN> ( <PUNCT> Geometridae <NOUN> ) <PUNCT> . <PUNCT>
# PROPN SYM AUX DET NOUN ADP DET NOUN ADP DET NOUN PUNCT NOUN PUNCT PUNCT

# 'Naam' 'naam'	'is' 	'een' 	'SOORT' 'uit de familie'				'FAMILIE (Naam)' 			'ONDERFAMILIE (Naam)'
# PROPN 	VERB 	AUX 	DET 	NOUN 	ADP DET NOUN 					VERB PUNCT PROPN PUNCT PUNCT NOUN ADJ PUNCT PROPN PUNCT PUNCT
# PROPN 	PROPN 	AUX 	DET 	NOUN 	ADP DET NOUN 					VERB PUNCT PROPN PUNCT PUNCT
# 															'van de'
# PROPN 	SYM 	AUX 	DET 	NOUN 	ADP DET NOUN 		ADP DET 	NOUN PUNCT NOUN PUNCT PUNCT
