from collections import defaultdict
import json
import string
from epitran import Epitran

class Corpus:

	def __init__(self, path, epi_code):
		self._file = path
		self._dict_file = 'g2p_dictionary/dutch_dic_to_phonetic.1.json'
		self._epi_code = epi_code
		self._count_table = defaultdict(int)

		self.set_corpus()

	def clean_line(self, line):
		# remove punctuation
		line = line.translate(str.maketrans('', '', string.punctuation))
		# to lower case
		line = line.lower()
		# remove nl character
		line = line.replace("\n", "")
		return line

	def transliterate_line(self, line, g2p_dict, epi):
		line = self.clean_line(line)
		# transliterate g2p using dict with epitran as fallback
		line_phonetic = []
		for word in line.split():
			word_phonetic = g2p_dict.get(word, epi.transliterate(word))
			line_phonetic.append(word_phonetic)
		return line_phonetic

	def set_corpus(self):
		with open(self._file, 'r') as text, \
			open(self._dict_file, 'r') as g2p_file:
			g2p_dict = json.load(g2p_file)
			g2p_dict = {k.lower():v for k,v in g2p_dict.items()}
			epi = Epitran(self._epi_code)

			for line in text:
				line_phonetic = self.transliterate_line(line, g2p_dict, epi)
				for word in line_phonetic:
					self._count_table[word] += 1

	def get_data_stream(self, min_count=1, min_length=1):
		with open(self._file, 'r') as text, \
			open(self._dict_file, 'r') as g2p_file:
			g2p_dict = json.load(g2p_file)
			g2p_dict = {k.lower():v for k,v in g2p_dict.items()}
			epi = Epitran(self._epi_code)

			for line in text:
				list_phonetic_words = self.transliterate_line(line, g2p_dict, epi)
				if (self.validate_line(list_phonetic_words, min_count, min_length)):
					yield (list_phonetic_words)

	def	validate_line(self, list_words, min_count=1, min_length=1):
		if (len(list_words) < min_length):
			return False
		if (any([self._count_table[word] < min_count for word in list_words])):
			return False
		if (any([c.isdigit() for c in " ".join(list_words)])):
			return False
		return True

	def get_vocab(self, min_count=1, min_length=1):
		vocab = set()
		for line in self.get_data_stream(min_count, min_length):
			vocab.update(line)
		return vocab

	def print_vocab(self, min_count=1, min_length=1):
		print ()
		print(sorted(self.get_vocab(min_count, min_length)))

	def print_corpus(self, min_count=1, min_length=1):
		print ()
		for line in self.get_data_stream(min_count, min_length):
			print (" ".join(line))

class NGram_LM:

	def __init__(self, corpus, min_count=1, min_length=1, order=1):
		self._corpus = corpus
		self._order = order
		self._count_table = dict()
		self._prob_table = dict()

		self.count_ngrams(min_count, min_length)
		self.make_prob_table()

	def preprocess_line(self, line):
		return (tuple("<BoS>" * self._order) +
				tuple([c for c in line]) +
				tuple("<EoS>"))

	def count_ngrams(self, min_count, min_length):
		for line in self._corpus.get_data_stream(
								min_count=min_count, min_length=min_length):
			line = self.preprocess_line(line)
			for i in range(len(line) - self._order):
				phoneme = line[i + self._order]
				ngram = line[i:i + self._order]
				if (ngram in self._count_table):
					if (phoneme in self._count_table[ngram]):
						self._count_table[ngram][phoneme] += 1
					else:
						self._count_table[ngram][phoneme] = 1
				else:
					self._count_table[ngram] = {phoneme: 1}

	def make_prob_table(self):
		self._prob_table = self._count_table

		for ngram, countdict in self._count_table.items():
			ngram_count = sum([count for count in countdict.values()])
			for word, count in countdict.items():
				self._prob_table[ngram][word] = count / ngram_count

def main():
	# parsing of input flags
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbose", nargs='?', const=1, type=int,
		help="output additional information")
	parser.add_argument("-c", "--count", type=int, default=1,
		help="Prune sentences with words that occur less than COUNT times in corpus.")
	parser.add_argument("-l", "--length", type=int, default=1,
		help="Prune sentences that have fewer than LENGTH words.")
	parser.add_argument("file", type=str,
        help="input file used as training data")
	args = parser.parse_args()

	# Init language model
	corp = Corpus(args.file, "nld-Latn")

	# Output corpus info if verbose
	if (args.verbose):
		print("\nWithout pruning:")
		print("Sentences: {}\nUnique words: {}" \
				.format(len([line for line in corp.get_data_stream()]),
						len(corp.get_vocab())))

	# Output corpus info if verbose
	if (args.verbose):
		print("\nWith pruning:")
		print("Sentences: {}\nUnique words: {}" \
				.format(len([line for line in corp.get_data_stream(
							min_count=args.count, min_length=args.length)]),
						len(corp.get_vocab(
							min_count=args.count, min_length=args.length))))

	# corp.print_corpus(min_count=args.count, min_length=args.length)
	# corp.print_vocab(min_count=args.count, min_length=args.length)

	ngram = NGram_LM(corp, min_count=args.count, min_length=args.length)

if __name__ == "__main__":
	main()
