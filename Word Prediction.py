import re
from collections import Counter
from collections import OrderedDict
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import time
import sys

mod_big = []
file_data = []
occurances = []
frequency_list = []
final_list = []
words = []

#List of all the words in 'big.txt' seperated by a comma
def word(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(word((open("big.txt").read())))

#Adds the current, previous, & next words to the mod_big list
def modified_big(text):
    big = re.findall(r'\w+', text.lower())
    for i in range(len(big) - 1):
        curr = big[i]
        prev = big[i-1]
        nxt = big[i+1]
        mod_big.insert(i,[prev, curr, nxt])
    return mod_big

#Returns the list with the highest freqency
def most_frequent():
    most_freq = final_list[0][3]
    for i in range(len(final_list) - 1):
        if(final_list[i][3] > most_freq):
            most_freq = final_list[i][3]
    for i in range(len(final_list) - 1):
        if(final_list[i][3] == most_freq):
            return final_list[i]

#Finds number of times the word occurs in 'big.txt'
def occurance(word):
    for i in range(len(mod_big) - 1):
        if(mod_big[i][1] == word):
            occurances.append(mod_big[i])

#Finds the number of times the same pair exists in 'big.txt' (previous, next)
def count_occurances(prev_next):
    counter = 0
    for i in range(len(occurances) - 1):
        if(occurances[i][0] == prev_next[0] and occurances[i][2] == prev_next[1]):
            counter = counter + 1
    return counter

#Calculates if the same previous and next it will increment the counter until 'eof' state. Adds the number to the pair list
def frequency(word):
    occurance(word)
    for i in range(len(occurances) - 1):
        if(occurances[i][1] == word):
            frequency = count_occurances([occurances[i][0], occurances[i][2]])
            frequency_list.append([occurances[i][0], occurances[i][1], occurances[i][2], frequency])
        remove_duplicates(frequency_list)

#Removes the duplicates from the freqency list, storing them into final_list
def remove_duplicates(x):
    for i in x:
        if i not in final_list:
            final_list.append(i)

if __name__ == '__main__':
    modified_big(open('big.txt').read())
    temp = []
    print("Enter a line of text. Type 'quit' to quit the program after a line.")
    for line in sys.stdin:
        words = word_tokenize(line)
        if words[0] != "quit":
            previous_word = words[len(words) - 2]
            current_word = words[len(words) - 1]
            frequency(current_word)
            temp = most_frequent()
            print(line + temp[2])
            words.clear()
        else:
            break