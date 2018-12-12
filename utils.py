def ngrams(sentence, n):
	return [sentence.split()[i:i+n] for i in range(0, len(sentence.split())-n+1)]


def ngram_list_to_string(ngram_list):
	return ''.join(str(i)+' ' for i in ngram_list[0:-1])+str(ngram_list[-1])

def ngram_similarity_absolute(comment, data_file_path, n):
	comment_ngrams = ngrams(comment, n)

	max_number_shared_ngrams = 0
	max_number_shared_ngrams_sentence = ""
	with open(data_file_path, "r", encoding="utf-8") as corpus_file:
		for line in corpus_file:
			number_shared_ngrams = 0
			line_ngrams = ngrams(line, n)

			for ngram in comment_ngrams:
				if ngram in line_ngrams:
					number_shared_ngrams = number_shared_ngrams + 1

			if number_shared_ngrams > max_number_shared_ngrams:
				max_number_shared_ngrams = number_shared_ngrams
				max_number_shared_ngrams_sentence = line

	return max_number_shared_ngrams, max_number_shared_ngrams_sentence


def ngram_similarity_percentage(comment, data_file_path, n):
	comment_ngrams = ngrams(comment, n)
	number_comment_ngrams = len(comment_ngrams)

	max_percentage_shared_ngrams = 0
	max_percentage_shared_ngrams_sentence = ""
	with open(data_file_path, "r", encoding="utf-8") as corpus_file:
		for line in corpus_file:
			number_shared_ngrams = 0
			line_ngrams = ngrams(line, n)
			number_line_ngrams = max(len(line_ngrams), 1)

			for ngram in comment_ngrams:
				if ngram in line_ngrams:
					number_shared_ngrams = number_shared_ngrams + 1

			percentage_shared_ngrams = number_shared_ngrams / number_line_ngrams

			if percentage_shared_ngrams > max_percentage_shared_ngrams:
				max_percentage_shared_ngrams = percentage_shared_ngrams
				max_percentage_shared_ngrams_sentence = line

	return max_percentage_shared_ngrams, max_percentage_shared_ngrams_sentence


def support(comment, data_file_path, n):
	support = {}
	comment_ngrams = ngrams(comment, n)

	for ngram in comment_ngrams:
		support[ngram_list_to_string(ngram)] = []

	with open(data_file_path, "r", encoding="utf-8") as corpus_file:
		for line in corpus_file:
			for ngram in comment_ngrams:
				if ngram_list_to_string(ngram) in line:
					support[ngram_list_to_string(ngram)].append(line)

	return support


def ngram_frequencies(comment, data_file_path, n):
	ngram_support = support(comment, data_file_path, n)
	frequencies = {}
	
	for key in ngram_support.keys():
		frequencies[key] = len(ngram_support[key])

	return frequencies