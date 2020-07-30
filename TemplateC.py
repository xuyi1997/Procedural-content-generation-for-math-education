import xlrd
import random
import numpy as np
from binary_expression_tree import *
from fractions import Fraction
from interval import Interval
from prettytable import PrettyTable
from copy import deepcopy
from text_templateGenerate import phead, database
<<<<<<< HEAD
from textGenerator import retreive_words, get_score, set_theme, set_num_constraints

integers = ['object1', 'object2', 'gram', 'meter', 'liter', 'width', 'length', 'numerator', 'denominator', 'people', 'object', 'size', 'part', 'whole', 'container', 'amount', 'food', 'unit', 'ingredient', 'number', 'day', 'hour', 'minute', 'second', 'century', 'decade', 'year']

=======
from textGenerator import retreive_words, get_score, set_theme
import pytab

integers = ['object1', 'object2','price', 'unit', 'width', 'length', 'numerator', 'denominator', 'people', 'object', 'size', 'part', 'whole', 'container', 'amount', 'food', 'unit', 'ingredient', 'number', 'day', 'hour', 'minute', 'second', 'century', 'decade', 'year']
replacable = ['object1', 'object2', 'food', 'ingredient']
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5

def get_integer():
    x = random.randint(1, 10)
    y = random.choice([x, x*10, x*100])
    return x


def get_decimal():

    x = random.uniform(1, 10)
<<<<<<< HEAD
    return round(x, 1)
=======
    return round(x, 2)
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5


def get_num(attr):
    n = 0
    int_mode = False
    for i in range(len(integers)):
        if integers[i] in attr:
            int_mode = True
    if int_mode:
        n = get_integer()
    else:
        n = get_decimal()
    return n


def addition_cal(row, note):
    res = ''
    if 'fraction' in note:
        res = str(Fraction(row[0], row[1]))
<<<<<<< HEAD
    elif 'area' in note:
        res = (round(row[0] * row[1], 3))
    elif len(note) > 0:
        res = (round(row[1]/row[0], 3))
    return res


def text_question(question_type, attr_list, values):
    import plotly.graph_objects as go
    col_num = len(values)
    question = ""
    answer = ""

    if 'conversion' in question_type:
        text = "Fill in the box: "
        index = random.sample(list(range(0, len(attr_list))), 2)
        question = text + '\n' + str(values[index[0]][0]) + attr_list[index[0]] + " = " + "_" + attr_list[index[1]]
        answer = str(values[index[1]][0])
        fig = go.Figure(data=[go.Table(header=dict(values=attr_list),
                                       cells=dict(values=values))
                              ])
    elif 'fill' in question_type:
        from textGenerator import generate_text
        operands = [values[0][0], values[1][0], values[0][1]]
        question = ""
        if attr_list[1] == "price":
            fa = {'relation': "bought",
                  'entities': ["#character1#", operands[0], attr_list[0].strip("number of"), operands[1],
                               "euro"]}
            fb = {'relation': "needs", 'entities': ["#character1#", operands[2], attr_list[0].strip("number of") + 's']}
            facts1 = [fa, fb]
            facts = facts1
            context = generate_text('N', operands, facts, "", ":")
            question += "How much is it? Please fill in the empty box."
        else:
            question += "Please fill in the empty box."
        answer = str(values[len(values)-1][len(values[0])-1])
        values[len(values)-1][len(values[0])-1] = '?'
        if '.' in str(values[1][0]):
            if len(str(values[1][0])) - str(values[1][0]).index('.') == 2:
                values[1][0] = str(values[1][0]).replace('.', ',') + '0'
            else:
                values[1][0] = str(values[1][0]).replace('.', ',')
        fig = go.Figure(data=[go.Table(header=dict(values=attr_list),
                                       cells=dict(values=values))
                              ])
    elif 'cal' in question_type:
        question = "Look at the table and calculate the "
        ratio_dict = {'speed': 'average speed',
                      'price': 'price per' + attr_list[0], 'population': 'population density'}
        for item in ratio_dict.keys():
            if item in question_type:
                question += ratio_dict[item]
                break
        answer = str(values[1][0] / values[0][0])
        fig = go.Figure(data=[go.Table(header=dict(values=attr_list),
                                       cells=dict(values=values))
                              ])
    else:
        fig = go.Figure(data=[go.Table(header=dict(values=attr_list),
                                       cells=dict(values=values))
                              ])

    return question, answer, fig


def template_ratio_table(data, index):
    table = data.sheets()[2]
    row_no = int(index)
    kc_id = str(table.cell_value(row_no, table.row_values(0).index("Knowledge component")))
    kc_des = str(table.cell_value(row_no, table.row_values(0).index("Description")))
    question_type = str(table.cell_value(row_no, table.row_values(0).index("Question type")))
    num_attr = int(float(table.cell_value(row_no, table.row_values(0).index("Attributes"))))
    num_rows = int(float(table.cell_value(row_no, table.row_values(0).index("Number of rows"))))
    note = str(table.cell_value(row_no, table.row_values(0).index("Note")))
    values = []
    heading_line = []
    attr_list = []
    for i in range(num_attr):
        heading_line.append(str(table.cell_value(row_no, 1+i+table.row_values(0).index("Attributes"))))
        attr_list.append(str(table.cell_value(row_no, 1+i+table.row_values(0).index("Attributes"))))
=======
    elif 'total' in note:
        res = str(round(row[0] * row[1], 3))
    elif 'area' in note:
        res = str(round(row[0] * row[1], 3))
    elif len(note) > 0:
        res = str(round(row[1]/row[0], 3))
    return res


def template_ratio_table(data, index):
    table = data.sheets()[2]
    # number of rows and cols
    cols_num = table.ncols
    index_row = table.row_values(0)
    # print("first_row_values:", index_row)
    kc_col_no = dc_col_no = attr_col_no = ratio_col_no = rnum_col_no = note_col_no = 0
    for col_no in range(cols_num):
        if 'Knowledge component' in index_row[col_no]:
            kc_col_no = col_no
        if 'Description' in index_row[col_no]:
            dc_col_no = col_no
        if 'Attribute' in index_row[col_no]:
            attr_col_no = col_no
        if 'Ratio' in index_row[col_no]:
            ratio_col_no = col_no
        if 'row' in index_row[col_no]:
            rnum_col_no = col_no
        if 'Note' in index_row[col_no]:
            note_col_no = col_no
    row_no = int(index)
    kc_row_value = table.row_values(row_no)
    kc_no = kc_row_value[kc_col_no]
    kc_des = str(str(int(float(kc_no))) + " " + kc_row_value[dc_col_no])
    num_attr = int(float(kc_row_value[attr_col_no]))
    num_rows = int(float(kc_row_value[rnum_col_no]))
    values = []
    heading_line = []
    attr_list = []
    note = str(kc_row_value[note_col_no])
    for i in range(num_attr):
        heading_line.append(str(kc_row_value[attr_col_no+1+i]))
        attr_list.append(str(kc_row_value[attr_col_no+1+i]))
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
    if len(note) > 1:
        heading_line.append(note)
    ratio_list = []
    for i in range(len(heading_line)):
        values.append([])
    for i in range(num_attr-1):
<<<<<<< HEAD
        ratio_list.append(str(table.cell_value(row_no, i + table.row_values(0).index("Ratios"))))
=======
        ratio_list.append(str(kc_row_value[ratio_col_no+i]))
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5

    # when the ratio is randomly generated
    if 'Interval' in ratio_list[0]:
        ratio_table = PrettyTable(heading_line)
        # Firstly, get the first row
        first_row = []
        num = [1 for i in range(num_attr)]
        for l in range(num_attr-1):
            ratio_range = ratio_list[l]
            while num[l+1] == num[l] or float(num[l+1]/num[l]) not in eval(ratio_range):
                num[l] = get_num(attr_list[l])
                num[l+1] = get_num(attr_list[l+1])
        for l in range(len(num)):
            first_row.append(num[l])

        if len(heading_line) > num_attr:
            first_row.append(addition_cal(first_row, note))
        for l in range(len(first_row)):
            values[l].append(first_row[l])
        ratio_table.add_row(first_row)

        # Next, get the rest rows:
        mul_list = []
        for r in range(num_rows-1):
            mul = 1
            while (mul == 1) or (mul in mul_list):
                mul = random.randint(2, 10)
            mul_list.append(mul)
            row = []
            for l in range(num_attr):
                num = mul * first_row[l]
                row.append(round(num, 3))
            if len(heading_line) > num_attr:
                row.append(addition_cal(row, note))
            ratio_table.add_row(row)
            for l in range(len(row)):
                values[l].append(row[l])

    else:
        ratio_table = PrettyTable()
        # if the ratio value is a clear number, we firsly generate the first line of the table
        first_line = []
        for r in range(num_rows):
            num = 0
            while (num == 0) or num in first_line:
                num = get_num(attr_list[0])
            first_line.append(round(num, 3))
        ratio_table.add_column(heading_line[0], first_line)
        values[0] = first_line
        pre_line = first_line
        for l in range(num_attr-1):
            column = []
            ratio = float(ratio_list[l])
            for r in range(num_rows):
                num = pre_line[r] * ratio
                column.append(round(num, 3))
            pre_line = column
            values[l+1] = column
            ratio_table.add_column(heading_line[l+1], column)
<<<<<<< HEAD

=======
    print(ratio_table)
    print(values)
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
    replace_word_list = []
    is_replace = False
    for attr in attr_list:
        if '#' in attr:
            is_replace = True
        replace_word_list.append(attr)
    if is_replace:
        candidates = []
        word_score = []
        for num in range(20):
            head = deepcopy(phead)
            head.update(database)
            head['story'] = "-".join(replace_word_list)
            if 'object1' in head['story'] and 'object2' in head['story']:
                head['set'] += '[#setclass#]'
            set_theme(head, 'N')
<<<<<<< HEAD
            set_num_constraints(['euro'], head, [values[0][0], values[1][0]], ':')
            word_list = retreive_words(head)
            score, word_set = get_score([], word_list, replace_word_list)
=======
            word_list = retreive_words(head)
            score = get_score([], word_list)
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
            word_score.append(score)
            candidates.append(word_list)
        max_score_index = word_score.index(max(word_score))
        final_word_list = candidates[max_score_index]
        attr_list = final_word_list
<<<<<<< HEAD
    if len(note) > 1:
        attr_list.append(note)
    for l in range(len(values)):
        for r in range(len(values[0])):
            if '.' in str(values[l][r]) and values[l][r] % 1 == 0:
                values[l][r] = round(values[l][r])
    question, answer, fig= text_question(question_type, attr_list, values)
    img_dir = "ratio_table" + "\\" + "ratio_table_" + kc_id + ".png"
    fig.write_image(img_dir)
    return question, answer, img_dir
=======

    print("attributes: ", attr_list)
    if len(note) > 1:
        attr_list.append(note)
    import plotly.graph_objects as go

    fig = go.Figure(data=[go.Table(header=dict(values=attr_list),
                                   cells=dict(values=values))
                          ])

    return kc_des, ratio_table, fig

>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5


if __name__ == "__main__":
    constraints_lib = xlrd.open_workbook("data\constraints.xlsx")
<<<<<<< HEAD
    for index in range(3, 60):
        question, answer, img_dir = template_ratio_table(constraints_lib, index)
        print(question)
        print(answer)
        print(img_dir)

=======
    index = input("Please input KC ID:")
    while index != '0':
        kc_des, ratio_table,fig = template_ratio_table(constraints_lib, index)
        dir = "table" + str(index) + ".png"
        fig.write_image(dir)
        from PIL import Image
        import matplotlib.pyplot as plt

        img = Image.open(dir)
        plt.figure("fig")
        plt.imshow(img)
        plt.show()
        index = input("Please input KC ID:")
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5




