import json
from epitran.backoff import Backoff
from epitran import Epitran

def epi_test():
	# Just look at Dutch phonemes
	epi = Epitran('nld-Latn')
	print(epi.transliterate('Werkt'))

	# Look at English phonemes first, also consider Dutch.
	# Here to see if flite works.
	backoff = Backoff(['eng-Latn', 'nld-Latn'])
	print(backoff.transliterate('Werkt'))

def compare_epi_to_dict():
	dict_file = open('g2p_dictionary/dutch_dic_to_phonetic.1.json', 'r')
	g2p_dict = json.load(dict_file)
	epi = Epitran('nld-Latn')
	# n = 0
	for key in g2p_dict:
		dic_word = g2p_dict[key]
		epi_word = epi.transliterate(key)
		if (dic_word != epi_word):
			# n += 1
			fstring = "Key: %s\nDic: %s\nEpi: %s\n" % (key, dic_word, epi_word)
			print (fstring)
	# print (n)

def main():
	# file1 = open('datasets/sample_sentences.txt', 'r')
	# lines = file1.readlines()
	#
	# # phonemes = ""
	# # backoff = Backoff(['nld-Latn', 'eng-Latn'])
	# epi = Epitran('nld-Latn')
	#
	# for line in lines:
	# 	print(epi.transliterate(line))
	#
	# file1.close()
	# print(phonemes)

	compare_epi_to_dict()

if __name__ == "__main__":
	main()
