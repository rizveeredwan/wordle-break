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


def wordle_next_level_search(maps, domain_knowledge, invalid_characters, last_used_domain_knowledge):
    possibles = []
    domain_knowledge_keys = list(domain_knowledge.keys())
    domain_knowledge_keys.sort()
    try:
        for key in tr.dict:
            # check domain knowledge
            # domain knowledge validation
            d = return_character_count(word=key)
            flag = True
            for key2 in domain_knowledge:
                if d.get(key2) is None:
                    flag = False
                    break
            if flag is False:
                # domain knowledge absence
                continue
            # print("CAME ", key, domain_knowledge, maps,invalid_characters)
            flag=True
            for i in range(0, len(maps)):
                if maps[i] != 0:
                    if key[i] == maps[i]:
                        continue
                    else:
                        flag = False
                        break
            if flag is False:
                # map violation
                continue
            # invalid character presence issue
            invalid_character_presence = False
            apply_domain_knowledge = {}
            dom_keys = []
            for i in range(0, len(key)):
                if key[i] == maps[i]:
                    # valid positional mapping
                    continue
                if domain_knowledge.get(key[i]) is not None:
                    if apply_domain_knowledge.get(key[i]) is None:
                        if last_used_domain_knowledge.get(key[i]) is not None and i in last_used_domain_knowledge[key[i]]:
                            continue
                        apply_domain_knowledge[key[i]] = i
                        dom_keys.append(key[i])
                        continue
                if invalid_characters.get(key[i]) is not None:
                    invalid_character_presence = True
                    break
            if invalid_character_presence is True:
                continue
            dom_keys.sort()
            print(domain_knowledge_keys, dom_keys, domain_knowledge_keys == dom_keys)
            if len(domain_knowledge_keys)>0 and domain_knowledge_keys != dom_keys:
                continue
            print(key, domain_knowledge, last_used_domain_knowledge, apply_domain_knowledge)
            print(dom_keys, domain_knowledge_keys)
            possibles.append(key)
    except Exception as e:
        print(e)
    return possibles


def handler(signum, frame):
    exit()


def get_information(input_string, maps,  domain_knowledge, invalid_characters, last_used_domain_knowledge):
    for i in range(0, len(input_string), 2):
        print(input_string[i], "yes")
        if input_string[i] == '0':
            continue
        else:
            if input_string[i+1] == '1':
                maps[int(floor(i / 2))] = input_string[i]
                if domain_knowledge.get(input_string[i]) is not None:
                    # requirement chilo, filled up
                    domain_knowledge[input_string[i]] = 0
                    del domain_knowledge[input_string[i]]
                    del last_used_domain_knowledge[input_string[i]]
            elif input_string[i+1] == '0':
                domain_knowledge[input_string[i]] = 1
                if last_used_domain_knowledge.get(input_string[i]) is None:
                    last_used_domain_knowledge[input_string[i]] = []
                if int(floor(i / 2)) not in last_used_domain_knowledge[input_string[i]]:
                    last_used_domain_knowledge[input_string[i]].append(int(floor(i / 2)))
            elif input_string[i+1] == '2':
                invalid_characters[input_string[i]] = True
    # repeating characters' domain knowledge update
    for i in range(0, len(input_string), 2):
        print(input_string[i], "yes")
        if input_string[i] == '0':
            continue
        else:
            if input_string[i + 1] == '0':
                domain_knowledge[input_string[i]] = 1
                if last_used_domain_knowledge.get(input_string[i]) is None:
                    last_used_domain_knowledge[input_string[i]] = []
                if int(floor(i / 2)) not in last_used_domain_knowledge[input_string[i]]:
                    last_used_domain_knowledge[input_string[i]].append(int(floor(i / 2)))
    return domain_knowledge, maps, invalid_characters, last_used_domain_knowledge


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
    last_used_domain_knowledge = {}
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
            domain_knowledge, maps, invalid_characters, last_used_domain_knowledge = get_information(input_string, maps, domain_knowledge, invalid_characters, last_used_domain_knowledge)
            print(domain_knowledge, maps, invalid_characters, last_used_domain_knowledge)
            possibles = wordle_next_level_search(maps, domain_knowledge, invalid_characters, last_used_domain_knowledge)
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