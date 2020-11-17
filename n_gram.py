import json
import argparse
import string
from epitran import Epitran
from collections import defaultdict

class NGLM:

	def __init__(self, path, epi, order=3):
		self._order = order
		self._count_table = dict()
		self._prob_table = dict()
		self._corpus = list()
		self._vocab = set()

		self.set_corpus(path, epi)
		self.set_vocab()

	def set_corpus(self, path, epi, use_dict=True):
		def clean_line(line):
			# remove digits
			line = line.translate(str.maketrans('', '', string.digits))
			# remove punctuation
			line = line.translate(str.maketrans('', '', string.punctuation))
			# to lower case
			line = line.lower()
			# remove nl character
			line = line.replace("\n", "")

			return line

		corpus_sentences = []
		with open(path, 'r') as text, \
			open('g2p_dictionary/dutch_dic_to_phonetic.1.json', 'r') as g2p_file:
			lines = text.readlines()
			g2p_dict = json.load(g2p_file)
			g2p_dict = {k.lower():v for k,v in g2p_dict.items()}

			for line in lines:
				line = clean_line(line)
				# transliterate g2p using dict with epitran as fallback
				if (use_dict):
					line_phonetic = []
					for word in line.split():
						word_phonetic = g2p_dict.get(word, epi.transliterate(word))
						line_phonetic.append(word_phonetic)
					corpus_sentences.append(" ".join(line_phonetic))
				# transliterate using epitran
				else:
					line_phonetic = epi.transliterate(line)
					corpus_sentences.append(line_phonetic)

		self._corpus = corpus_sentences

	def set_vocab(self):
		self._vocab = set()

		for line in self._corpus:
			self._vocab.update(line.split())


	def rm_lines_with_rare_words(self, min_count=1):

		# get word count in corpus
		count = defaultdict(int)
		for line in self._corpus:
			for word in line.split():
				count[word] += 1

		# store lines that do not contain rare words
		sentences = []
		for line in self._corpus:
			add = True
			for word in line.split():
				if count[word] < min_count:
					add = False
					break
			if (add):
				sentences.append(line)

		self._corpus = sentences
		self.set_vocab()

	def rm_short_lines(self, min_length=1):
		sentences = []
		for line in self._corpus:
			if (len(line.split()) >= min_length):
				sentences.append(line)

		self._corpus = sentences
		self.set_vocab()

def main():
	# parsing of input flags
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbose", nargs='?', const=1, type=int,
					help="output additional information")
	parser.add_argument("-c", "--count", type=int,
					help="Prune sentences with words that occur less than COUNT times in corpus.")
	parser.add_argument("-l", "--length", type=int,
					help="Prune sentences that have fewer than LENGTH words.")
	parser.add_argument("file", type=str,
                    help="input file used as training data")
	args = parser.parse_args()

	# Transliterating the corpus
	epi = Epitran("nld-Latn")
	n_gram_lm = NGLM(args.file, epi)

	# Output corpus info if verbose
	if (args.verbose):
		print("\nBefore pruning:")
		print("Sentences: {}\nUnique words: {}" \
								.format(len(n_gram_lm._corpus), len(n_gram_lm._vocab)))

	# Prune sentences
	if (args.count):
		n_gram_lm.rm_lines_with_rare_words(args.count)
	if (args.length):
		n_gram_lm.rm_short_lines(args.length)

	# Output corpus info if verbose
	if (args.verbose):
		print("\nAfter pruning:")
		print("Sentences: {}\nUnique words: {}" \
								.format(len(n_gram_lm._corpus), len(n_gram_lm._vocab)))

if __name__ == "__main__":
	main()
