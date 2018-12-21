Final Project for CMSC 208Speech Synthesis and Recognition

A binary language model based on all the Harry Potter books. It will then create sentences based on that model and assess the probability of a sentence being from the HP series.

The model should already be generated in the text file. The program can then be rerun to generate more random sentences, on average 6 seconds per sentence. Some example generated sentences can be found in the 'generated_sentences.txt' file.

The program will take generate words based on either highest probability or on random chance given the previous word. The sentences that were created varied in length, from a few words to more than twenty. The random generator will keep adding words to the sentence until it reaches a sentence boundary as opposed to a word limit. 

I did not have time to have users evaluate the generated sentences. In my opinion, my sentence generation requires a lot more work. Implementing a length cutoff or having it be less on chance and more on the probability of the bigrams themselves. Another possible implementation is doing this in trigrams or 4-gram, which would create better sentences. 

To find the probability of a sentence, there are two functions. One is an easy one because all the words are already in the corpus and are probably already likely bigrams. In the event they are not in the corpus or are not bigrams, we use the seconds probability function that will apply Laplace Smoothing and shift some of the probability onto the newer bigrams. 

The model is stored in a separate text file that is read from when calculating probability or generating sentences. There is an encoding error where there are hexadecimal characters in the string caused by encoding the information to the file. Storing the information in the file is necessary in order to have the program run for a minute, and then be able to generate sentences without regenerating the model. 