import os
import signal
from math import floor
import random

class Trie:
    def __init__(self):
        self.dict = {}

    def insert_words(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            for lines in f:
                l = lines.strip().split(' ')[0]
                self.dict[l.upper()] = True


def word_validation(word):
    for i in range(0, len(word)):
        if ord('a') <= ord(word[i]) <= ord('z'):
            continue
        else:
            return False
    return True


def reduce_data(file_name):
    w = open('data_5_length.txt', 'w', encoding='utf-8')
    with open(file_name, 'r', encoding='utf-8') as f:
        for lines in f:
            l = lines.strip().split(' ')
            word = l[0]
            if word_validation(word) is True and len(word) == 5:
                w.write(word+'\n')


# reduce_data(file_name=os.path.join('.','data.txt'))

def return_character_count(word):
    d = {}
    for i in range(0, len(word)):
        if d.get(word[i]) is None:
            d[word[i]] = 0
        d[word[i]] = d[word[i]] + 1
    return d


def wordle_next_level_search(maps, domain_knowledge, invalid_characters):
    possibles = []
    try:
        for key in tr.dict:
            # invalid character presence issue
            invalid_character_presence = False
            for i in range(0, len(key)):
                if invalid_characters.get(key[i]) is not None:
                    invalid_character_presence = True
                    break
            if invalid_character_presence is True:
                continue
            # domain knowledge validation
            d = return_character_count(word=key)
            d_flag = True
            for key2 in domain_knowledge:
                if d.get(key2) is None or d[key2] != domain_knowledge[key2]:
                    d_flag = False
                    break
            if d_flag is True:
                pos_flag = True
                for i in range(0, len(maps)):
                    if maps[i] != 0:
                        if key[i] == maps[i]:
                            continue
                        else:
                            pos_flag = False
                            break
                if pos_flag is True:
                    possibles.append(key)
    except Exception as e:
        print(e)
    return possibles


def handler(signum, frame):
    exit()


def get_information(input_string, maps,  domain_knowledge, invalid_characters):
    for i in range(0, len(input_string), 2):
        print(input_string[i], "yes")
        if input_string[i][0] == '0':
            continue
        else:
            if input_string[i + 1] in ['0', '1']:
                if domain_knowledge.get(input_string[i][0]) is None:
                    domain_knowledge[input_string[i][0]] = 0
                domain_knowledge[input_string[i][0]] = 1
            if input_string[i+1] == '1':
                maps[int(floor(i/2))] = input_string[i]
            if input_string[i + 1] == '2':
                invalid_characters[input_string[i][0]] = True
    return domain_knowledge, maps, invalid_characters


def input_validation(input_string):
    if len(input_string) != 10:
        print("input length error")
        return False
    for i in range(0, len(input_string), 2):
        print(input_string, input_string[i], ord(input_string[i]),)
        if input_string[i] == '0':
            continue
        if 'A' <= input_string[i] <= 'Z':
            print("dhuke ", input_string[i+1])
            if input_string[i+1] in ['0', '1', '2']:
                continue
            else:
                print("P value not properly given in {}th index", format(i+1), input_string[i+1], type(input_string[i+1]))
                return False
        else:
            print("C value not properly given in {}th index", format(i))
            return False
    return True


def process():
    domain_knowledge={}
    invalid_characters={}
    maps = [0, 0, 0, 0, 0]
    try:
        while True:
            print("Input will always be 10 characters: ith possible character(C), its guarantee of occurring there(P)")
            print("If ith character(C) is 0, it means not sure about this position")
            print("If for any ith position C is given but P is given as 0, it means, I know C will occur but not sure if it occurs in this position")
            print("If for any ith position C is given but P is given as 1, it means, I know C will definitely occur in this position")
            print("If for any ith position C is given but P is given 2, it means, I know C will never occur in this string")
            input_string = input()
            input_string = input_string.strip()
            input_string = input_string.upper()
            if input_validation(input_string) is False:
                print("input error ")
                continue
            domain_knowledge, maps, invalid_characters = get_information(input_string, maps, domain_knowledge, invalid_characters)
            print(domain_knowledge, maps, invalid_characters)
            possibles = wordle_next_level_search(maps, domain_knowledge, invalid_characters)
            print(len(possibles))
            if len(possibles) > 0:
                idx = random.randint(0, len(possibles)-1)
                print("A possible choice {}".format(possibles[idx]))
            print()

    except Exception as e:
        print(e)


tr = Trie()
tr.insert_words(file_name=os.path.join('.','data_5_length.txt'))
signal.signal(signal.SIGINT, handler)
process()