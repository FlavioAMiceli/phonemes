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

def main():
	file1 = open('datasets/sample_sentences.txt', 'r')
	lines = file1.readlines()

	# phonemes = ""
	# backoff = Backoff(['nld-Latn', 'eng-Latn'])
	epi = Epitran('nld-Latn')

	for line in lines:
		print(epi.transliterate(line))

	file1.close()
	# print(phonemes)

if __name__ == "__main__":
	main()
