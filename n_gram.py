from collections import defaultdict

class Corpus:

	def __init__(self, path, epi):
		self._count_table = defaultdict(int)
		self._corpus = list()
		self._vocab = set()

		self.set_corpus(path, epi)
		self.update_count_table()

	def set_corpus(self,
			path, epi_code, dict_path='g2p_dictionary/dutch_dic_to_phonetic.1.json'):
		def clean_line(line):
			import string

			# remove digits
			line = line.translate(str.maketrans('', '', string.digits))
			# remove punctuation
			line = line.translate(str.maketrans('', '', string.punctuation))
			# to lower case
			line = line.lower()
			# remove nl character
			line = line.replace("\n", "")
			return line

		import json
		from epitran import Epitran
		with open(path, 'r') as text, \
			open(dict_path, 'r') as g2p_file:
			g2p_dict = json.load(g2p_file)
			g2p_dict = {k.lower():v for k,v in g2p_dict.items()}
			epi = Epitran(epi_code)

			for line in text:
				line = clean_line(line)
				# transliterate g2p using dict with epitran as fallback
				if (use_dict):
					line_phonetic = []
					for word in line.split():
						word_phonetic = g2p_dict.get(word, epi.transliterate(word))
						line_phonetic.append(word_phonetic)
					self._corpus.append(" ".join(line_phonetic))
				# transliterate using epitran
				else:
					line_phonetic = epi.transliterate(line)
					self._corpus.append(line_phonetic)

	def update_count_table(self):
		# Go through corpus line by line. Add occurences of each word to table.
		self._count_table = defaultdict(int)
		for line in self._corpus:
			for word in line.split():
				self._count_table[word] += 1

		self._vocab = set(self._count_table.keys())

	def prune_corpus(self, min_count=1, min_length=1):
		if (min_count > 1):
			self.rm_lines_with_rare_words(min_count)
		if (min_length > 1):
			self.rm_short_lines(min_length)

	def rm_lines_with_rare_words(self, min_count=1):
		# Store each line in corpus where every word occurs at least min_count times
		# in the original corpus.
		self._corpus = [line for line in self._corpus if \
			all([self._count_table[word] >= min_count for word in line.split()])]
		self.update_count_table()

	def rm_short_lines(self, min_length=1):
		self._corpus = \
			[line for line in self._corpus if len(line.split()) >= min_length]
		self.update_count_table()

	def print_corpus(self):
		for line in self._corpus:
			print (line)

	def print_vocab(self):
		print(sorted(self._vocab))

class NGram_LM:

	def __init__(self, order):
		self._order = order
		self._count_table = dict()
		self._prob_table = dict()

	def preprocess_sentence(self, text):
		for line in text:
			yield [c for c in line]

	def preprocess_history(self, history):
		# Used to select the end of a longer sentence, or pad the start of a
		# sentence with <s> tokens
		if (len(history) == self._order):
            return (tuple(history))
		elif (len(history) > self._order):
            return (tuple(history[len(history) - self._order:length]))
		else:
            missing = self._order - len(history)
            return (tuple(['<s>'] * missing) + tuple(history))

	def count_ngrams(self, text):
		for line in text:
			for i in range(len(line)):
				phoneme = line[i]
				ngram = self.preprocess_history(line[:i])
				if ngram in self._count_table:
					if phoneme in self._count_table[ngram]:
                        self._count_table[ngram][phoneme] += 1
                    else:
                        self._count_table[ngram][phoneme] = 1
				else:
                    self._count_table[ngram] = {phoneme: 1}

	def set_prob_table(self):
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
		print("\nBefore pruning:")
		print("Sentences: {}\nUnique words: {}" \
				.format(len(corp._corpus), len(corp._vocab)))

	# Prune sentences
	corp.prune_corpus(min_count=args.count, min_length=args.length)

	# Output corpus info if verbose
	if (args.verbose):
		print("\nAfter pruning:")
		print("Sentences: {}\nUnique words: {}" \
				.format(len(corp._corpus), len(corp._vocab)))

	# corp.print_corpus()
	# corp.print_vocab()

if __name__ == "__main__":
	main()
