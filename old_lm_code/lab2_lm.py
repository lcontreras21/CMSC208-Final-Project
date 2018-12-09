'''
 Test Suite
# CMSC/LING 208 Lab 2
# Name: Luis Contreras-Orendain

#Read in data
>>> mydata = open('hamlet.txt', 'r').read().split()

#Preprocess it: No capital letters and no punctuation.
>>> processedData = preprocess(mydata)

#Get_counts for bigrams and trigrams
>>> bigrams = getBigrams(processedData)
>>> unigrams = getUnigrams(processedData)
>>> assert(len(unigrams) < len(bigrams)) #There should be a lot more bigrams because it is using nearly every word twice to make the bigrams.

>>> bigrams2, unigrams2 = get_counts(processedData) 
>>> assert(bigrams == bigrams2)
>>> assert(unigrams == unigrams2)

>>> bigramModel = bigram_model(processedData)
>>> print(bigramModel[('of', 'denmarke')]) #There were only 8 of this bigram in the text. Looks reasonable.
0.013114754098360656

>>> prob = get_sentence_probability(bigramModel, ["of", "denmarke"])
>>> prob
0.013114754098360656

##Inputting the sentence probability of a bigram should give us the probability of that bigram from the model.

>>> prob2 = get_sentence_probability(bigramModel, ["prince", "of", "denmarke"])
>>> prob2
0.004371584699453552

##This probability should be lower than that of "of denmarke"
'''
# read in your chosen corpus as a list of words (change the file name if you're using a different corpus)
mydata = open('hamlet.txt','r').read().split()

# Part 1: Preprocessing

def preprocess(data):
	processedData = []
	for word in data:
		if word not in [",", "-", "\"", "\'", ".", "!",":", ";", "...", "?", "{", "}", "[", "]"]:
			processedData.append(word.lower())
	return processedData

# Part 2: Get bigram and unigram counts

##Helper functions to get counts
def getBigrams(data):

	copyData = data
	bigrams = {}
	while len(copyData) >= 2:
		#Make the bigram at that location.
		bigram = (copyData[0], copyData[1])
		
		#If bigram is in the dict, add 1 to its count. Else, make an entry and set it to 1.
		if bigram in bigrams:
			bigrams[bigram] += 1
			copyData = copyData[1:]
		else:
			bigrams[bigram] = 1
			copyData = copyData[1:]
	return bigrams
	
def getUnigrams(data):
	unigram = {}
	#Iterate through the list, if its in dict, add one to it and if its not, then add it to the dict. Easier than finding bigrams.
	for word in data:
		if word not in unigram:
			unigram[word] = 1
		else:
			unigram[word] += 1
	return unigram

def get_counts(data):
   bigrams = {}
   unigrams = {}
   
   #Going to use two helper functions. One is going to look for bigrams, and 1 is going for unigrams.
   
   bigrams = getBigrams(data)
   unigrams = getUnigrams(data)

   return bigrams,unigrams


# Part 3: Build the bigram model

def bigram_model(data):
	bigrams,unigrams = get_counts(data)
	model = {}
	
	for bigram in bigrams:
		unigramCount = unigrams[bigram[0]]
		probability = bigrams[bigram] / unigramCount
		
		model[bigram] = probability
	
	return model


# Part 4: Use your model to get a sentence probability
def get_sentence_probability(model,sentence):
	#sentence takes a list as a parameter
	prob = 1
	
	#Then find the bigrams.
	bigrams = getBigrams(sentence)
	
	#Find the probability of those bigrams being in that order.
	
	for bigram in bigrams:
		prob = prob * model[bigram]
	return prob


# Test run
# update this variable with a test sentence for your model
sentence_to_test = 'hamlet lord of denmarke shall rule till the end of time'

def demo(corpus, testsentence):
	processed = preprocess(corpus)
	print("processed the data")
	mymodel = bigram_model(processed)
	print("built the model")
	#If we run into the case where the bigram in the sentence is not in the model, we have to update it.
	#We add it as having a count of 1 in the corpus and divide by the number of unigrams given by the first word in the bigram plus one.
   
	#First process the testsentence
	testsentencelist = testsentence.lower().split()
	#Get sentence bigrams and corpus unigrams.
	testSentenceBigrams = getBigrams(testsentencelist)
	corpusUnigrams = getUnigrams(processed)
	printTrue = False
	for bigram in testSentenceBigrams:
		if bigram not in mymodel:
			if printTrue == False:
				print("Retraining model")
				printTrue = True
			#update model if bigram not in model
			mymodel[bigram] = 1 / (corpusUnigrams[bigram[0]] + 1)
	
	print("The probability of this sentence is:")
	print(get_sentence_probability(mymodel,testsentencelist))
	
	

###Extra Credit Portion of the Lab 	
	
	
	
def findMaxBigram(model, word):
	possibleBigram = {}
	for bigram in model:
		if bigram[0] == word:
			possibleBigram[bigram] = model[bigram]
	
	vals = list(possibleBigram.values())
	keys = list(possibleBigram.keys())
	return keys[vals.index(max(vals))]
	
def generateSentence(model, length, startingWord):
	#Given a model and a length that is at least greater than 2, it will give back the most likely sentece based on a given starting word.
	copyModel = model #Copying just in case
	
	sentenceList = [startingWord]
	count = 0
	while count < length:
		#Find the bigram with the highest probability given the first word.
		maxBigram = findMaxBigram(copyModel, sentenceList[-1])
		sentenceList += [maxBigram[1]]
		
		copyModel.pop(maxBigram)
		
		
		count += 1
	return sentenceList
	
	
	
def _test():
	import doctest
	result = doctest.testmod()
	print("Result of doctest for Lab2Starter is:", result[0])
	if result[0] == 0:
		print("Wahoo! Passed all", result[1], "tests!")
	else:
		print("Rats!")
   
   
if __name__ == "__main__":
	_test()
	demo(mydata,sentence_to_test)
	print(generateSentence(bigram_model(preprocess(mydata)), 10, "the"))
	


