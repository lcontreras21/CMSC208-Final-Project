'''
Luis Contreras-Orendain
CMSC 208 - Final Project

>>> import time
>>> start = time.process_time()

#Read in data
>>> mydata = read_data()

#Preprocess it: No capital letters and no punctuation.
>>> processed_data = preprocess(mydata)
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

>>> f = io.open("model.txt", "r", encoding='utf-8')
>>> f = f.read()
>>> model = ast.literal_eval(f)

#>>> gls = generate_likely_sentence(model, 50)
#>>> gls

#>>> generate_random_sentence(model)

>>> easy_probability(model, "harry potter")

>>> smoothed_probability(processed_data, "What is the meaning of this.")

>>> end = time.process_time()
>>> print(end-start)


# read in data
'''
import random
import ast
import sys
import re
import io
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
		f = f.replace("...", "")
		f = f.replace("..", "")
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
	even_data = data[:len(data) - remainder] # work with even chunks
	
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

## building the bigram model
## returns a dictionary containing each bigram and its probability
def bigram_model(bigrams, unigrams):
	model = {}
	for bigram in bigrams: 
		model[bigram] = bigrams[bigram] / unigrams[bigram[0]]
	return model

import codecs
def retrain_model(data):
	model = bigram_model(faster_creation(get_bigrams, preprocess(data), 10000), get_unigrams(preprocess(data)))
	f = io.open('model.txt', 'w', encoding='utf-8')
	#modelutf8 = str(model).encode('UTF-8')
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

## building sentences based on random selection
def generate_likely_sentence(model, length):
	#Given a model and a length that is at least greater than 2, it will give back the most likely sentece based on a given starting word.
	copy_model = model #Copying just in case
	
	sentence_list = [random.choice(list(model.keys()))[0]]
	count = 0
	while count < length:
		#Find the bigram with the highest probability given the first word.
		max_bigram = find_max_bigram(copy_model, sentence_list[-1])
		sentence_list += [max_bigram[1]]
		copy_model.pop(max_bigram)
		count += 1
	sentence = ' '.join(word for word in sentence_list[1:])
	return sentence
	
def find_all_similar_bigrams(model, word):
	possible_bigrams = []
	for bigram in model:
		if bigram[0] == word:
			possible_bigrams.append(bigram)
	return possible_bigrams

def generate_random_sentence(model):
	sentence_list = [random.choice(list(model.keys()))[0]]
	while sentence_list[-1] != "SB":
		try:
			next_bigram = random.choice(find_all_similar_bigrams(model, sentence_list[-1]))
			max_prob = random.random()
			if model[next_bigram] < max_prob:
				sentence_list.append(next_bigram[1])
			else:
				raise Exception
		except:
			next_bigram = random.choice(list(model.keys()))
			if model[next_bigram] < max_prob:
				sentence_list.append(next_bigram[1])
			else:
				pass
	sentence = ' '.join(word for word in sentence_list[1:])
	sentence = sentence[:-3].capitalize() + "."
	return sentence

### Generating sentence probability
### Assuming all words are in the corpus
def easy_probability(model, sentence):
	sentence_list = preprocess(sentence.split())
	sentence_bigrams = get_bigrams(sentence_list)
	probability = 1
	current_bigram = ()
	for bigram in sentence_bigrams:
		current_bigram = bigram
		probability *= model[bigram]
	return probability

### harder way to factor probability using data smoothing to account for unknown words.
def smoothed_probability(data, sentence):
	combined_data = data + ["SB"] +  preprocess(sentence.split())
	# retrain the model to account for bigrams in sentence
	model_bigrams = faster_creation(get_bigrams, combined_data, 10000)
	# add 1 to all bigram counts
	for bigram in model_bigrams:
		model_bigrams[bigram] += 1
	model_unigrams = get_unigrams(combined_data)
	# add the number of words in vocabulary to the unigram counts
	for unigram in model_unigrams:
			model_unigrams[unigram] += len(model_unigrams)
	# make model using the new counts

	return easy_probability(bigram_model(model_bigrams, model_unigrams), sentence)




def _test():
		import doctest
		result = doctest.testmod()
		print("Result of doctest for lang_model is:", result[0])
		if result[0] == 0:
			print("Wahoo! Passed all", result[1], "tests!")
		else:
			 print("Rats!")
_test()
