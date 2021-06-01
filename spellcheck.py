import re
from collections import Counter
import sys
from nltk.tokenize import word_tokenize
import nltk

mod_big = []
file_data = []
occurances = []
frequency_list = []
final_list = []
candidates = []

def word(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(word((open('big.txt').read())))

def modified_big(text):
    big = re.findall(r'\w+', text.lower())
    for i in range(len(big) - 1):
        curr = big[i]
        prev = big[i-1]
        nxt = big[i+1]
        mod_big.insert(i,[prev, curr, nxt])
    return mod_big

def modified_file(text):
    big = re.findall(r'\w+', text.lower())
    for i in range(len(big) - 1):
        curr = big[i]
        prev = big[i-1]
        nxt = big[i+1]
        file_data.insert(i,[prev, curr, nxt])
    return file_data

def most_frequent():
    most_freq = final_list[0][3]
    for i in range(len(final_list) - 1):
        if(final_list[i][3] > most_freq):
            most_freq = final_list[i][3]
    for i in range(len(final_list)):
        if(final_list[i][3] == most_freq):
            return final_list[i]

def correction(context): 
    "Most probable spelling correction for word." 
    # for i in range(len(mod_big)):
    #     if(mod_big[i][1] == context[1]):
    #         return context[1]
    #     else:
    #         frequency(context[1])
    #         if(mod_big[i][0] == context[i][0], mod_big[i][1] == context[i][1]):

    edit1 = (known(one_edit_distance(context[1])))
    edit2 = (known(two_edit_distance(context[1])))
    for i in edit1:
        candidates.append([i])
    for i in edit2:
        candidates.append([i])
    for i in candidates:
        frequency(i[0])

    prev = context[0]
    nxt = context[2]

    for i in range(len(final_list)):
        if(prev == final_list[i][0] and nxt == final_list[i][2]):
            return final_list[i][1]
        else:
            return context[1]
    

def occurance(word):
    for i in range(len(mod_big)):
        if(mod_big[i][1] == word):
            occurances.append(mod_big[i])

def count_occurances(prev_next):
    counter = 0
    for i in range(len(occurances)):
        if(occurances[i][0] == prev_next[0] and occurances[i][2] == prev_next[1]):
            counter = counter + 1
    return counter

def frequency(word):
    occurance(word)
    for i in range(len(occurances)):
        if(occurances[i][1] == word):
            frequency = count_occurances([occurances[i][0], occurances[i][2]])
            frequency_list.append([occurances[i][0], occurances[i][1], occurances[i][2], frequency])
    remove_duplicates(frequency_list)

def remove_duplicates(x):
    for i in x:
        if i not in final_list:
            final_list.append(i)

def one_edit_distance(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def two_edit_distance(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in one_edit_distance(word) for e2 in one_edit_distance(e1))

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def check_for_word(word, words):
    for i in range(len(words)):
        if(word == words[i]):
            return True
        elif(i != len(words)):
            continue
        else:
            return False

if __name__ == '__main__':
    line_split = []
    word_split = []
    words = []
    word(open('big.txt').read())
    modified_big(open('big.txt').read())
    with open('big.txt', 'r') as dataset:
        for line in dataset:
            line_split.append(word_tokenize(line))
    for i in range(len(mod_big)):
        word_split.append(mod_big[i][1])
    print("Enter a sentence: ")
    for line in sys.stdin:
        words = word_tokenize(line)
        if(words[0] == 'quit'):
            break
        else:     
            for i in range(len(words) - 1):
                if(check_for_word(words[i], word_split)):
                     print(words[i])
                else:
                    curr = words[i]
                    prev = words[i-1]
                    if(i >= len(words)):
                         nxt = words[0]
                    else:
                        nxt = words[i+1]
                    print(correction([prev, curr, nxt]))
            words.clear()
    # print(correction(['best', 'resourec', 'was']))

