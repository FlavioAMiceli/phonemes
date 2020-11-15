import argparse
import string
from epitran import Epitran
from collections import defaultdict

def get_corpus(path, epi):
	corpus_sentences = []

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
			# add sentence to corpus
			corpus_sentences.append(line_phonetic)

	return corpus_sentences

def rm_lines_with_rare_words(lines, min_count=1):
	# get word count in corpus
	count = defaultdict(int)
	for line in lines:
		for word in line.split():
			count[word] += 1
	# store lines that do not contain rare words
	sentences = []
	for line in lines:
		add = True
		for word in line.split():
			if count[word] < min_count:
				add = False
				break
		if (add):
			sentences.append(line)
	return (sentences)

def rm_short_lines(lines, min_length=1):
	sentences = []
	for line in lines:
		if (len(line.split()) >= min_length):
			sentences.append(line)
	return (sentences)

def main():
	# parsing of input flags
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2, 3, 4],
					help="output additional information")
	parser.add_argument("-c", "--count", type=int,
					help="Prune sentences with words that occur less than n times in corpus.")
	parser.add_argument("-l", "--length", type=int,
					help="Prune sentences with less than n words.")
	parser.add_argument("file", type=str,
                    help="input file used as training data")
	args = parser.parse_args()

	# Transliterating the corpus
	epi = Epitran("nld-Latn")
	sentences = get_corpus(args.file, epi)

	# Output corpus info if verbose
	if (args.verbosity >= 2):
		words = set()
		for line in sentences:
			words.update(line.split())
		print("\nBefore pruning:")
		print("Sentences: {}\nUnique words: {}" \
								.format(len(set(sentences)), len(words)))

	# Prune sentences
	if (args.count):
		sentences = rm_lines_with_rare_words(sentences, args.count)
	if (args.length):
		sentences = rm_short_lines(sentences, args.length)

	if (args.count or args.length):
		# build new word corpus
		words = set()
		for line in sentences:
			words.update(line.split())

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
