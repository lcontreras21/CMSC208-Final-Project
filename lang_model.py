'''
Luis Contreras-Orendain
CMSC 208 - Final Project


### Test suite
>>> data = read_data()
>>> data[:100]

Preprocess data
>>> processed_data = preprocess(data)
>>> processed_data[:100]

# read in data
'''
import re
# reading in the files as a list of words and combining them into fdata
def read_data():
    fdata = []
    path = "harry_potter_texts/harry_potter_"
    files = [1,2,3,4,5,6,7]
    for i in files:
        f = open(path+str(i),"r", encoding="utf-8").read()
        f = re.sub('([,!?()])',r' \1 ', f)
        f = re.sub('\s{2,}', ' ', f)
        f = f.split()
        fdata += f
    return fdata

# Preprocessing the data

def preprocess(data):
    processed_data = []
    for word in data:
        if word not in [",", "-", "\"", "\"", ".", "!",":", ";", "...", "?", "{", "}", "[", "]"]:
            if "\"" in word:
                processed_data.append(word.lower().replace("\"", ""))
            elif "'" in word:
                processed_data.append(word.lower().replace("'", ""))
            else: 
                processed_data.append(word.lower())
    return processed_data

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
        unigrams[word] += 1
    else:
        unigrams[word] = 1
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



def _test():
        import doctest
        result = doctest.testmod()
        print("Result of doctest for lang_model is:", result[0])
        if result[0] == 0:
            print("Wahoo! Passed all", result[1], "tests!")
        else:
             print("Rats!")
_test()
