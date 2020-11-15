import argparse
import string
from epitran import Epitran
from collections import defaultdict

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
			for word in line_phonetic.split():
				corpus_words.append(word)

	return corpus_sentences, set(corpus_words)

def rm_lines_with_rare_words(lines, min_count=1):
	# get word count in corpus
	count = defaultdict(int)
	for line in lines:
		for word in line.split():
			count[word] += 1
	# prune lines with rare words
	sentences = []
	for line in lines:
		add = True
		for word in line.split():
			if count[word] < min_count:
				add = False
				break
		if (add):
			sentences.append(line)
	# build new word corpus
	words = []
	for line in sentences:
		for word in line.split():
			words.append(word)
	return (sentences, set(words))

def main():
	# parsing of input flags
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2, 3, 4],
					help="output additional information")
	parser.add_argument("-p", "--prune", type=int,
					help="Prune sentences with words that occur less than n times in corpus.")
	parser.add_argument("file", type=str,
                    help="input file used as training data")
	args = parser.parse_args()
	min_count = args.prune if args.prune else 1

	# preparing the corpus
	epi = Epitran("nld-Latn")
	sentences, words = get_corpus(args.file, epi)

	# Output corpus info if verbose
	if (args.verbosity >= 2):
		print("\nBefore pruning:")
		print("Sentences: {}\nUnique words: {}" \
								.format(len(set(sentences)), len(words)))

	# Prune sentences
	sentences, words = rm_lines_with_rare_words(sentences, min_count)

	# Output corpus info if verbose
	if (args.verbosity >= 2):
		print("\nAfter pruning:")
	if (args.verbosity >= 1):
		print("Sentences: {}\nUnique words: {}" \
								.format(len(set(sentences)), len(words)))
	if (args.verbosity == 4):
		for line in sentences:
			print(line)
	if (args.verbosity >= 3):
		print(sorted(words))

if __name__ == "__main__":
	main()
