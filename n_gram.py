from collections import defaultdict

class CORPUS:

	def __init__(self, path, epi):
		self._count_table = defaultdict(int)
		self._corpus = list()
		self._vocab = set()

		self.set_corpus(path, epi)
		self.update_count_table()


	# TODO: use a generator to yield lines
	def set_corpus(self, path, epi_code, use_dict=True):
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
			open('g2p_dictionary/dutch_dic_to_phonetic.1.json', 'r') as g2p_file:
			lines = text.readlines()
			g2p_dict = json.load(g2p_file)
			g2p_dict = {k.lower():v for k,v in g2p_dict.items()}
			epi = Epitran(epi_code)

			for line in lines:
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
		# Update count table
		self._count_table = defaultdict(int)
		for line in self._corpus:
			for word in line.split():
				self._count_table[word] += 1

		# Update vocab
		self._vocab = set(self._count_table.keys())

	def rm_lines_with_rare_words(self, min_count=1):

		# store lines that do not contain rare words
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
		print(self._vocab)

def main():
	# parsing of input flags
	import argparse
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

	# Init language model
	corp = CORPUS(args.file, "nld-Latn")

	# Output corpus info if verbose
	if (args.verbose):
		print("\nBefore pruning:")
		print("Sentences: {}\nUnique words: {}" \
				.format(len(corp._corpus), len(corp._vocab)))

	# Prune sentences
	if (args.count):
		corp.rm_lines_with_rare_words(args.count)
	if (args.length):
		corp.rm_short_lines(args.length)

	# Output corpus info if verbose
	if (args.verbose):
		print("\nAfter pruning:")
		print("Sentences: {}\nUnique words: {}" \
				.format(len(corp._corpus), len(corp._vocab)))

	# corp.print_corpus()
	# corp.print_vocab()

if __name__ == "__main__":
	main()
