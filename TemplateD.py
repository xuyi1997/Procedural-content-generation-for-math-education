import xlrd
import random
from binary_expression_tree import *
from fractions import Fraction
from interval import Interval
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable

def get_total():
    x = random.randint(1, 9)
    y = random.randint(10, 20)
    mul_x = random.choice([10, 100])
    t = random.choice([x * mul_x, 5 * y])
    return t


def get_percentage(kc_des, perc_range):
    perc = 0
    if 'discount' in kc_des:
        perc = 5 * random.randint(10, 19)
    else:
        perc = eval(str('random.randint' + perc_range))
    return perc

<<<<<<< HEAD
def generate_num_list(table, index):
    row_no = int(index)
    integer_mode = False
    if 'yes' in str(table.cell_value(row_no, table.row_values(0).index("integer only"))):
        integer_mode = True

    num_in_total = int(float(table.cell_value(row_no, table.row_values(0).index("Percentages"))))
    vType = str(table.cell_value(row_no, table.row_values(0).index("value type")))
    perc_list = []
    perc_range_list = []
    for i in range(num_in_total):
        perc_range_list.append(str(table.cell_value(row_no, 1 + i + table.row_values(0).index("Percentages"))))
    num_list = []
    total_type = str(table.cell_value(row_no, table.row_values(0).index("Total Value")))
    text = ""
=======

def template_perc_chart(data, index):
    table = data.sheets()[3]
    # number of rows and cols
    rows_num = table.nrows
    cols_num = table.ncols
    first_row_values = table.row_values(0)
    # print("first_row_values:", first_row_values)
    kc_col_no = dc_col_no = tol_col_no = res_col_no = cType_col_no = pc_col_no  = 0
    for col_no in range(cols_num):
        if 'Knowledge component' in first_row_values[col_no]:
            kc_col_no = col_no
        if 'Discription' in first_row_values[col_no]:
            dc_col_no = col_no
        if 'Total' in first_row_values[col_no]:
            tol_col_no = col_no
        if 'result' in first_row_values[col_no]:
            res_col_no = col_no
        if 'chart' in first_row_values[col_no]:
            cType_col_no = col_no
        if 'Percentage' in first_row_values[col_no]:
            pc_col_no = col_no
    row_no = int(index)
    kc_row_value = table.row_values(row_no)
    # print("kc_row_value", kc_row_value)
    kc_no = kc_row_value[kc_col_no]
    kc_des = kc_row_value[dc_col_no]
    print(int(float(kc_no)), kc_des)
    integer_mode = False
    if 'yes' in str(kc_row_value[res_col_no]):
        integer_mode = True
    cType = str(kc_row_value[cType_col_no])
    # print(cType)
    num_in_total = int(kc_row_value[pc_col_no])
    perc_list = []
    perc_range_list = []
    for i in range(num_in_total):
        perc_range_list.append(str(kc_row_value[pc_col_no + 1 + i]))
    num_list = []
    total_type = str(kc_row_value[tol_col_no])
    total = 0
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5

    if total_type.isdigit():
        total = int(float(total_type))
    elif '(' in total_type:
        total = eval('random.rand' + total_type)
    else:
        total = get_total()

<<<<<<< HEAD
=======

>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
    if integer_mode == True:
        if num_in_total == 1:
            num_list = []
            num = 0
<<<<<<< HEAD
            while float(100 * num / total) not in eval('Interval' + perc_range_list[0]):
=======
            while float(100 * num/total) not in eval('Interval' + perc_range_list[0]):
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
                num = random.randint(1, total)
            num_list.append(num)
        elif num_in_total > 1:
            redo = True
            while redo:
                num_list = []
                redo = False
                temp = []
                temp.append(0)
                for i in range(num_in_total - 1):
                    temp.append(random.randint(1, total))
                temp.append(total)
                temp.sort()
                for i in range(len(temp) - 1):
                    num_list.append(temp[i + 1] - temp[i])
                for i in range(len(num_list)):
                    if 100 * num_list[i] / total not in eval('Interval' + perc_range_list[i]):
                        redo = True
    else:
        if num_in_total == 1:
            num_list = []
            num = 0
            perc = 0
<<<<<<< HEAD
            while float(100 * num / total) not in eval('Interval' + perc_range_list[0]):
                print(perc_range_list)
                perc = get_percentage(vType, perc_range_list[0])
                print(perc)
=======
            while float(100 * num/total) not in eval('Interval' + perc_range_list[0]):
                perc = get_percentage(kc_des, perc_range_list[0])
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
                num = total * perc * 0.01
            perc_list.append(perc)
            num_list.append(round(num, 3))
        elif num_in_total > 1:
            num_list = []
            redo = True
            while redo:
                perc_list = []
                redo = False
                temp = []
                temp.append(0)
                for i in range(num_in_total - 1):
                    temp.append(random.randint(1, 100))
                temp.append(100)
                temp.sort()
                for i in range(len(temp) - 1):
                    perc_list.append(temp[i + 1] - temp[i])
                for i in range(len(perc_list)):
                    if perc_list[i] not in eval('Interval' + perc_range_list[i]):
                        redo = True
            for i in range(len(perc_list)):
                num_list.append(round(total * perc_list[i] * 0.01, 3))
<<<<<<< HEAD
    text = text + "Total: " + str(total) + '\n'
    return text, num_list, total

def template_perc_chart(data, index):
    row_no = int(index)
    table = data.sheets()[3]
    kc_id = str(table.cell_value(row_no, table.row_values(0).index("Knowledge Component")))
    cType = str(table.cell_value(row_no, table.row_values(0).index("chart type")))
    text, num_list, total = generate_num_list(table, index)
    vType = str(table.cell_value(row_no, table.row_values(0).index("value type")))
    img_dir = ""
    if len(cType) > 0:
        img_dir = "percentage_chart" + "\\" + "perc_" + kc_id + ".png"
    if 'fraction' in vType:
        frac_list = []
        for i in range(len(num_list)):
            frac_list.append(str(Fraction(num_list[i], total)))
        text = text + "Fraction: " + str(frac_list) + '\n'
    if 'percent' in vType:
=======
    print("Total: ", total)

    if 'fraction' in kc_des:
        frac_list = []
        for i in range(len(num_list)):
            frac_list.append(str(Fraction(num_list[i], total)))
        print("Fraction: ", frac_list)
    if 'percent' in kc_des:
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
        perc_list = []
        if len(perc_list) == 0:
            for i in range(len(num_list)):
                perc_list.append(str(round(100*num_list[i]/total, 2)) + '%')
<<<<<<< HEAD
        text = text + "Percentage: " + str(perc_list) + '\n'
    if 'discount' in vType:
=======
        print("Percentage: ", perc_list)
    if 'discount' in kc_des:
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
        discount_list = []
        if len(discount_list) == 0:
            for i in range(len(num_list)):
                discount_list.append(str(100 - round(100 * num_list[i] / total, 2)) + '%')
<<<<<<< HEAD
        text = text + "Discount: " + str(discount_list) + '\n'
    text = text + "numbers: " + str(num_list) + '\n'

    facts_lib = xlrd.open_workbook("data\Facts_library_en.xlsx")
    text_sheets = facts_lib.sheets()[7]
    colors = ['blue', 'green', 'red', 'yellow', 'pink']
    if 'pie' in cType:
        i = text_sheets.col_values(0).index('pie')
        attrs = eval(text_sheets.cell_value(i, text_sheets.row_values(0).index('attributes list')))
        plt.figure()
        plt.subplot(1,3,1)
        plt.pie(num_list, colors=colors)
        text2, num_list2, total2 = generate_num_list(table, index)
        plt.subplot(1, 3, 2)
        plt.pie(num_list2, colors=colors)
        text3, num_list3, total3 = generate_num_list(table, index)
        plt.subplot(1, 3, 3)
        plt.pie(num_list3, colors=colors)
        plt.tight_layout()

        plt.axis('equal')

        plt.savefig(img_dir)
        plt.close()
        text += text_sheets.cell_value(i, text_sheets.row_values(0).index('text')) + '\n'
        for num in num_list:
            text += str(num) + " choose "
            text += attrs[num_list.index(num)] + '\n'
        text += text_sheets.cell_value(i, text_sheets.row_values(0).index('question')) + '\n'
    if 'bar' in cType:
        x = np.arange(len(num_list)) + 1
        i = text_sheets.col_values(0).index('bar')
        attrs = eval(text_sheets.cell_value(i, text_sheets.row_values(0).index('attributes list')))
        plt.bar(x, num_list, alpha=0.9, width=0.35, color=colors, label='one', lw=1)
        plt.xticks(x, [], size='small')
        plt.grid(True, linestyle=':', color='grey', alpha=0.6)
        plt.savefig(img_dir)
        plt.close()
        text = str(sum(num_list)) + " " + text_sheets.cell_value(i, text_sheets.row_values(0).index('text')) + '\n'
        for k in range(len(num_list)):
            text += str(num_list[k]) + " choose " + attrs[k] + '\n'
        text += text_sheets.cell_value(i, text_sheets.row_values(0).index('question')) + " " + random.choice(attrs)

    if 'table' in cType:
        i = text_sheets.col_values(0).index('table')
        attrs = eval(text_sheets.cell_value(i, text_sheets.row_values(0).index('attributes list')))
        values = []
        for i in range(len(num_list)):
            values.append([num_list[i]])
        import plotly.graph_objects as go
        fig = go.Figure(data=[go.Table(header=dict(values=attrs[0:len(num_list)]),
                                       cells=dict(values=values))
                              ])
        fig.write_image(img_dir)
    return text, img_dir
=======
        print("Discount: ", discount_list)
    print("numbers: ", num_list)

    if 'pie' in cType:
        plt.pie(num_list)
        plt.axis('equal')
        plt.show()

    if 'bar' in cType:
        x = np.arange(len(num_list)) + 1
        plt.bar(x, num_list, alpha=0.9, width=0.35, facecolor = 'lightskyblue', edgecolor = 'white', label='one', lw=1)
        plt.show()

    if 'table' in cType:

        attr = ['A', 'B', 'C', 'D', 'E']
        table = PrettyTable(['Object', 'Number'])
        for i in range(len(num_list)):
            table.add_row([attr[i], str(num_list[i])])
        table.add_row(["Total", total])
        print(table)
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5


if __name__ == "__main__":
    constraints_lib = xlrd.open_workbook("data\constraints.xlsx")
<<<<<<< HEAD
    for index in range(2, 24):
        text, img_dir = template_perc_chart(constraints_lib, index)
        print(text)

=======
    template_perc_chart(constraints_lib, 22)
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5








