# a3

## Part I
#### Posterior Probability
We calculate the sum of the pos and words and normalize it. We calculate the posterior probability using the emission probability for bayes net. 
For the bayes net we calculate the probability using the emission probability.
For the viterbi algoritm we use emission probabilty and transition probabilty to calculate the posterior probability.
For the Gibbs sampling we calculate the probability using the emission, transions probabilty and using the POS count which has been normalzied for the training data.
If the word pos is not there then we chose a constant using the minimum possible product. We sum up these probabilities and return for the respective model.

#### Bayes Net
We calculated the Bayes net probability and stored it in a dictionary. We stored probability for each word and stored all the possible POS's of the word and normalize them for each of the words. If the testing label exists in the training dictionary, we use the most probable POS from the training data. Else we consider it as a foreign word( 'x' ).
##### Emission Probability
The emission probability of each word and stored it in a dictionary with a tuple of word and pos as key and its probability as the value which again is normalized for each word. 
##### Transition Probability
The transition probability is calculated for 12 x 12 POS. It has a tuple of previous_pos and current_pos as keys and its count as values. Later the count is normalized using the total counts.
##### Initial Probability
The initial probability distribution for the first words using their POS. It is again normalized for the first word and used as it is.
#### Viterbi
We store the respective combinations of initial distribution and emission probability for the first word. For all the next words we calculate the respective products of emission probability, previous probability and transition probability. While iterating through all the 12 POS we consider the pos with the maximum probability. We append this value to the current distribution. We append such values for all 12 POS up to the length of the sentence.
While calculating the probability for the first POS, if the word doesn't exist we append the most frequent first character in the initial probability.
While iterating through the second word if we don't find any combination of a word with all of the 12 pos, only then we consider the exception case of using the transition probability, previous probability and a scaling constant because of not having an emission probability.   
Backtracking
For the last word, we chose the maximum probability for all the 12 POS. After choosing this POS we backtrack from the last word and use the maximum transition probability for that POS.
For backtracking, if we don't find a combination of word and pos in the current distribution we consider the transition probability as an alternative.
Then we reverse the list because the list was appended in the reverse format and return it.
##### MCMC
For Gibbs sampling, we store the emission probabilities for the 12 POS. If the POS doesn't exist we replace it with a downscaled value among all the minimum values.
Then we randomly iterate for 1000 times and based on a range of probability it lies in. We do this for all the words in the sentence. Then we store the last of all the POS and return it.

Handling all the exceptions whenever the testing data had some new words or the length of sentence was exceptionally small was another challenege.This program in particularly required a lot of dictioneries to be maintained. 

## Part II

Codebreaking
Metropolis-Hastings algorithm is a Markov chain Monte Carlo method of random sampling from a probability distribution where there are millions of combinations, and hence direct sampling is difficult.

In Code Breaking problem, we are provided with a message, that is encrypted using two techniques, replacement and rearrangement. To decipher this, we are provided with training data, which is a corpus of more than 700,000 English words. For a given sentence, we score it how closely it resembles the English language. We trained our model using this corpus and counted the number of times a pair of words occurred. More the number of times a sequence is encountered, more is the probability of it appearing in the text. The scoring dictionary keeps the count of two consecutive alphabets along with the spaces. Taking spaces along with the words signifies which letter has the most probability of being the first letter. The scoring is done for each combination of pair appearing in the decrypted text, multiplied by the number of times it has appeared. We have used logarithmic while adding up the score because the probability values, when multiplied, tends to 0.
After constructing the scoring dictionary, we tackle the task of decrypting the code.

The decipher key is a randomly initialized mapping of alphabets. This key is used to map each alphabet and produce a new text. The next part is to rearrange the text by rearranging every 4 characters of the text. This decrypted text is then scored using the scoring dictionary and a reference score is generated (PD).
The new deciphering key is generated by swapping any two random keys of the dictionary. The above steps are repeated and a new score (PD dash) is produced. If the new score is greater than the original score, then the decipher key and arrangement key is replaced by the new decipher key and new rearrangement key. If the new score is lesser than that of the previous score, then the probability of replacing the old decipher with the new one is the ratio of new score divided by the old score. Since, we have taken the log of the number of occurrences, instead of dividing the score, the probability now is exponential of the difference of two scores.

This process goes for around 100000 iterations, and record of the highest score and its corresponding decrypted text is stored and returned as output.

It was hard to decrypt larger words with a larger number of letters.

## Part III
This part of the assignment is a supervised document classification problem where the algorithm helps in deciding whether an e-mail is a spam or not spam. This problem can be considered as a classic example of Naive Bayes Implementation. The naive Bayes implementation typically is derived from the Bayes Net Problem, keeping in mind the assumption that there exists conditional independence amongst all the observable variables. In the context of this problem, the assumption is that we consider email as a bag of words instead of considering any relation between a set of words or considering rules of grammar.

For example, if we have an email with n words, so we need to find the probability of whether the given email is a spam or not spam which is given by, P(spam | w1, w2, w3, w4, w5, …. wn). We can calculate this probability by the Naive Bayes formula as follows, 

###### P(spam | w1, w2, w3, w4, w5, …. wn)  = ( P(w1, w2, w3, w4, w5, …. Wn | Spam)  * P(spam) ) / P(word)

To describe broadly, the implementation of the problem was done in two steps, first where the training set was read, and cleaned and priori probabilities were calculated and the second step, we used the priori probabilities to calculate the posterior probabilities. We start with the training of the classifier using the training set of the email provided. We read all the spam and not spam emails separately and clean only the newline characters. We store the words in the spam and not-spam emails in two dictionaries and calculate the values of P(word|spam) and P(word|notspam). 

The interesting part of this part was cleaning of the data, which very strongly infeluenced the accuracy of this part. We did many hit and trial to get the accuracy, first, we only read the body of the email rather than reading the entire email, this resulted in a very poor accuracy (57%). Then we went on to read the complete emails, including the header and the body, and considered only alpha-numeric characters, which gave us the best accuracy (95%). But we did not go ahead ignoring the alpha-numeric, because we believe special characters can influence the probability of an email being a spam. The solution we have implemented takes in consideration everything except the newline characters. This gave us the accuracy of 91%. 

Currently the code will not run because it can't find the data in the same directory. As soon as data is added in the same directory it will run without an error.

The output of this file is a output-file.txt, which has list of emails and their corresponding type (spam / notspam). On console, we print the Accuracy in percentage.
In this part of the assignment, reading the large dataset and then generating the count of each word was a time consuming task, and to increase the efficiency, we used a counter function, which increased the speed by large amount.
