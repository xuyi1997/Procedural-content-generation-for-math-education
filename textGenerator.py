import tracery
from copy import deepcopy
import random
from tracery.modifiers import base_english
from TemplateA import w2v, database, phead
from text_templateGenerate import TextTemplateGenerator
from numpy import *

Ncandidates = 20

det_list = ["a", "an", "the", "these", "this"]
class Add(object):

    def __init__(self, operands):
        self.operands = operands
        self.relation = ""
        self.entities = []
        self.story = ""
        self.theme = ""

    def facts_to_template(self):
        z = self.operands[0] + self.operands[1]
        self.theme = input("Please enter theme: Normal: N; Fiction: F ")
        # Set Facts
        # e.g. Tom has 5 marbles, Jerry gives Tom 3 marbles, how many marbles does Tom have now?
        fa = {'relation': "has", 'entities': ["#character1#", self.operands[0], "#object1.s#"]}
        fb = {'relation': "gives", 'entities': ["#character2#", "#character1#", self.operands[1], "#object1.s#"]}
        fc = {'relation': "have", 'entities': ["#character1#", z, "#object1.s#"], 'Unknown': z}
        facts1 = [fa, fb, fc]
        endstr1 = ' now'
        # e.g. There are 11 girls and 12 boys in the classroom. How many children are there in total?
        fd = {'relation': "there_are", 'entities': [self.operands[0], "#object1.s#", self.operands[1], "#object2.s#", "#location#"]}
        fe = {'relation': "there_are", 'entities': [z, "#object_class.s#"], 'Unknown': z}
        facts2 = [fd, fe]
        endstr2 = ' in total'
        # e.g. Tom has 2 marbles, Jerry has 3 marbles, how many marbles does Tom and Jerry have in total?
        fg = {'relation': "has", 'entities': ["#character2#", self.operands[1], "#object1.s#"]}
        fh = {'relation': "have", 'entities': ["#character1# and #character2#", z, "#object1.s#"], 'Unknown': z}
        facts3 = [fa, fg, fh]
        endstr3 = ' in total'
        # e.g. Tom bought a parrot for 3 krones, then he bought a pear for 5 krones . How much does Tom spend in total?
        fi = {'relation': "bought", 'entities': ["#character1#", "#object1#", self.operands[0], "#currency.s#"]}
        fj = {'relation': "bought", 'entities': ["#character1#", "#object2#", self.operands[1], "#currency.s#"]}
        fk = {'relation': "spend", 'entities': ["#character1#", z, "#currency#"], 'Unknown': z}
        facts4 = [fi, fj, fk]
        endstr4 = ' in total'


        # fl = {'relation': "#walk#", 'entities': ["#character1#",  self.operands[0], "#distance_unit.s#", "#location1#", "#location2#"]}
        # fm = {'relation': "#walk#", 'entities': ["#character1#",  self.operands[1], "#distance_unit.s#", "#location2#", "#location3#"]}
        # fn = {'relation': "#walk#", 'entities': ["#character1#",  z, "#distance_unit.s#"], 'Unknown': z}
        # facts5 = [fl, fm, fn]
        # head['set'] += "[walk: #walk#][distance_unit: #distance_unit#][location1: #location1#][location2: #location2#]"
        # text_template5 = TextTemplateGenerator(facts5).decider()
        # text_template5 += ' in total'

        # choose fact:
        a = self.operands[0]
        b = self.operands[1]
        # for decimals
        if a % 1 > 0 or b % 1 > 0 or '.' in str(a) or '.' in str(b):
            facts = [facts4]
            endstr_list = [endstr4]
        else:
            facts = [facts1, facts2, facts3]
            endstr_list = [endstr1, endstr2, endstr3]
        text_list = []
        for i in range(len(facts)):
            text_list.append(generate_text(self.theme, self.operands, facts[i], endstr_list[i]))
        return text_list


class Sub(object):

    def __init__(self, operands):
        self.operands = operands
        self.relation = ""
        self.entities = []
        self.story = ""
        self.theme = ""

    def facts_to_template(self):
        z = self.operands[0] + self.operands[1]
        self.theme = input("Please enter theme: Normal: N; Fiction: F ")
        # Set Facts
        # A has 3 apples, A gives 2 apples to B, how many apples does A have left.
        fa = {'relation': "has", 'entities': ["#character1#", self.operands[0], "#object1.s#"]}
        fb = {'relation': "gives", 'entities': ["#character1#", "#character2#", self.operands[1], "#object1.s#"]}
        fc = {'relation': "have", 'entities': ["#character1#", z, "#object1.s#"], 'Unknown': z}
        facts1 = [fa, fb, fc]
        endstr1 = ' left'

        fd = {'relation': "has", 'entities': ["#character1#", self.operands[0], "#currency.s#"]}
        # somebody buy sth for n euros
        fe = {'relation': "bought", 'entities': ["#character1#", "#object1#", self.operands[1], "#currency.s#"]}
        ff = {'relation': "have", 'entities': ["#character1#", z, "#currency#"], 'Unknown': z}
        facts2 = [fd, fe, ff]
        endstr2 = ' left'

        # e.g. Tom has 5 marbles, Jerry has 3 marbles, how many more marbles does Tom have than Jerry?
        fg = {'relation': "has", 'entities': ["#character2#", self.operands[1], "#object1.s#"]}
        fh = {'relation': "have_more", 'entities': ["#character1#", z, "#character2#", "#object1#"], 'Unknown': z}
        facts3 = [fa, fg, fh]
        endstr3 = ''
        # e.g. There are 40 cookies, A takes 10 cookies, how many cookies are there left.
        fi = {'relation': "there_are", 'entities': [self.operands[0], "#object1.s#", "#container#"]}
        fj = {'relation': "takes", 'entities': ["#character1#", self.operands[1], "#object1.s#"]}
        fk = {'relation': "there_are", 'entities': [z, "#object1.s#"], 'Unknown': z}
        facts4 = [fi, fj, fk]
        endstr4 = ' left'

        # choose fact:
        a = self.operands[0]
        b = self.operands[1]
        # for decimals
        if a % 1 > 0 or b % 1 > 0 or '.' in str(a) or '.' in str(b):
            facts = [facts2]
            endstr_list = [endstr2]
        else:
            facts = [facts1, facts3, facts4]
            endstr_list = [endstr1, endstr3, endstr4]
        text_list = []
        for i in range(len(facts)):
            text_list.append(generate_text(self.theme, self.operands, facts[i], endstr_list[i]))
        return text_list


class Mul(object):

    def __init__(self, operands):
        self.operands = operands
        self.relation = ""
        self.entities = []
        self.story = ""
        self.theme = ""

    def facts_to_template(self):
        z = self.operands[0] + self.operands[1]
        self.theme = input("Please enter theme: Normal: N; Fiction: F ")
        # One apple costs 0.2 euro, Tom bought 2 apples, how much does Tome spend?
        fa = {'relation': "costs", 'entities': ["One #object1#", self.operands[0], "#currency.s#"]}
        fb = {'relation': "bought ", 'entities': ["#character1#", self.operands[1], "#object1.s#"]}
        fc = {'relation': "spend", 'entities': ["#character1#", z, "#currency#"], 'Unknown': z}
        facts1 = [fa, fb, fc]
        endstr1 = ' in total'
        # One round is 2 kilometers, Tom cycled 5 laps, how long does Tom cycle in total?

        # There are 320 gift box in the warehouse, each gift box has 10 pencils, how many pencils are there in the warehouse?
        fg = {'relation': "there_are", 'entities': [self.operands[0], "#container.s#", "#location#"]}
        fh = {'relation': "has", 'entities': ["Each #container#", self.operands[1], "#object1.s#"]}
        fi = {'relation': "there_are", 'entities': [z, "#object1.s#"], 'Unknown': z}
        facts2 = [fg, fh, fi]
        endstr2 = ' in total'

        # Tom make 5 glasses of lemonade, each glass of lemonade need 3 lemons, how many lemons dose Tom need in total?
        fg = {'relation': "makes", 'entities': ["#character1#", self.operands[0], "#quantity_unit.s# of #food#"]}
        fh = {'relation': "needs", 'entities': ["Each #quantity_unit# of #food#", self.operands[1], "#ingredient.s#"]}
        fi = {'relation': "need", 'entities': ["#character1#", z, "#ingredient.s#"], 'Unknown': z}
        facts3 = [fg, fh, fi]
        endstr3 = ' in total'

        # choose fact:
        a = self.operands[0]
        b = self.operands[1]
        # for decimals
        if a % 1 > 0 or b % 1 > 0 or '.' in str(a) or '.' in str(b):
            facts = [facts1]
            endstr_list = [endstr1]
        else:
            facts = [facts2, facts3, facts1]
            endstr_list = [endstr2, endstr3, endstr1]
        text_list = []
        for i in range(len(facts)):
            text_list.append(generate_text(self.theme, self.operands, facts[i], endstr_list[i]))
        return text_list


class Dev(object):

    def __init__(self, operands):
        self.operands = operands
        self.relation = ""
        self.entities = []
        self.story = ""
        self.theme = ""

    def facts_to_template(self):
        z = self.operands[0] + self.operands[1]
        self.theme = input("Please enter theme: Normal: N; Fiction: F ")
        # Tom has 10 apples, Tom share apples evenly to 5 children, how many apples does each child get?
        fa = {'relation': "has", 'entities': ["#character1#", self.operands[0], "#object1.s#"]}
        fb = {'relation': "share", 'entities': ["#character1#", "#object1.s#", self.operands[1], "friends"]}
        fc = {'relation': "get", 'entities': ["each friend", z, "#object1.s#"], 'Unknown': z}
        facts1 = [fa, fb, fc]
        endstr1 = '?'
        fd = {'relation': "has", 'entities': ["#character1#", self.operands[0], "#object1.s#"]}
        fe = {'relation': "split", 'entities': ["#character1#", "#object1.s#", self.operands[1], "#container.s#"]}
        ff = {'relation': "have", 'entities': [z, "each #container#", "#object1.s#"], 'Unknown': z}
        facts2 = [fd, fe, ff]
        endstr2 = '?'
        fg = {'relation': "bought ", 'entities': ["#character1#", self.operands[1], "#object1.s#"]}
        fh = {'relation': "spend ", 'entities': ["#character1#", self.operands[0], "#currency.s#"]}
        fi = {'relation': "cost ", 'entities': ["each #object1#", z, "#currency.s#"], 'Unknown': z}
        facts3 = [fg, fh, fi]
        endstr3 = '?'

        # choose fact:
        a = self.operands[0]
        b = self.operands[1]
        # for decimals
        if a % 1 > 0 or b % 1 > 0 or '.' in str(a) or '.' in str(b):
            facts = [facts3]
            endstr_list = [endstr3]
        else:
            facts = [facts1, facts2, facts3]
            endstr_list = [endstr1, endstr2, endstr3]
        text_list = []
        for i in range(len(facts)):
            text_list.append(generate_text(self.theme, self.operands, facts[i], endstr_list[i]))

        return text_list


def generate_text(theme, operands, facts, endstr):
    fact_list = facts
    temp_list = []
    relation_words = []
    for fact in fact_list:
        relation_words.append(fact['relation'])
        for entity in fact['entities']:
            if '#' in str(entity):
                temp_list.append(entity)
    replace_word_list = list(set(temp_list))
    candidates = []
    word_score = []
    for num in range(20 * len(replace_word_list)):
        head = deepcopy(phead)
        head.update(database)
        head['story'] = "-".join(replace_word_list)
        if 'object_class' in head['story']:
            head['set'] += '[#setclass#]'
        set_theme(head, theme)
        # ("head1", head)
        set_num_constraints(head, operands)
        # print("head2", head)
        word_list = retreive_words(head)
        score = get_score(relation_words, word_list)
        word_score.append(score)
        candidates.append(word_list)
    max_score_index = word_score.index(max(word_score))
    final_word_list = candidates[max_score_index]
    final_dictionary = dict(zip(replace_word_list, final_word_list))
    text_template = TextTemplateGenerator(fact_list).decider()
    # print(text_template)
    final_text = str(text_template)
    for item in replace_word_list:
        final_text = final_text.replace(str(item), str(final_dictionary[item]))
    final_text += endstr
    # print(final_text)
    return final_text


def set_theme(head, theme):
    s = ""
    if theme == 'N':
        s = "[#Normal_theme#]"
    elif theme == 'F':
        s = "[#Fiction_theme#]"
    elif theme == 'M':
        s = "[#Movie_theme#]"
    elif theme == 'C':
        s = "[#Cartoon_theme#]"
    str_list = list(head['origin'][0])
    str_list.insert(1, s)
    head['origin'][0] = "".join(str_list)


def set_num_constraints(head, operands):
    a = operands[0]
    b = operands[1]
    # for decimals
    if a % 1 > 0 or b % 1 > 0 or '.' in str(a) or '.' in str(b) or 'currency' in head['story']:
        # set price constraints
        if (0 < a <= 10 or 0 < b <= 10) and 'object_class' not in head['story']:
            head['set'] += "[object1: #price_10#][object2: #price_10#]"
        elif (10 < a <= 100 or 10 < b <= 100) and 'object_class' not in head['story']:
            head['set'] += "[object1: #price_100#][object2: #price_100#]"
        elif (100 < a <= 1000 or 10 < b <= 1000) and 'object_class' not in head['story']:
            head['set'] += "[object1: #price_1000#][object2: #price_1000#]"
        elif 'object_class' not in head['story']:
            head['set'] += "[object1: #price_10000#][object2: #price_10000#]"
    # for integers set quantity constraints
    else:
        if (20 < a <= 100 or 20 < b <= 100) and 'object_class' not in head['story']:
            head['set'] += "[object1: #obj_100#][object2: #obj_100#]"
        elif (a > 100 or b > 100) and 'object_class' not in head['story']:
            head['set'] += "[object1: #obj_1000#][object2: #obj_1000#]"


def retreive_words(head):
    grammar = tracery.Grammar(head)
    grammar.add_modifiers(base_english)
    is_reproduce = True
    word_list = []
    while is_reproduce:
        text = str(grammar.flatten("#origin#"))
        word_list = []
        for word in text.split("-"):
            word = str(word).strip(" ")
            word_list.append(word)
        if len(word_list) != len(set(word_list)):
            print("Duplicates! Need Reproduce")
        else:
            is_reproduce = False

    return word_list


def get_score(relation_words, original_word_list):
    word_list = deepcopy(original_word_list)
    new_word_list = []
    for relation_word in relation_words:
        word_list.append(relation_word)
    # print(word_list)
    score_list = []
    l = len(word_list)
    for i in range(l):
        j = i+1
        w1 = word_list[i]
        word1 = w1
        if 'and' in word1:
            continue
        if '_' in w1:
            p = w1.find('_')
            word1 = w1[p+1:len(w1)]
        word1.strip()
        while j < l:
            w2 = word_list[j]
            word2 = w2
            if 'and' in word2:
                j += 1
                continue
            if '_' in w2:
                p = w2.find('_')
                word2 = w2[p+1:len(w2)]
            word2.strip()
            score_list.append(w2v.similarity(word1,word2))
            # score_list.append(5)
            j += 1
    score = mean(score_list)
    # print(score)
    return score


def temp_sum(operands):
    add_text = Add(operands)
    text_list = add_text.facts_to_template()
    questions = ""
    for text in text_list:
        questions += text
        questions += "\n"
    # print(questions)
    return questions


def temp_sub(operands):
    sub_text = Sub(operands)
    text_list = sub_text.facts_to_template()
    questions = ""
    for text in text_list:
        questions += text
        questions += "\n"
    # print(questions)
    return questions


def temp_mul(operands):
    mul_text = Mul(operands)
    text_list = mul_text.facts_to_template()
    questions = ""
    for text in text_list:
        questions += text
        questions += "\n"
    # print(questions)
    return questions


def temp_dev(operands):
    add_text = Dev(operands)
    text_list = add_text.facts_to_template()
    questions = ""
    for text in text_list:
        questions += text
        questions += "\n"
    # print(questions)
    return questions


if __name__ == "__main__":
    c = input("continue or not: ")
    while c != '0':
        temp_dev([8, 2])

