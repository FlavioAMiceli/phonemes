import spacy
import sys

def main():
	nlp = spacy.load('nl_core_news_sm')
	doc1 = nlp("Siccia orbiculata is een vlinder uit de familie spinneruilen (Erebidae), onderfamilie beervlinders (Arctiinae). De wetenschappelijke naam van de soort is voor het eerst geldig gepubliceerd in 2007 door Kühne. Deze nachtvlinder komt voor in tropisch Afrika.")
	doc2 = nlp("Acolastus minimus is een keversoort uit de familie bladkevers (Chrysomelidae). De wetenschappelijke naam van de soort werd in 1917 gepubliceerd door Jacobson.")
	doc3 = nlp("Salasaca spinea is een vlinder uit de familie van de spanners (Geometridae). De wetenschappelijke naam van de soort is voor het eerst geldig gepubliceerd in 1983 door Rindge.")
	doc4 = nlp("Tipula (Trichotipula) kennedyana is een tweevleugelige uit de familie langpootmuggen (Tipulidae).")

	# Phalacrophyto is een geslacht van vliegen (Brachycera) uit de familie van de sluipvliegen (Tachinidae).
	# Dipsalidictis is een uitgestorven roofzoogdier behorend tot de familie Oxyaenidae van de Creodonta dat in het Laat-Paleoceen en Vroeg-Eoceen in Noord-Amerika leefde.
	# Epamera is een geslacht van vlinders van de familie Lycaenidae.
	# Het markiezinnetje (Dascyllus aruanus) is een straalvinnige vissensoort uit de familie van de rifbaarzen en koraaljuffertjes (Pomacentridae).
	# Arenorbis is een geslacht van uitgestorven slangsterren uit de familie Ophiolepididae.
	# Plagiostomum quadrioculatum is een platworm (Platyhelminthes).
	# Pseudogobio is een geslacht van straalvinnige vissen uit de familie van eigenlijke karpers (Cyprinidae).
	# Aspilota flagimilis is een insect dat behoort tot de orde vliesvleugeligen (Hymenoptera) en de familie van de schildwespen (Braconidae).
	# Hyalonema (Coscinonema) conus is een sponssoort in de taxonomische indeling van de glassponzen (Hexactinellida).
	# Lasioglossum albipenne is een vliesvleugelig insect uit de familie Halictidae.
	# Mijten (Acariformes) zijn kleine geleedpotigen met een lichaam dat niet duidelijk in twee (zoals bij spinnen) of drie (zoals bij insecten) geledingen is gedeeld.
	# Perilitus trigonalis is een insect dat behoort tot de orde vliesvleugeligen (Hymenoptera) en de familie van de schildwespen (Braconidae).

	# LIJST
	# De lijst van vlinders in IJsland bevat alle vlindersoorten die voorkomen in IJsland.
	#

	# for token in doc1:
	# 	if token.text == '.':
	# 		print (f"{token.pos_}")
	# 		break
	# 	else:
	# 		print (f"{token.pos_}", end=' ')
	#
	# for token in doc2:
	# 	if token.text == '.':
	# 		print (f"{token.pos_}")
	# 		break
	# 	else:
	# 		print (f"{token.pos_}", end=' ')
	#
	# for token in doc3:
	# 	if token.text == '.':
	# 		print (f"{token.pos_}")
	# 		break
	# 	else:
	# 		print (f"{token.pos_}", end=' ')

	for token in doc4:
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

# Tipula <PROPN> ( <PUNCT> Trichotipula <PROPN> ) <PUNCT> kennedyana <PROPN> is <AUX> een <DET> tweevleugelige <ADJ> uit <ADP> de <DET> familie <NOUN> langpootmuggen <VERB> ( <PUNCT> Tipulidae <PROPN> ) <PUNCT> . <PUNCT>
# PROPN PUNCT PROPN PUNCT PROPN AUX DET ADJ ADP DET NOUN VERB PUNCT PROPN PUNCT PUNCT

# 'Naam' 						'naam'					'is' 	'een' 	'SOORT' 'uit de familie'				'FAMILIE (Naam)' 			'ONDERFAMILIE (Naam)'
# PROPN 						VERB 					AUX 	DET 	NOUN 	ADP DET NOUN 					VERB PUNCT PROPN PUNCT PUNCT NOUN ADJ PUNCT PROPN PUNCT PUNCT
# PROPN 						PROPN 					AUX 	DET 	NOUN 	ADP DET NOUN 					VERB PUNCT PROPN PUNCT PUNCT
# 			'(Naam)'
# PROPN 	PUNCT PROPN PUNCT 	PROPN 					AUX 	DET 	ADJ 	ADP DET NOUN 					VERB PUNCT PROPN PUNCT PUNCT
# 																				'van de'
# PROPN 						SYM 					AUX 	DET 	NOUN 	ADP DET NOUN 		ADP DET 	NOUN PUNCT NOUN PUNCT PUNCT
