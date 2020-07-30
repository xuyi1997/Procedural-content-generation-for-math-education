
import xlrd
language = 'nl'

from numpy import *
constraints_lib = xlrd.open_workbook("data\constraints.xlsx")
facts_lib = xlrd.open_workbook("data\Facts_library_en.xlsx")
kc = [[], [], [], [], []]
for i in range(5):
    table = constraints_lib.sheets()[i]
    l = table.col_values(0)
    x = len(l) - 1
    while x >= 0:
        if l[x] == "" or x < 1:
            break
        kc[i].append(int(float(l[x])))
        x -= 1
    kc[i].reverse()

class Menu(object):

    def __init__(self, kc_id, language, is_retrieve):
        self.kc_id = kc_id
        self.language = language
        self.is_retrieve = is_retrieve
    def menu(self):
        import shutil, os
        from TemplateA import template_equation
        from TemplateB import template_number_sequence
        from TemplateC import template_ratio_table
        from TemplateD import template_perc_chart
        from TemplateE import template_grid_paper
        shutil.rmtree('grid_paper'), shutil.rmtree('retrieved_image'), shutil.rmtree('percentage_chart'), shutil.rmtree(
            'ratio_table')
        os.mkdir('grid_paper'), os.mkdir('retrieved_image'), os.mkdir('percentage_chart'), os.mkdir('ratio_table')
        generated_question = ""
        generated_answer = ""
        img_dir_list = []
        if self.kc_id in kc[0]:
            index = kc[0].index(self.kc_id) + 3
            generated_expression, RA, WA, text, img_dir_list = template_equation(constraints_lib, index, self.language, self.is_retrieve)
            equation = str(generated_expression + ' = ' + '?')
            generated_question = text
            generated_answer = equation + "\n" + "correct answer: " + RA + "\n" + "wrong answer" + str(WA)

        elif self.kc_id in kc[1]:
            index = kc[1].index(self.kc_id) + 2
            kc_des, question, answer = template_number_sequence(constraints_lib, index, self.language)
            generated_question = question
            generated_answer = answer

        elif self.kc_id in kc[2]:
            index = kc[2].index(self.kc_id) + 3
            question, answer, img_dir = template_ratio_table(constraints_lib, index)
            generated_question = question
            generated_answer = answer
            img_dir_list.append(img_dir)


        elif self.kc_id in kc[3]:
            index = kc[3].index(self.kc_id) + 2
            text, img_dir = template_perc_chart(constraints_lib, index)
            generated_question = text
            generated_answer = ""
            img_dir_list.append(img_dir)

        elif self.kc_id in kc[4]:
            index = kc[4].index(self.kc_id) + 1
            text, img_dir = template_grid_paper(constraints_lib, index)
            generated_question = text
            generated_answer = ""
            img_dir_list.append(img_dir)


        else:
            generated_question = "Sorry, we can not generate contents for this knowledge component, please enter again"
            generated_answer = "Sorry, we can not generate contents for this knowledge component, please enter again"

        return generated_question, generated_answer, img_dir_list



if __name__ == "__main__":

    kc_id = int(input("Please enter Knowledge Component ID: "))
    while kc_id > 0:
        m = Menu(kc_id, 'nl', False)
        generated_question, generated_answer, img_dir_list = m.menu()
        print(generated_question, generated_answer, img_dir_list)
        kc_id = int(input("Please enter Knowledge Component ID: "))








