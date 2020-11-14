import string
from epitran import Epitran

def get_corpus(path, epi):
	corpus_sentences = []
	corpus_words = []

	with open(path, 'r') as text:
		lines = text.readlines()

		for line in lines:
			# remove punctuation
			line_nop = line.translate(str.maketrans('', '', string.punctuation)).replace("\n", "")
			# transliterate g2p
			line_phonetic = epi.transliterate(line_nop)

			# add sentences and words to corpus
			corpus_sentences.append(line_phonetic)
			for word in line_phonetic.split(" "):
				corpus_words.append(word)

	return corpus_sentences, corpus_words

def main():
	epi = Epitran("nld-Latn")

	sentences, words = get_corpus("datasets/sample_sentences.txt", epi)

	# Check corpus sizes
	print("Sentences:")
	print(len(set(sentences)))
	print("Words:")
	print(len(set(words)))

if __name__ == "__main__":
	main()
