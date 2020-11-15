import argparse
import string
from epitran import Epitran

def get_corpus(path, epi):
	corpus_sentences = []
	corpus_words = []

	with open(path, 'r') as text:
		lines = text.readlines()

		for line in lines:
			# remove digits
			line = line.translate(str.maketrans('', '', string.digits))
			# remove punctuation
			line = line.translate(str.maketrans('', '', string.punctuation))
			# remove nl character
			line = line.replace("\n", "")
			# transliterate g2p
			line_phonetic = epi.transliterate(line)

			# add sentences and words to corpus
			corpus_sentences.append(line_phonetic)
			for word in line_phonetic.split(" "):
				corpus_words.append(word)

	return corpus_sentences, corpus_words

def main():
	# parsing of input flags
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
					help="output additional information")
	parser.add_argument("file", type=str,
                    help="input file used as training data")
	args = parser.parse_args()

	# preparing the corpus
	epi = Epitran("nld-Latn")
	sentences, words = get_corpus(args.file, epi)

	# Output corpus info if verbose
	if (args.verbosity == 2):
		for line in sentences:
			print(line)
		print(sorted(set(words)))
	elif (args.verbosity == 1):
		print("Sentences: {}\nUnique words: {}" \
								.format(len(set(sentences)), len(set(words))))

if __name__ == "__main__":
	main()
