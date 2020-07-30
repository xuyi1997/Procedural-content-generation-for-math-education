import json
with open('data\word_library.json', 'r') as f:
    data = json.load(fp=f)
database = data
import tracery
from copy import deepcopy
import random
from tracery.modifiers import base_english
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
class Add(object):

    def __init__(self, operands):
        self.operands = operands
        self.relation = ""
        self.entities = []
        self.story = ""
        self.theme = ""

    def facts_to_template(self):
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
class Sub(object):

    def __init__(self, operands):
        self.operands = operands
        self.relation = ""
        self.entities = []
        self.story = ""
        self.theme = ""

    def facts_to_template(self):
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
        self.relation = ""
        self.entities = []
        self.story = ""
        self.theme = ""

    def facts_to_template(self):
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
class Dev(object):

    def __init__(self, operands):
        self.operands = operands
        self.relation = ""
        self.entities = []
        self.story = ""
        self.theme = ""

    def facts_to_template(self):
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
                temp_list.append(entity)
    replace_word_list = list(set(temp_list))
    candidates = []
    word_score = []
    word_set = []
    for num in range(10 * len(replace_word_list)):
        head = deepcopy(phead)
        head.update(database)
        head['story'] = "-".join(replace_word_list)
        if 'object_class' in head['story']:
            head['set'] += '[#setclass#]'
        set_theme(head, theme)
        set_num_constraints(facts[0]['entities'], head, operands,operator)
        word_list = retreive_words(head)
        score, word_set = get_score(relation_words, word_list, replace_word_list)
        word_score.append(score)
        candidates.append(word_list)
    max_score_index = word_score.index(max(word_score))
    final_word_list = candidates[max_score_index]
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
        if len(word_list) == len(set(word_list)):
            is_reproduce = False

    return word_list


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

