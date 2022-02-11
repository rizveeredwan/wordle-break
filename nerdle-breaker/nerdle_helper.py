import random
from math import floor
from random import shuffle
import signal

W=open('output.txt', 'w')
class NerdleHelper:
    def __init__(self):
        self.weights = {
            '/': 4,
            '*': 4,
            '-': 3,
            '+': 3
        }
        self.already_applied = {}

    def generate_number(self, _list):
        new_list = []
        for i in range(0, len(_list)):
            if len(new_list) == 0:
                if 0 <= _list[i] <= 9:
                    new_list.append(_list[i])
                else:
                    new_list.append(_list[i])
            else:
                if _list[i] in ['/', '*', '+', '-']:
                    new_list.append(_list[i])
                else:
                    if new_list[-1] in ['/', '*', '+', '-']:
                        new_list.append(int(_list[i]))
                    else:
                        new_list[-1] = new_list[-1] * 10 + _list[i]
        return new_list

    def absurd_string_detection(self, _list):
        _stack = []
        for i in range(0, len(_list)):
            if len(_stack) == 0:
                _stack.append(_list[i])
            else:
                if _stack[-1] in ['/', '*', '+', '-', '=']:
                    _stack.append(_list[i])
                else:
                    if _list[i] in ['/', '*', '+', '-', '=']:
                        _stack.append(_list[i])
                    else:
                        _stack[-1] = _stack[-1] * 10 + _list[i]

        _str = ""
        for i in range(0, len(_stack)):
            _str = _str + str(_stack[i])
        # print("_stack ", _stack, len(_str), len(_list))
        if len(_str) != len(_list):
            return False
        return True

    def postfix_generation(self, maths):
        _stack = []
        postfix = []
        for i in range(0, len(maths)):
            # print(maths, maths[i])
            if type(maths[i]) is int:
                postfix.append(maths[i])
            else:
                if len(_stack) == 0:
                    _stack.append(maths[i])
                else:
                    if self.weights[_stack[-1]] < self.weights[maths[i]]:
                        # current has higher preference
                        _stack.append(maths[i])
                    else:
                        while len(_stack) > 0:
                            if self.weights[_stack[-1]] >= self.weights[maths[i]]:
                                postfix.append(_stack[-1])
                                _stack.pop()
                        _stack.append(maths[i])
        while len(_stack) > 0:
            postfix.append(_stack.pop())
        return postfix

    def evaluation(self, postfix):
        _stacks = []
        try:
            for i in range(0, len(postfix)):
                # print('_stacks ', _stacks)
                if type(postfix[i]) is int:
                    _stacks.append(postfix[i])
                else:
                    if postfix[i] in ['*', '/', '+', '-']:
                        if len(_stacks) < 2:
                            raise Exception("Error")
                        v2 = _stacks.pop()
                        v1 = _stacks.pop()
                        if type(v1) is not int or type(v2) is not int:
                            raise Exception("Error")
                        if postfix[i] == '*':
                            v = v1 * v2
                        if postfix[i] == '/':
                            if v2 == 0:
                                raise Exception("Error")
                            v = int(v1 / v2)
                            if v1 % v2 != 0:
                                raise Exception("Error")
                        if postfix[i] == '+':
                            v = v1 + v2
                        if postfix[i] == '-':
                            v = v1 - v2
                        _stacks.append(v)
                    else:
                        pass
                        """
                        if postfix[i] in ['+', '-']:
                            if len(_stacks) < 2:
                                v1 = _stacks.pop()
                                v2 = _stacks.pop()
                                if postfix[i] == '+':
                                    v = v1 + v2
                                if postfix[i] == '-':
                                    v = v1 + v2
                            else:
                                pass
                        """
        except Exception as e:
            # print(e)
            return None
        if len(_stacks) != 1:
            raise Exception("Error")
        return _stacks[-1]

    def mathematical_string_validation(self, gen_string):
        parts = [[], []]
        flag = False
        for i in range(0, len(gen_string)):
            if gen_string[i] == '=':
                flag = True
                continue
            if flag is False:
                parts[0].append(gen_string[i])
            else:
                parts[1].append(gen_string[i])
        result = parts[1]
        maths = parts[0]
        # print("maths ", maths, result)
        result = self.generate_number(_list=result)
        maths = self.generate_number(_list=maths)
        postfix = self.postfix_generation(maths=maths)
        # print("postfix ",postfix)
        try:
            value = self.evaluation(postfix)
            print("value ", value, postfix, gen_string, maths, result)
            if value == result[0]:
                return True
            else:
                return None
        except Exception as e:
            # print("e ", e)
            return None

    def find_random_unset_idx(self, gen_string):
        while True:
            idx = random.randint(0, len(gen_string) - 1)
            if gen_string[idx] is None:
                return idx

    def generation_validation(self, gen_string):
        if '*' not in gen_string and '/' not in gen_string and '+' not in gen_string and '-' not in gen_string:
            return False
        for i in range(0, len(gen_string)):
            if gen_string[i] in ['+', '-', '*', '/']:
                if i-1 >= 0 and type(gen_string[i-1]) is int and i+1 < len(gen_string) and type(gen_string[i+1]) is int:
                    continue
                else:
                    return False
        return True

    def backtrack_combination(self, idx, end, gen_string, curr_generations, generations, valids):
        if idx > end:
            generations.append([])
            for i in range(0, len(curr_generations)):
                generations[-1].append(curr_generations[i])
            return
        if gen_string[idx] is not None:
            # mapped already
            curr_generations.append(gen_string[idx])
            self.backtrack_combination(idx+1, end, gen_string, curr_generations, generations, valids)
            curr_generations.pop()
        else:
            for ch in valids:
                curr_generations.append(ch)
                self.backtrack_combination(idx + 1, end, gen_string, curr_generations, generations, valids)
                curr_generations.pop()
            pass

    def sort_mix_list(self, _list):
        for i in range(0, len(_list)):
            best_idx = i
            best_value = _list[i]
            if type(_list[i]) is not int:
                best_value = ord(_list[i])
            for j in range(i+1, len(_list)):
                com_value = _list[j]
                if type(_list[j]) is not int:
                    com_value = ord(_list[j])
                if com_value < best_value:
                    best_value = com_value
                    best_idx = j
            temp = _list[i]
            _list[i] = _list[best_idx]
            _list[best_idx] = temp
        return

    def string_generation(self, maps, domain_knowledge, invalid_characters, last_used_domain_knowledge):
        print("YESSS")
        domain_knowledge_keys = list(domain_knowledge.keys())
        self.sort_mix_list(_list=domain_knowledge_keys)
        print("YESSS 1")
        print("domain_knowledge_keys ",domain_knowledge_keys)
        characters = []
        for i in range(0, 10):
            characters.append(0)
        characters.append('+')
        characters.append('-')
        characters.append('*')
        characters.append('/')
        possibilities = []
        gen_string = [None, None, None, None, None, None, None, None]
        # using map to fix the positions
        equals_position = None
        for i in range(0, 8):
            if maps[i] is not None:
                gen_string[i] = maps[i]
            if gen_string[i] == '=':
                equals_position = i
        print("gen_string1 ", gen_string)
        # applying = sign
        if '=' not in gen_string:
            # did not use = yet
            while True:
                idx = random.randint(3, 6)
                print("idx ",idx)
                if self.already_applied.get(idx) is not None:
                    continue
                gen_string[idx] = '='
                equals_position = idx
                self.already_applied[idx] = True
                break
        print("gen_string2 ", gen_string)
        # random generation
        left_side_possibilities = []
        self.backtrack_combination(idx=0, end=equals_position - 1, gen_string=gen_string, curr_generations = [],
                                   generations=left_side_possibilities, valids=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', '-', '*', '/'])
        print(len(left_side_possibilities), left_side_possibilities[0])
        right_side_possibilities = []
        self.backtrack_combination(idx=equals_position+1, end=len(gen_string)-1, gen_string=gen_string, curr_generations=[],
                                   generations=right_side_possibilities, valids=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        print(len(right_side_possibilities), right_side_possibilities[0])
        shuffle(left_side_possibilities)
        shuffle(right_side_possibilities)
        tmp = []
        for j in range(0, len(left_side_possibilities)):
            # normal generation validation
            if self.generation_validation(left_side_possibilities[j]) is True:
                tmp.append(left_side_possibilities[j])
        left_side_possibilities = tmp
        print("simulating ", len(left_side_possibilities) * len(right_side_possibilities))
        left_dict = {}
        lt_cnt, rt_cnt = 0, 0
        for j in range(0, len(left_side_possibilities)):
            try:
                if self.absurd_string_detection(_list=left_side_possibilities[j]) is False:
                    continue
                maths = self.generate_number(_list=left_side_possibilities[j])
                pf = self.postfix_generation(maths=maths)
                ev = self.evaluation(postfix=pf)
                if ev is None:
                    continue
                if left_dict.get(ev) is None:
                    left_dict[ev] = []
                left_dict[ev].append(left_side_possibilities[j])
                #print("LS ", ev, left_side_possibilities[j], pf, equals_position)
                # W.write("LS {} {} {} {}\n".format(ev, left_side_possibilities[j], pf, equals_position))
                lt_cnt = lt_cnt + 1
            except Exception as e:
                print(e)
        right_dict = {}
        for j in range(0, len(right_side_possibilities)):
            if self.absurd_string_detection(_list=right_side_possibilities[j]) is False:
                continue
            try:
                maths = self.generate_number(_list=right_side_possibilities[j])
                pf = self.postfix_generation(maths=maths)
                ev = self.evaluation(postfix=pf)
                if ev is None:
                    continue
                if right_dict.get(ev) is None:
                    right_dict[ev] = []
                # W.write("RS {} {} {} {}\n".format(ev, right_side_possibilities[j], pf, equals_position))
                #print("RS ", ev, right_side_possibilities[j], pf, equals_position)
                rt_cnt = rt_cnt + 1
                right_dict[ev].append(right_side_possibilities[j])
            except Exception as e:
                print(e)
        print("LT RT ",lt_cnt, rt_cnt)
        for key in left_dict:
            if right_dict.get(key) is not None:
                for j in range(0, len(left_dict[key])):
                    for l in range(0, equals_position):
                        gen_string[l] = left_dict[key][j][l]
                    for k in range(0, len(right_dict[key])):
                        for l in range(0, len(right_dict[key][k])):
                            gen_string[equals_position + 1 + l] = right_dict[key][k][l]
                        print(gen_string, left_dict[key][j], right_dict[key][k])
                        W.write("First: {} {} {}\n".format(gen_string, left_dict[key][j], right_dict[key][k]))
                        # invalid character check
                        keys = {}
                        for l in range(0, len(gen_string)):
                            if maps[l] is not None:
                                continue
                            if keys.get(gen_string[l]) is None:
                                keys[gen_string[l]] = 1
                        flag = True
                        W.write("{} ".format(flag))
                        # domain knowledge presence validation
                        for elm in domain_knowledge:
                            if keys.get(elm) is None:
                                flag = False
                                break
                        print(keys, domain_knowledge, flag)
                        W.write("{} {} {} {}\n".format(keys, domain_knowledge, flag, invalid_characters))
                        if flag is True:
                            print(keys, list(domain_knowledge.keys()), domain_knowledge, flag)
                            W.write("{} {} {} {}\n".format(keys, list(domain_knowledge.keys()), domain_knowledge, flag))
                            # domain knowledge satisfied
                            flag = True
                            applied_domain_knowledge = {}
                            dom_keys = []
                            for l in range(0, len(gen_string)):
                                if maps[l] is not None:
                                    continue
                                if domain_knowledge.get(gen_string[l]) is not None:
                                    if applied_domain_knowledge.get(gen_string[l]) is None:
                                        if last_used_domain_knowledge.get(gen_string[l]) is not None and l in last_used_domain_knowledge[gen_string[l]]:
                                            continue
                                        applied_domain_knowledge[gen_string[l]] = l
                                        dom_keys.append(gen_string[l])
                                        continue
                                if invalid_characters.get(gen_string[l]) is not None:
                                    flag = False
                                    break
                            if flag is False:
                                continue
                            else:
                                #print("gen string ", gen_string)
                                if self.absurd_string_detection(_list=gen_string) is False:
                                    #print("YES")
                                    continue
                                self.sort_mix_list(_list=dom_keys)
                                print("dom_keys ",dom_keys, domain_knowledge_keys)
                                if len(domain_knowledge_keys) > 0 and domain_knowledge_keys != dom_keys:
                                    # can't properly apply domain knowledge
                                    continue
                                possibilities.append([])
                                for l in range(0, len(gen_string)):
                                    possibilities[-1].append(gen_string[l])
        return possibilities

    def get_information(self, input_string, maps, domain_knowledge, invalid_characters, last_used_domain_knowledge):
        # updating maps + domain knowledge
        for i in range(0, len(input_string), 2):
            if input_string[i] == 'X':
                # No idea
                continue
            else:
                validity = input_string[i+1]
                if validity == '1' and maps[floor(i/2)] is None:
                    char = input_string[i]
                    if char >= '0' and char <= '9':
                        char = int(char)
                    maps[floor(i/2)] = char
                    if domain_knowledge.get(char) is not None:
                        # jana knowledge ami komaye dilam
                        del domain_knowledge[char]
                        del last_used_domain_knowledge[char]
                elif validity == '0':
                    # a possible option
                    char = input_string[i]
                    if char >= '0' and char <= '9':
                        char = int(char)
                    if domain_knowledge.get(char) is None:
                        domain_knowledge[char] = 1
                    if last_used_domain_knowledge.get(char) is None:
                        last_used_domain_knowledge[char] = []
                    if int(floor(i / 2)) not in last_used_domain_knowledge[char]:
                        last_used_domain_knowledge[char].append(int(floor(i / 2)))
                elif validity == '2':
                    char = input_string[i]
                    if char >= '0' and char <= '9':
                        char = int(char)
                    invalid_characters[char] = 1
        return domain_knowledge, maps, invalid_characters, last_used_domain_knowledge

    def input_validation(self, input_string):
        if len(input_string) != 16:
            print("input length error")
            return False
        for i in range(0, len(input_string), 2):
            print(input_string, input_string[i], ord(input_string[i]))
            if input_string[i] == 'X':
                continue
            elif input_string[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '=']:
                print("dhuke ", input_string[i + 1])
                if input_string[i + 1] in ['0', '1', '2']:
                    continue
                else:
                    print("P value not properly given in {}th index", format(i + 1), input_string[i + 1],
                          type(input_string[i + 1]))
                    return False
            else:
                print("C value not properly given in {}th index", format(i))
                return False
        return True

    def nerdle_next_level_search(self, maps, domain_knowledge, invalid_characters, last_used_domain_knowledge):
        possibles = []
        possibles = self.string_generation(maps, domain_knowledge, invalid_characters, last_used_domain_knowledge)
        print(len(possibles))
        if len(possibles) > 0:
            idx = random.randint(0, len(possibles)-1)
            return possibles[idx]
        return None

    def process(self):
        domain_knowledge = {
            '=': 1
        }
        invalid_characters = {}
        maps = [None, None, None, None, None, None, None, None]
        last_used_domain_knowledge = {}
        try:
            while True:
                print(
                    "Input will always be 16 characters: ith possible character(C), its guarantee of occurring there(P)")
                print("If ith character(C) is X, it means not sure about this position")
                print(
                    "If for any ith position C is given but P is given as 0, it means, I know C will occur but not sure if it occurs in this position")
                print(
                    "If for any ith position C is given but P is given as 1, it means, I know C will definitely occur in this position")
                print(
                    "If for any ith position C is given but P is given 2, it means, I know C will never occur in this string")
                input_string = input()
                input_string = input_string.strip()
                input_string = input_string.upper()
                if self.input_validation(input_string) is False:
                    print("input error ")
                    continue
                domain_knowledge, maps, invalid_characters, last_used_domain_knowledge = self.get_information(input_string, maps, domain_knowledge,
                                                                                  invalid_characters, last_used_domain_knowledge)
                print(domain_knowledge, maps, invalid_characters, last_used_domain_knowledge)
                possibles = self.nerdle_next_level_search(maps, domain_knowledge, invalid_characters, last_used_domain_knowledge)
                print(possibles)
        except Exception as e:
            print(e)


def handler(signum, frame):
    exit()


signal.signal(signal.SIGINT, handler)


nerdle_helper = NerdleHelper()
#nerdle_helper.string_validation(gen_string='9+8/8=10')
nerdle_helper.process()
