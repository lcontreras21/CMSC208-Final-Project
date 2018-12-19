'''
Luis Contreras-Orendain
CMSC 208 - Final Project

>>> import time
>>> start = time.process_time()

#Read in data
>>> mydata = read_data()

#Preprocess it: No capital letters and no punctuation.
#>>> processed_data = preprocess(mydata)
#>>> len(processed_data)

# getting bigram and unigram counts
#>>> bigrams = faster_creation(get_bigrams, processed_data, 10000)
#>>> unigrams = get_unigrams(processed_data)

### To retrain the model, uncomment the next 6 inputs.
# building the model
#>>> model = bigram_model(faster_creation(get_bigrams, preprocess(mydata), 10000), get_unigrams(preprocess(mydata)))

# writing the dictionary into a json file so that it doesnt take a minute to generate sentences each time.
#>>> f = open('model.txt', 'w')
#>>> f.write(str(model))
#>>> f.close()

### The above are testing the individual components
# This brings it all together and makes it easier to retrain the model as well as input it into the file.
#>>> retrain_model(mydata)

>>> f = open('model.txt').read()
>>> model = ast.literal_eval(f)

#>>> gls = generate_likely_sentence(model, "harry", 50)
#>>> gls

#>>> model = {('strange', 'just'): 0.007936507936507936, ('winky', 'remained'): 0.006711409395973154, ('at', 'uncle'): 0.0011547344110854503, ('temper', 'perhaps'): 0.018518518518518517, ('stay', 'at'): 0.06363636363636363, ('SB', 'fifth'): 4.444493827709197e-05, ('lockhart', 'speaking'): 0.0048543689320388345, ('buckbeak', 'resumed'): 0.010309278350515464}

>>> generate_random_sentence(model, 20)

#>>> generate_random_sentence(model)

#>>> generate_random_sentence(model)

#>>> generate_random_sentence(model)

#>>> generate_random_sentence(model)

#>>> generate_random_sentence(model)

>>> end = time.process_time()
>>> print(end-start)


# read in data
'''

import random
import ast
import sys
import re
# reading in the files as a list of words and combining them into fdata
def read_data():
	fdata = []
	path = "harry_potter_texts/harry_potter_"
	files = [1,2,3,4,5,6,7]
	for i in files:
		f = open(path+str(i),"r", encoding="utf-8").read()
		f = re.sub('([,();{}:-])',r' \1 ', f)
		f = re.sub('(["])',r' \1 ', f)
		f = re.sub('\s{2,}', ' ', f)
		f = f.split()
		fdata += f
	return fdata

# Preprocessing the data

def preprocess(data):
	processed_data = []
	for word in data:
		if word not in [",", "-", "'", '"',":", ";", "{", "}", "(", ")"]:
			check_punctuation = (".", "?", "!", "..")
			if word.endswith(check_punctuation):
				# special case for mr ms and mrs
				if word[-1] == "." and word.lower()[:2] == "mr" or word.lower()[:2] == "ms":
					processed_data.append(word.lower())
				# removing end punctuation and inserting sentence boundary
				else:
					if word[-1] in [".","?","!"]:
						processed_data.append(word.lower()[:-1])
						processed_data.append("SB")
					else:
						processed_data.append(word.lower()[:-2])
						processed_data.append("SB")
			else:
				processed_data.append(word.lower())
	return processed_data
	
# it takes a lot of time to process the functions. Split up the work.
def faster_creation(function, data, increment):
	remainder = len(data) % increment
	even_data = data[:len(data) - remainder]
	
	output_dict = {}
	old_index = 0
	original_increment = increment
	while len(even_data) >= increment:
		slice = function(even_data[old_index:increment])
		output_dict = { k: output_dict.get(k, 0) + slice.get(k, 0) for k in set(output_dict) | set(slice) }
		old_index = increment - 1
		increment += original_increment
	
	slice = function(data[-remainder - 1:])
	output_dict = { k: output_dict.get(k, 0) + slice.get(k, 0) for k in set(output_dict) | set(slice) }
	return output_dict

## returns a dictionary of unique bigram pairs and their count
def get_bigrams(data):
	copy_data = data
	bigrams = {}
	while len(copy_data) >= 2:
		bigram = (copy_data[0], copy_data[1])

		# if the current bigram is in the dict, add 1 to its count
		# otherwise make a new entry and set its value to 1
		if bigram in bigrams:
			bigrams[bigram] += 1
			copy_data = copy_data[1:]
		else:
			bigrams[bigram] = 1
			copy_data = copy_data[1:]
	return bigrams

## returns a dictionary of unique words and their count
def get_unigrams(data):
	unigrams = {}
	# do similar process as getting the bigrams
	for word in data:
		if word not in unigrams:
			unigrams[word] = 1
		else:
			unigrams[word] += 1
	return unigrams

## returns the two dictionaries containing bigram and unigram information
def get_counts(data):
	return get_bigrams(data), get_unigrams(data)

## building the bigram model
## returns a dictionary containing each bigram and its probability
def bigram_model(bigrams, unigrams):
	model = {}
	for bigram in bigrams:
		unigram_count = unigrams[bigram[0]]
		model[bigram] = bigrams[bigram] / unigram_count
	return model
	
def retrain_model(data):
	model = bigram_model(faster_creation(get_bigrams, preprocess(data), 10000), get_unigrams(preprocess(data)))
	f = open('model.txt', 'w')
	f.write(str(model))
	f.close()
	
	
## Building sentences based on the most likely word to come next
def find_max_bigram(model, word):
	possible_bigram = {}
	for bigram in model:
		if bigram[0] == word:
			possible_bigram[bigram] = model[bigram]
	
	vals = list(possible_bigram.values())
	keys = list(possible_bigram.keys())
	return keys[vals.index(max(vals))]	

def generate_likely_sentence(model, starting_word, length):
	#Given a model and a length that is at least greater than 2, it will give back the most likely sentece based on a given starting word.
	copy_model = model #Copying just in case
	
	sentence_list = [starting_word]
	count = 0
	while count < length:
		#Find the bigram with the highest probability given the first word.
		max_bigram = find_max_bigram(copy_model, sentence_list[-1])
		sentence_list += [max_bigram[1]]
		
		copy_model.pop(max_bigram)
		count += 1
	return sentence_list
	
## building sentences based on random selection
def find_all_similar_bigrams(model, word):
	possible_bigram = {}
	for bigram in model:
		if bigram[0] == word:
			possible_bigram[bigram] = model[bigram]
	
	vals = list(possible_bigram.values())
	keys = list(possible_bigram.keys())
	return keys

def generate_random_sentence(model, length):
	copy_model = model
	
	sentence_list = ["reaplce this"]
	account_first_word = False
	count = 0
	limit = 0
	while sentence_list[-1] != "SB" and count < length and limit < length:
		if not account_first_word:
			account_first_word = True
			sentence_list = []
		###
		# to pick the next word
		# 1. pick a word at random
		# 2. form the bigram from that word and the previous word
		# 3. find the probability of that bigram
		# 4. if that probability is smaller than a random number between 0 and 1, we keep that word. Otherwise, start over.
		###
		
		if len(sentence_list) == 0:
			all_possible_bigram_keys = list(model.keys())
		else:
			all_possible_bigram_keys = find_all_similar_bigrams(model, sentence_list[-1])
		
		found_next_word = False
		while not found_next_word:
			max_prob = random.random()
			next_bigram = random.choice(all_possible_bigram_keys)	
			if model[next_bigram] <= max_prob:
				sentence_list.append(next_bigram[1])
				found_next_word = True
				count += 1
			limit += 1
	sentence = ' '.join(word for word in sentence_list[1:])
	sentence = sentence.replace("SB", ".")
	return sentence


def _test():
		import doctest
		result = doctest.testmod()
		print("Result of doctest for lang_model is:", result[0])
		if result[0] == 0:
			print("Wahoo! Passed all", result[1], "tests!")
		else:
			 print("Rats!")
_test()
