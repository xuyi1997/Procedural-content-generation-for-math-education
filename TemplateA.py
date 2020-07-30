import time
import xlrd
import random
from binary_expression_tree import *
<<<<<<< HEAD
import textGenerator
from interval import Interval
=======
from fractions import Fraction
from interval import Interval
import json
from word2vec import Embeddings
print("Loading word embeddings...")
t0 = time.time()
w2v = Embeddings.load("data\enw.npy")
t1 = time.time()
print("Word embeddings loaded in ", t1 - t0)
#
with open('data\word_library.json', 'r') as f:
    data = json.load(fp=f)
database = data

phead = {
        'origin': ["#[#set#]story#"],
        'set': "[quantity_unit:#quantity_unit#][container:#container#][currency:#currency#][food:#food#][ingredient:#ingredient#]"
    }

>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5

def get_operands(num_total, opr_num, opr_col_no, cst_col_no, rows_value):
    # get the operands based on the assistant number in the constraints file
    nums = [0 for _ in range(10)]
    oprands = []
    n1 = n2 = n3 = n4 = n5 = 0
    min_val = []
    max_val = []
    cst_col_no += 1
    i = 0
    while i < num_total*2:
        min_exp = str(rows_value[cst_col_no+i])
        min_val.append(eval(min_exp))
        i += 1
        max_exp = str(rows_value[cst_col_no+i])
        max_val.append(eval(max_exp))
        i += 1

    for i in range(num_total):
        val = random.randint(min_val[i], max_val[i])
        nums[i] = val

    n1, n2, n3, n4, n5, n6 = nums[0], nums[1], nums[2], nums[3], nums[4], nums[5]

    opr_col_no += 1
    for i in range(opr_num):
        opr_exp = str(rows_value[opr_col_no + i])
        operand = eval(opr_exp)
        oprands.append(round(operand, 4))
<<<<<<< HEAD
    for i in range(len(oprands)):
        if oprands[i] > 1 and oprands[i] % 1 == 0:
            oprands[i] = int(oprands[i])
=======

>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
    return oprands


def get_answer(result, result_type, operands):
    # this function is for some KCs that require extra result instead of the operation result itself
    answer = str(result)
    if result - int(result) > 0:
        if result_type == 'remainder':
<<<<<<< HEAD
            is_select = False
=======
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
            intpart = int(result)
            remainder = operands[0] - intpart * operands[1]
            answer = str(intpart) + ' remainder: ' + str(remainder)

    if 'percentage' in result_type:
<<<<<<< HEAD
        is_select = False
=======
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
        result_perc = round(float(result) * 100, 1)
        answer = answer + " percentage: " + str(result_perc) + '%'
    return answer


def get_w1(result, is_frac):
    # get wrong answer based on Rule 1: Similar to right answer
    w1_list = []
    # dicimal numbers
    if result % 1 > 0 and is_frac is False:
        snum = str(result)
        lnum = list(snum)
        idot = lnum.index('.')
        lnum.insert(idot+1, '0')
        s = "".join(lnum)
        w1_list.append(float(s))
        for i in range(min(len(str(result)), 6)):
            snum = str(result)
            lnum = list(snum)
            if snum[i] != '.':
                lnum = list(snum)
                x = int(snum[i]) + 1
                y = int(snum[i]) + 2
                lx = list(lnum)
                lx[i] = str(x)
                sx = "".join(lx)
                w1_list.append(float(sx))
                lx[i] = str(y)
                sx = "".join(lx)
                w1_list.append(float(sx))
                if int(float(snum[i])) > 0:
                    y = int(snum[i]) - 1
                    ly = list(lnum)
                    ly[i] = str(y)
                    sy = "".join(ly)
                    w1_list.append(float(sy))
                if int(float(snum[i])) > 1:
                    y = int(snum[i]) - 2
                    ly = list(lnum)
                    ly[i] = str(y)
                    sy = "".join(ly)
                    w1_list.append(float(sy))

    # Fraction
    elif is_frac is True:
        m = Fraction(result)
        w1_list.append(Fraction(m.numerator, m.denominator+1))
        w1_list.append(Fraction(m.numerator+1, m.denominator))
        w1_list.append(Fraction(m.numerator, m.denominator + 2))
        w1_list.append(Fraction(m.numerator + 2, m.denominator))
        if m.denominator > 2:
            w1_list.append(Fraction(m.numerator, m.denominator - 1))
        if m.numerator > 1:
            w1_list.append(Fraction(m.numerator-1, m.denominator))
    # integers
    else:
        if result > 0 and result % 100 == 0:
            w1_list.append(result/10)
<<<<<<< HEAD
            w1_list.append(result*10)
=======
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
        else:
            snum = str(result)
            for i in range(len(snum)):
                if snum[i] == '.':
                    break
                else:
                    lnum = list(snum)
                    x = int(snum[i]) + 1
                    lx = list(lnum)
                    lx[i] = str(x)
                    sx = "".join(lx)
                    w1_list.append(float(sx))
                    if int(float(snum[i])) > 1:
                        y = int(snum[i]) - 1
                        ly = list(lnum)
                        ly[i] = str(y)
                        sy = "".join(ly)
                        w1_list.append(float(sy))
<<<<<<< HEAD
            w1_list.append(result*10)
=======
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5

    return w1_list


def get_w2(result, operator, operands, is_frac):
    # get wrong answer based on Rule 2: Switch Operator
    lexp = list(integrate(operator, operands))
    loprator = list(operator)
    add = 0
    mul = 0
    iadd = 0
    imul = 0
    res = 0
    for i in range(len(loprator)):
        if loprator[i] in "+-":
            add += 1
            iadd = i
        if loprator[i] == '*/:':
            mul += 1
            imul = i
    if add >= 1 and mul >= 1 and ('(' not in loprator):
        loprator.insert(iadd, '(')
        loprator.insert(iadd+2, ')')
        soperator = "".join(loprator)
        sexp = integrate(soperator, operands)
        tree = BinaryExpressionTree(sexp)
        res = tree.evaluate(is_frac)
        if res < 0 and result > 0:
            res = abs(res)
        return res
    elif '-' in lexp:
        i = lexp.index('-')
        lexp[i] = '+'
        sexp = "".join(lexp)
        tree = BinaryExpressionTree(sexp)
        res = tree.evaluate(is_frac)
        return res
    elif '+' in lexp:
        i = lexp.index('+')
        lexp[i] = '-'
        sexp = "".join(lexp)
        tree = BinaryExpressionTree(sexp)
        res = tree.evaluate(is_frac)
        if res < 0 and result > 0:
            res = abs(res)
        return res
    elif '*' in lexp:
        i = lexp.index('*')
        lexp[i] = '+'
        sexp = "".join(lexp)
        tree = BinaryExpressionTree(sexp)
        res = tree.evaluate(is_frac)
        if res < 0 and result > 0:
            res = abs(res)
        return res
    elif '/' in lexp:
        i = lexp.index('/')
        lexp[i] = '-'
        sexp = "".join(lexp)
        tree = BinaryExpressionTree(sexp)
        res = tree.evaluate(is_frac)
        if res < 0 and result > 0:
            res = abs(res)
        return res
    elif ':' in lexp:
        i = lexp.index(':')
        lexp[i] = '-'
        sexp = "".join(lexp)
        tree = BinaryExpressionTree(sexp)
        res = tree.evaluate(is_frac)
        if res < 0 and result > 0:
            res = abs(res)
        return res
    return res


<<<<<<< HEAD
def get_w3(result, operator, operands, is_frac):
    if operator == '*':
        # Decimal: 12.3*12.4 -> 12*12 + 0.3*0.4
        if operands[0] % 1 > 0 and operands[1] % 1 > 0:
            w3 =  (operands[0] % 1)*(operands[1] % 1) + int(operands[0]) * int(operands[1])
        elif operands[0] % 1 > 0 and operands[1] % 1 == 0:
            w3 = (operands[0] % 1) + int(operands[0]) * int(operands[1])
        elif operands[0] % 1 == 0 and operands[1] % 1 > 0:
            w3 = (operands[1] % 1) + int(operands[0]) * int(operands[1])
        else:
            #integer
            b = max(operands)
            a = min(operands)
            a_tail, b_tail = operands[0] % 10, operands[1] % 10
            if a_tail == b_tail == 0:
                w3 = random.choice(get_w1(a*b, False))
            elif a == a_tail and b == b_tail:
                # 6 * 9 -> 6 * 10 - 9
                if b >= 8 and a != b:
                    w3 = a * b - abs(a - b)
                else:
                    w3 = a * b * 10
            else:
                # 23*45 -> 20*40+3*5
                w3 = (a-a_tail)*(b-b_tail) + max(1, a_tail)*max(1, b_tail)
        if w3 == get_w2(result, operator, operands, is_frac):
            w3 = random.choice(get_w1(result, False))
        return w3

    else:
        # Random generate an answer under some constraints
        if result % 1 > 0 and is_frac is False:
            # decimal
            nint = int(result)
            lnum = len(str(nint))
            if lnum == 1:
                vmax = 10
                vmin = 1
            else:
                vmax = (int(str(nint)[0]) + 1) * pow(10, lnum - 1)
                vmin = (int(str(nint)[0])) * pow(10, lnum - 1)
            return random.randint(vmin, vmax) + result - nint
        elif is_frac is True:
            # fraction
            m = Fraction(result)
            return Fraction(random.randint(1, 9), random.randint(1, 9)) + m
        else:
            # integer
            lnum = len(str(int(result)))
            if lnum == 1:
                vmax = 10
                vmin = 1
            else:
                vmax = (int(str(result)[0]) + 1) * pow(10, lnum - 1)
                vmin = (int(str(result)[0])) * pow(10, lnum - 1)
            return random.randint(vmin, vmax)


def template_equation(data, index, language, is_retrieve):
    table = data.sheets()[0]
    row_no = int(index)
    kc_row_value = table.row_values(row_no)
    kc_des = str(table.cell_value(row_no, table.row_values(0).index("Discription")))
    result_type = str(table.cell_value(row_no, table.row_values(0).index("result_type")))
    # number of operands
    opr_col_no = table.row_values(0).index("operands")
    operands_num = int(table.cell_value(row_no, opr_col_no))
=======
def text_generator(operands, operator):
    # call text generation functions to generate text questions
    from textGenerator import temp_sum, temp_sub, temp_mul, temp_dev
    text = ""
    if '+' in operator:
        text = temp_sum(operands)
    elif '-' in operator:
        text = temp_sub(operands)
    elif '*' in operator:
        text = temp_mul(operands)
    elif ':' in operator:
        text = temp_dev(operands)
    return text

def template_equation(data, index):
    table = data.sheets()[0]
    # number cols
    cols_num = table.ncols
    # Kc_No = input("please enter the KC.no: ")
    first_row_values = table.row_values(0)
    # print("first_row_values:", first_row_values)
    kc_col_no = dc_col_no = op_col_no = result_range_col_no = opr_col_no = cst_col_no = sel_col_no = result_type_col_no = 0
    for col_no in range(cols_num):
        if 'Knowledge component' in first_row_values[col_no]:
            kc_col_no = col_no
        if 'Discription' in first_row_values[col_no]:
            dc_col_no = col_no
        if 'operator' in first_row_values[col_no]:
            op_col_no = col_no
        if 'result_range' in first_row_values[col_no]:
            result_range_col_no = col_no
        if 'result_type' in first_row_values[col_no]:
            result_type_col_no = col_no
        if 'operands' in first_row_values[col_no]:
            opr_col_no = col_no
        if 'constraints' in first_row_values[col_no]:
            cst_col_no = col_no
        if 'select' in first_row_values[col_no]:
            sel_col_no = col_no


    # print(kc_col_no, dc_col_no, op_col_no, opr_col_no, cst_col_no, tp_col_no)
    row_no = int(index)
    kc_row_value = table.row_values(row_no)
    kc_no = table.row(row_no)[kc_col_no].value
    kc_des = str(str(kc_no) + kc_row_value[dc_col_no])
    result_type = str(kc_row_value[result_type_col_no])
    # print("Knowledge Component", int(kc_no), ": ", kc_des)

    # number of operands
    operands_num = int(table.row(row_no)[opr_col_no].value)
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
    generated_operands = []

    # get operators
    predefined_operator = ""
    while len(predefined_operator) < operands_num - 1:
<<<<<<< HEAD
        predefined_operator += str(random.choice(eval(table.cell_value(row_no, table.row_values(0).index("operator")))))
    # print("operator: ", operator)

    result = 0
    result_range = eval(str('Interval' + str(table.cell_value(row_no, table.row_values(0).index("result_range")))))
=======
        predefined_operator += str(random.choice(eval(table.row(row_no)[op_col_no].value)))
    # print("operator: ", operator)

    result = 0
    result_range = eval(str('Interval' + str(table.row(row_no)[result_range_col_no].value)))
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
    # print("result range:", result_range)
    generated_expression = ""

    is_frac = False
    if 'fraction' in result_type:
        is_frac = True

    # number of assistant numbers
<<<<<<< HEAD
    assnum_col_no = table.row_values(0).index("assistant numbers")
    num_in_total = int(table.cell_value(row_no, assnum_col_no))
    while result not in result_range:
        generated_operands = get_operands(num_in_total, operands_num, opr_col_no, assnum_col_no, kc_row_value)
        # print(generated_operands)
        generated_expression = integrate(predefined_operator, generated_operands)
        # print(generated_expression)
        exptree = BinaryExpressionTree(generated_expression)
        result = exptree.evaluate(is_frac)

    if is_frac is False:
        result = round(result, 5)
        if result % 1 == 0:
            result = round(result)
    is_select = True
    correct_answer = get_answer(result, result_type, generated_operands)
=======
    num_in_total = int(table.row(row_no)[cst_col_no].value)
    while result not in result_range:
        generated_operands = get_operands(num_in_total, operands_num, opr_col_no, cst_col_no, kc_row_value)
        generated_expression = integrate(predefined_operator, generated_operands)
        exptree = BinaryExpressionTree(generated_expression)
        result = exptree.evaluate(is_frac)


    if is_frac is False:
        result = round(result, 5)
    correct_answer = get_answer(result, result_type, generated_operands)

    # print("RA: ", result)
    is_select = False
    if kc_row_value[sel_col_no] == 'YES':
        is_select = True
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
    wrong_answers = []
    # generate wrong answers for multiple choice questions
    if is_select is True:
        w2 = get_w2(result, predefined_operator, generated_operands, is_frac)
<<<<<<< HEAD
        answer_list = [result, w2]
        w3 = get_w3(result, predefined_operator, generated_operands, is_frac)
        while w3 in answer_list:
            w3 = get_w3(result, predefined_operator, generated_operands, is_frac)
        answer_list.append(w3)
        w1_list = get_w1(result, is_frac)
        w1 = random.choice(w1_list)
        while w1 in answer_list:
            w1 = random.choice(w1_list)
        answer_list.append(w1)

        if is_frac is not True:
            w1 = round(w1, 5)
            if w1 % 1 == 0: w1 = round(w1)
            w2 = round(w2, 5)
            if w2 % 1 == 0: w2 = round(w2)
            w3 = round(w3, 5)
            if w3 % 1 == 0: w3 = round(w3)
        wa1 = get_answer(w1, result_type, generated_operands)
        wa2 = get_answer(w2, result_type, generated_operands)
        wa3 = get_answer(w3, result_type, generated_operands)
        wrong_answers.append(str(wa1))
        wrong_answers.append(str(wa2))
        wrong_answers.append(str(wa3))
    from textGenerator import entry
    text, img_dir_list = entry(generated_operands, predefined_operator, language, is_retrieve)
    return generated_expression, correct_answer, wrong_answers, text, img_dir_list


if __name__ == "__main__":
    constraints_lib = xlrd.open_workbook("data\constraints.xlsx")
    for index in range(3, 164):
        generated_expression, correct_answer, wrong_answers, text, img_dir_list = template_equation(constraints_lib, index, 'en')
        print(text, generated_expression, correct_answer, wrong_answers, img_dir_list)
=======
        # print("w2: ", w2)
        answer_list = [result, w2]
        w1_list = get_w1(result, is_frac)
        # print("w1_list: ", w1_list)
        w1 = random.choice(w1_list)
        while w1 in answer_list:
            w1 = random.choice(w1_list)
        # print("w1: ", w1)
        answer_list.append(w1)
        w3_list = get_w1(w2, is_frac)
        # print("w3_list: ", w3_list)
        w3 = random.choice(w3_list)
        while w3 in answer_list:
            w3 = random.choice(w3_list)
        # print("w3: ", w3)
        if is_frac is not True:
            w1 = round(w1, 5)
            w2 = round(w2, 5)
            w3 = round(w3, 5)
        wa1 = get_answer(w1, result_type, generated_operands)
        wa2 = get_answer(w2, result_type, generated_operands)
        wa3 = get_answer(w3, result_type, generated_operands)
        wrong_answers.append(str(w1))
        wrong_answers.append(str(w2))
        wrong_answers.append(str(w3))
    text = text_generator(generated_operands, predefined_operator)
    return kc_des, generated_expression, correct_answer, wrong_answers, text


if __name__ == "__main__":
    constraints_lib = xlrd.open_workbook("constraints.xlsx")
    template_equation(constraints_lib, 100)
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5





