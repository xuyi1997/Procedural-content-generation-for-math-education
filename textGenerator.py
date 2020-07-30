<<<<<<< HEAD
import json
with open('data\word_library.json', 'r') as f:
    data = json.load(fp=f)
database = data
=======
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
import tracery
from copy import deepcopy
import random
from tracery.modifiers import base_english
<<<<<<< HEAD
from numpy import *
from word2vec import Embeddings
import time

import xlrd
import nltk
import inflect
inflect_engine = inflect.engine()
import pattern
from pattern.en import conjugate, PRESENT, SG
conjugate_en, PRESENT_EN, SG_EN = conjugate, PRESENT, SG
import spacy
import nl_core_news_md
from pattern.nl import pluralize,conjugate,PRESENT,SG
pluralize_nl, conjugate_nl, PRESENT_NL, SG_NL = pluralize, conjugate, PRESENT, SG
nlp_dutch = nl_core_news_md.load()
THEME = 'N'
language = 'en'
is_retrive_image = False
Op = ""
print("Loading word embeddings...")
t0 = time.time()
w2v = Embeddings.load("data\\vecs.npy")
t1 = time.time()
print("Word embeddings loaded in ", t1 - t0)
phead = {
        'origin': ["#[#set#]story#"],
        'set': ""
    }

Ncandidates = 20
is_retrieve_img = True
is_img_objnum = False
facts_lib = xlrd.open_workbook("data\Facts_library_en.xlsx")

# retrieve a fact set and end str from facts library
def retrieve_facts(facts_sheets, chosen_facts, operands):
    facts_name_list = facts_sheets.col_values(facts_sheets.row_values(0).index("Facts_set_index"))
    relation_word_list = facts_sheets.col_values(facts_sheets.row_values(1).index("Relation_word"))
    i = facts_name_list.index(chosen_facts)
    endstr = facts_sheets.cell_value(i, facts_sheets.row_values(0).index("End_word"))
    fact_index_list = [i]
    i += 1
    while i < len(facts_name_list) and len(facts_name_list[i]) == 0:
        fact_index_list.append(i)
        i += 1
    facts = []

    for fact_index in fact_index_list:
        f = {'relation': relation_word_list[fact_index], 'entities': []}
        if len(facts_sheets.cell_value(fact_index, facts_sheets.row_values(0).index("Unknown_entity"))) > 0:
            f['Unknown'] = facts_sheets.cell_value(fact_index, facts_sheets.row_values(0).index("Unknown_entity"))
        j = 1
        while len(facts_sheets.cell_value(fact_index, facts_sheets.row_values(1).index("Relation_word") + j)) > 0:
            entity = facts_sheets.cell_value(fact_index, facts_sheets.row_values(1).index("Relation_word") + j)
            if 'operands' in entity:
                f['entities'].append(eval(entity))
            else:
                f['entities'].append(
                    facts_sheets.cell_value(fact_index, facts_sheets.row_values(1).index("Relation_word") + j))
            j += 1
        facts.append(f)
    return facts, endstr
# choose a fact set for addition problem
=======
from TemplateA import w2v, database, phead
from text_templateGenerate import TextTemplateGenerator
from numpy import *

Ncandidates = 20

det_list = ["a", "an", "the", "these", "this"]
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
class Add(object):

    def __init__(self, operands):
        self.operands = operands
        self.relation = ""
        self.entities = []
        self.story = ""
        self.theme = ""

    def facts_to_template(self):
<<<<<<< HEAD
        self.theme = THEME
        operands = self.operands
        # choose fact:
        operands.sort()
        a = operands[0]
        b = operands[1]
        if a % 1 > 0 or a < 1 or b % 1 > 0 or b < 1:
            chosen_facts = "add-4"
        elif a < 20 and b < 20:
            chosen_facts = random.choice(["add-1", "add-3"])
        else:
            chosen_facts = random.choice(["add-2", "add-4"])
        facts_sheets = facts_lib.sheets()[0]
        facts, endstr = retrieve_facts(facts_sheets, chosen_facts, operands)
        text, word_list = generate_text(self.theme, operands, facts, endstr, '+')
        return text, word_list, chosen_facts

# choose a fact set for subtraction problem
=======
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


>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
class Sub(object):

    def __init__(self, operands):
        self.operands = operands
        self.relation = ""
        self.entities = []
        self.story = ""
        self.theme = ""

    def facts_to_template(self):
<<<<<<< HEAD
        self.theme = THEME
        operands = self.operands
        # choose fact:
        a = operands[0]
        b = operands[1]
        if a % 1 > 0 or a < 1 or b % 1 > 0 or b < 1:
            chosen_facts = "sub-2"
        elif a < 20 and b < 20:
            chosen_facts = random.choice(["sub-1", "sub-3"])
        elif a < 100 and b < 100:
            chosen_facts = random.choice(["sub-2", "sub-4"])
        else:
            chosen_facts = random.choice(["sub-2"])
        facts_sheets = facts_lib.sheets()[1]
        facts, endstr = retrieve_facts(facts_sheets, chosen_facts, operands)
        text, word_list = generate_text(self.theme, self.operands, facts, endstr, '-')
        return text, word_list, chosen_facts

# choose a fact set for multiplication problem
class Mul(object):

    def __init__(self, operands):
        self.operands = sort(operands)
=======
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
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
        self.relation = ""
        self.entities = []
        self.story = ""
        self.theme = ""

    def facts_to_template(self):
<<<<<<< HEAD
        self.theme = THEME
        operands = self.operands
        # choose fact:
        a = operands[0]
        b = operands[1]
        if (b % 1 > 0 or b < 1) and (a % 1 > 0 or a < 1):
            return "Sorry, we can't generate text for this equation", []
        elif b % 1 > 0 or b < 1:
            operands = [b, int(a)]
            chosen_facts = "mul-1"
        elif a % 1 > 0 or a < 1:
            operands = [a, int(b)]
            chosen_facts = "mul-1"
        elif a < 20 and b < 20:
            chosen_facts = random.choice(["mul-2", "mul-3"])
        else:
            chosen_facts = random.choice(["mul-1"])
        facts_sheets = facts_lib.sheets()[2]
        facts, endstr = retrieve_facts(facts_sheets, chosen_facts, operands)
        text, word_list = generate_text(self.theme, operands, facts, endstr, '*')
        return text, word_list

# choose a fact set for combined add-mul problem
class Mul2(object):
    def __init__(self, operands):
        self.operands = operands
        self.relation = ""
        self.entities = []
        self.story = ""
        self.theme = ""

    def facts_to_template(self):
        self.theme = THEME
        operands = self.operands
        facts_sheets = facts_lib.sheets()[4]
        facts, endstr = retrieve_facts(facts_sheets, "mul2",operands)
        text, word_list = generate_text(self.theme, self.operands, facts, endstr, '*+*')
        return text, word_list

# choose a fact set for devision problem
=======
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


>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
class Dev(object):

    def __init__(self, operands):
        self.operands = operands
        self.relation = ""
        self.entities = []
        self.story = ""
        self.theme = ""

    def facts_to_template(self):
<<<<<<< HEAD
        self.theme = THEME
        operands = self.operands
        # choose fact:
        a = operands[0]
        b = operands[1]
        # a : b = z ,b must be integers
        if b % 1 > 0 or b < 1:
            operands = [b, a]
            chosen_facts = "dev-3"
        elif a % 1 > 0 or a < 1:
            chosen_facts = "dev-3"
        elif a < 40 and b < 20:
            chosen_facts = random.choice(["dev-1", "dev-2"])
        elif a > 50 and b < 10:
            chosen_facts = "dev-4"
        else:
            chosen_facts = random.choice(["dev-3"])
        facts_sheets = facts_lib.sheets()[3]
        facts, endstr = retrieve_facts(facts_sheets, chosen_facts, operands)
        text, word_list = generate_text(self.theme, self.operands, facts, endstr, ':')
        return text, word_list


def generate_text(theme, operands, facts, endstr, operator):
    fact_list = deepcopy(facts)
    # print(facts)
    # print(fact_list)
    from text_templateGenerate import template_decider
    text_template = template_decider(fact_list, language)
    s_text = str(text_template)
    temp_list = []
    relation_words = []
    for fact in facts:
        # print(temp_list)
        relation_words.append(fact['relation'])
        for entity in fact['entities']:
            # print(entity)
            if ' ' in str(entity):
                for item in str(entity).split(' '):
                    if '#' in item:
                        temp_list.append(item)
            elif '#' in str(entity):
=======
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
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
                temp_list.append(entity)
    replace_word_list = list(set(temp_list))
    candidates = []
    word_score = []
<<<<<<< HEAD
    word_set = []
    for num in range(10 * len(replace_word_list)):
=======
    for num in range(20 * len(replace_word_list)):
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
        head = deepcopy(phead)
        head.update(database)
        head['story'] = "-".join(replace_word_list)
        if 'object_class' in head['story']:
            head['set'] += '[#setclass#]'
        set_theme(head, theme)
<<<<<<< HEAD
        set_num_constraints(facts[0]['entities'], head, operands,operator)
        word_list = retreive_words(head)
        score, word_set = get_score(relation_words, word_list, replace_word_list)
=======
        # ("head1", head)
        set_num_constraints(head, operands)
        # print("head2", head)
        word_list = retreive_words(head)
        score = get_score(relation_words, word_list)
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
        word_score.append(score)
        candidates.append(word_list)
    max_score_index = word_score.index(max(word_score))
    final_word_list = candidates[max_score_index]
<<<<<<< HEAD
    score, word_set = get_score(relation_words, final_word_list, replace_word_list)
    # print("final_word:", final_word_list)
    final_dictionary = dict(zip(replace_word_list, final_word_list))
    for item in replace_word_list:
        wr = final_dictionary[item]
        wf = ''
        if language == 'nl':
            from googletrans import Translator
            translator = Translator()
            translate_word_list = []
            if '_' in wr:
                translate_word_list = wr.split('_')
            else:
                translate_word_list.append(wr)
            print("translate: ", translate_word_list)
            for w in translate_word_list:
                if len(wf) > 0:
                    wf += '_'
                wf += translator.translate(w, dest=language).text
        elif language == 'en':
            wf = wr
        s_text = s_text.replace(str(item), wf)
    tl = s_text.split(" ")
    # indefinite word
    while '$det' in tl:
        i = tl.index('$det')
        if language == 'en':
            tl[i] = 'a'
            if str(tl[i+1])[0] in ['a', 'e', 'i', 'o'] or str(tl[i+1]) is 'hour':
                tl[i] = 'an'
        elif language == 'nl':
            tl[i] = 'een'

    s_text = " ".join(tl)
    s_text += " " + endstr + "?"
    s_text = s_text.replace("_", " ")
    s_text = s_text.replace("  ", " ")
    print(s_text)
    return s_text, word_set
=======
    final_dictionary = dict(zip(replace_word_list, final_word_list))
    text_template = TextTemplateGenerator(fact_list).decider()
    # print(text_template)
    final_text = str(text_template)
    for item in replace_word_list:
        final_text = final_text.replace(str(item), str(final_dictionary[item]))
    final_text += endstr
    # print(final_text)
    return final_text
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5


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


<<<<<<< HEAD
def set_num_constraints(entities, head, operands, operator):
    a, b = operands[0], operands[1]
    # for decimals
    if a % 1 > 0 or b % 1 > 0 or a < 1 or b < 1 or ('euro' in entities):
        # set price constraints
        if 'object_class' not in head['story']:
            if operator == ':':
                a = operands[0]/operands[1]
            if a <= 2: head['set'] += "[object1: #price_2#]"
            elif 2 < a <= 10: head['set'] += "[object1: #price_10#]"
            elif 10 < a <= 100: head['set'] += "[object1: #price_100#]"
            elif 100 < a <= 1000: head['set'] += "[object1: #price_1000#]"
            else: head['set'] += "[object1: #price_10000#]"
            if b <= 2: head['set'] += "[object2: #price_2#]"
            elif 2 < b <= 10: head['set'] += "[object2: #price_10#]"
            elif 10 < b <= 100: head['set'] += "[object2: #price_100#]"
            elif 100 < b <= 1000: head['set'] += "[object2: #price_1000#]"
            else: head['set'] += "[object2: #price_10000#]"
    # for integers set quantity constraints
    else:

        if 'object_class' not in head['story']:
            if a <= 10 and b <= 10:
                head['set'] += "[object1: #obj_10#][object2: #obj_10#]"
            elif a <= 20 and b <= 20:
                head['set'] += "[object1: #obj_20#][object2: #obj_20#]"
            elif 20 < a <= 100 and 20 < b <= 100:
                head['set'] += "[object1: #obj_100#][object2: #obj_100#]"
            else:
                head['set'] += "[object1: #obj_1000#][object2: #obj_1000#]"

=======
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
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5


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
<<<<<<< HEAD
        if len(word_list) == len(set(word_list)):
=======
        if len(word_list) != len(set(word_list)):
            print("Duplicates! Need Reproduce")
        else:
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
            is_reproduce = False

    return word_list


<<<<<<< HEAD
def get_score(relation_words, original_word_list, replace_word_list):
    word_list = deepcopy(original_word_list)
    re_word_list = deepcopy(replace_word_list)
    new_word_list = []
    # for relation_word in relation_words:
    #     word_list.append(relation_word)
    # print(word_list)
    score_list = []
    i, l = 0, len(word_list)
    print(word_list)
    while l >= 1 and i < l:
        if '_' in word_list[i]:
            p = word_list[i].find('_')
            word_list[i] = word_list[i][p + 1:len(word_list[i])]
        elif 'character' in re_word_list[i]:
            word_list.pop(i)
            re_word_list.pop(i)
            l -= 1
            continue
        i += 1
    word_list = list(set(word_list))
    if len(word_list) > 1:
        for i in range(len(word_list)):
            j = i + 1
            while j < len(word_list):
                word1 = word_list[i].strip()
                word2 = word_list[j].strip()
                score_list.append(w2v.similarity(word1, word2))
                j += 1
    elif len(word_list) == 1:
        score_list.append(0)
    score = mean(score_list)
    return score, word_list


def entry(operands, operator, l, i):
    global language, is_retrieve_img
    language = l
    is_retrieve_img = i
    if language == 'nl':
        global facts_lib
        facts_lib = xlrd.open_workbook("data\Facts_library_nl.xlsx")
    from imageGenerator import image_generator, image_splice
    word_list = []
    is_img_objnum = False
    img_dir_list = []
    Op = operator
    question = "Sorry, we can not generate text for this equation"
    if len(operator) == 1:
        word_list = []
        if '+' in operator:
            add_text = Add(operands)
            question, word_list, chosen_facts = add_text.facts_to_template()
            print(word_list)
            if 1 <= operands[0] <= 10 and 1 <= operands[1] <= 10 and operands[0] % 1 == 0 and operands[1] % 1 == 0:

                img_dir_list.append(image_splice(word_list[0], int(operands[0]), int(operands[1])))
        elif '-' in operator:
            sub_text = Sub(operands)
            question, word_list, chosen_facts = sub_text.facts_to_template()
            if 1 <= operands[0] <= 10 and 1 <= operands[1] <= 10 and operands[0] % 1 == 0 and operands[1] % 1 == 0:
                img_dir_list.append(image_generator(word_list[0], int(operands[0])))
        elif '*' in operator:
            mul_text = Mul(operands)
            question, word_list = mul_text.facts_to_template()
        elif ':' in operator:
            dev_text = Dev(operands)
            question, word_list = dev_text.facts_to_template()
    elif operator == "*+*":
        mul_text = Mul2(operands)
        question, word_list = mul_text.facts_to_template()
    if len(img_dir_list) == 0 and len(word_list) > 0 and is_retrieve_img:
        from retrieve_image import image_retrieve
        objs = " ".join(word_list)
        print("retrieve objs: ", objs)
        img_dir_list = image_retrieve(objs)
    question = eval('pos_correct_' + language + '(question)')
    return question, img_dir_list

def pos_correct_nl(s_text):
    doc = nlp_dutch(s_text)
    pos_set = []
    for token in doc:
        pos_set.append((str(token), str(token.pos_)))
    print(pos_set)
    f_text = str(pos_set[0][0]) + ' '
    index = 1
    while index < len(pos_set):
        pos = pos_set[index]
        pre_pos = pos_set[index - 1]
        pre_pre_pos = pos_set[max(0, index - 2)]
        post_pos = pos_set[min(len(pos_set) - 1, index + 1)]
        post_post_pos = pos_set[min(len(pos_set) - 1, index + 2)]
        index += 1
        # 3-rd single present
        if (pos[1] in ['VERB', 'AUX'] and pre_pos[1] in ['NOUN', 'PROPN'] and post_post_pos[0] not in ['en'] and pre_pre_pos[0] not in ['en','Hoeveel'] and post_pos[0] not in ['er'])\
                or (pos[1] in ['VERB', 'AUX'] and post_pos[1] in ['NOUN', 'PROPN'] and post_post_pos[1] not in ['en', 'Hoeveel'])\
                or (pos[1] in ['VERB', 'AUX'] and post_pos[1] in ['elke']):
            f_text += conjugate_nl(verb=pos[0], tense=PRESENT_NL, number=SG_NL)
            f_text += ' '
            continue
        elif pos[1] in ['VERB', 'AUX'] and post_pos[1] in ['NOUN', 'PROPN']:
            f_text += conjugate_nl(verb=pos[0], tense=PRESENT_NL, number=SG_NL)
            f_text += ' '
            continue
        # pluralize
        elif pos[1] == 'NOUN' and (
                (pre_pos[1] == 'NUM' and pre_pos[0] not in ['een', '1'] and index == len(pos_set))
                or (pre_pos[1] == 'NUM' and pre_pos[0] not in ['een', '1'] and post_pos[1] not in ['NOUN'])
                or (pre_pre_pos[1] == 'NUM' and pre_pre_pos[0] not in ['een', '1'] and pre_pos[0] not in ['ml', 'l'])
                or (pre_pos[1] in ['NOUN', 'ADJ'] and pre_pre_pos[0] in ['many', 'some', 'several', 'more'])
                or (pre_pos[0] in ['many', 'some', 'several', 'more'] and post_pos[1] not in ['NOUN'])
        ):
            f_text += pluralize_nl(pos[0]).replace('\'', '')
            f_text += ' '
            continue
        # hebben....done
        elif pos[1] == 'AUX' and post_pos[1] == 'ADJ':
            pos_set.remove(post_pos)
            pos_set.append(post_pos)
            post_pos = pos_set[min(len(pos_set) - 1, index)]
            print(post_pos)
            if post_pos[1] == 'PROPN':
                print(conjugate_nl(verb=pos[0], tense=PRESENT_NL, number=SG_NL))
                f_text += conjugate_nl(verb=pos[0], tense=PRESENT_NL, number=SG_NL)
                f_text += ' '
                continue
        f_text += pos[0]
        f_text += ' '

    print(f_text)
    return f_text


def pos_correct_en(s_text):
    text_token = nltk.word_tokenize(s_text)
    pos_set = nltk.pos_tag(text_token)
    f_text = str(pos_set[0][0]) + ' '
    index = 1
    while index < len(pos_set):
        pos = pos_set[index]
        pre_pos = pos_set[index-1]
        pre_pre_pos = pos_set[max(0, index-2)]
        post_pos = pos_set[min(len(pos_set)-1, index+1)]
        index += 1
        if pos[1] in ['VB','VBP'] and pre_pos[1] in ['NNP', 'NNS','NN'] and (pre_pre_pos[0] not in ['does','and','many']):
            f_text += conjugate_en(verb=pos[0], tense=PRESENT_EN, number=SG_EN)
            f_text += ' '
            continue
        # pluralize
        elif pos[1] == 'NN' and (
                (pre_pos[1] == 'CD' and pre_pos[0] not in ['one', 'One', '1'] and post_pos[1] not in ['NN'])
                or (pre_pre_pos[1] == 'CD' and pre_pre_pos[0] not in ['one', 'One', '1'] and pre_pos[0] not in ['ml', 'l'])
                or (pre_pos[1] in ['NN', 'JJ'] and pre_pre_pos[0] in ['many', 'some', 'several','more'])
                or (pre_pos[0] in ['many', 'some', 'several','more'] and post_pos[1] not in ['NN'])
        ):
            f_text += inflect_engine.plural(pos[0])
            f_text += ' '
            continue
        f_text += pos[0]
        f_text += ' '

    # print(s_text)
    return f_text
if __name__ == "__main__":
    c = input("continue or not: ")
    while c != '0':
        text = entry([2, 5], '+', 'en', False)
        print(text)
        c = input("continue or not: ")
=======
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
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5

