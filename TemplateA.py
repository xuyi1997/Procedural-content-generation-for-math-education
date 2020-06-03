import time
import xlrd
import random
from binary_expression_tree import *
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

    return oprands


def get_answer(result, result_type, operands):
    # this function is for some KCs that require extra result instead of the operation result itself
    answer = str(result)
    if result - int(result) > 0:
        if result_type == 'remainder':
            intpart = int(result)
            remainder = operands[0] - intpart * operands[1]
            answer = str(intpart) + ' remainder: ' + str(remainder)

    if 'percentage' in result_type:
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
    generated_operands = []

    # get operators
    predefined_operator = ""
    while len(predefined_operator) < operands_num - 1:
        predefined_operator += str(random.choice(eval(table.row(row_no)[op_col_no].value)))
    # print("operator: ", operator)

    result = 0
    result_range = eval(str('Interval' + str(table.row(row_no)[result_range_col_no].value)))
    # print("result range:", result_range)
    generated_expression = ""

    is_frac = False
    if 'fraction' in result_type:
        is_frac = True

    # number of assistant numbers
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
    wrong_answers = []
    # generate wrong answers for multiple choice questions
    if is_select is True:
        w2 = get_w2(result, predefined_operator, generated_operands, is_frac)
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





