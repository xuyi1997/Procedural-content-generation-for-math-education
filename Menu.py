import xlrd
import json
import xlwt
from TemplateA import template_equation
from TemplateB import template_number_sequence
from TemplateC import template_ratio_table
from TemplateD import template_perc_chart

from numpy import *

def menu(constraints_lib, kc_id):
    if kc_id in kc[0]:
        index = kc[0].index(kc_id) + 3
        kc_des, generated_expression, RA, WA, text = template_equation(constraints_lib, index)
        equation = str(generated_expression + ' = ' + '?')
        print(kc_des)
        print(equation)
        print(RA)
        print(WA)
        print(text)

    elif kc_id in kc[1]:
        index = kc[1].index(kc_id) + 2
        output = template_number_sequence(constraints_lib, index)
        print(output)

    elif kc_id in kc[2]:
        index = kc[2].index(kc_id) + 3
        kc_des, ratio_table, fig = template_ratio_table(constraints_lib, index)
        print(kc_des)
        print(ratio_table)
        img_dir = "table_kc" + str(kc_id) + ".png"
        fig.write_image(img_dir)
        from PIL import Image
        import matplotlib.pyplot as plt
        img = Image.open(img_dir)
        plt.figure("fig")
        plt.imshow(img)
        plt.show()

    elif kc_id in kc[3]:
        index = kc[3].index(kc_id) + 2
        template_perc_chart(constraints_lib, index)

    # elif template == 'E':
    #     templateE(constraints_lib, 16)

    else:
        print("Sorry, we can not generate contents for this knowledge component, please enter again")


if __name__ == "__main__":
    constraints_lib = xlrd.open_workbook("data\constraints.xlsx")
    kc = [[], [], [], []]
    for i in range(4):
        table = constraints_lib.sheets()[i]
        l = table.col_values(0)
        print(table.col_values(0))
        x = len(l) - 1
        while x >= 0:
            if l[x] == "":
                break
            kc[i].append(int(float(l[x])))
            x -= 1
        kc[i].reverse()

    kc_id = int(input("Please enter Knowledge Component ID: "))
    while kc_id > 0:
        menu(constraints_lib, kc_id)
        kc_id = int(input("Please enter Knowledge Component ID: "))








