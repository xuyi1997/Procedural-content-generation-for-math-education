
import matplotlib.pyplot as plt
data = [0, 10, 15, 45, 15]
labels = ['Very Poor', 'Poor', 'Fair', 'Good', 'Excellent']
plt.bar(range(5), data, width=0.5, tick_label = labels, color = ['b', 'r', '#FFFF00', 'g', '#9400D3'])
plt.ylabel('Participants')
plt.show()
# import xlrd
# constraints_lib = xlrd.open_workbook("data\constraints.xlsx")
# kc = [[],[],[],[],[]]
# for i in range(5):
#     table = constraints_lib.sheets()[i]
#     l = table.col_values(0)
#     x = len(l) - 1
#     while x >= 0:
#         if l[x] == "" or x < 1:
#             break
#         kc[i].append(int(float(l[x])))
#         x -= 1
#     kc[i].sort()
#
# print(kc)
# kc_list_equation = [27, 39, 51, 77, 83, 106, 108, 111, 113, 115, 117, 118, 119, 120, 121, 122, 123, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 141, 142, 143, 144, 145, 146, 148, 149, 150, 151, 152, 153, 155, 156, 157, 159, 160, 161, 161, 162, 163, 164, 165, 166, 168, 169, 170, 171, 173, 174, 175, 176, 177, 178, 179, 180, 181, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 195, 197, 198, 199, 201, 201, 201, 202, 204, 206, 207, 207, 209, 210, 212, 214, 215, 217, 218, 219, 221, 222, 223, 225, 227, 227, 229, 230, 232, 234, 235, 237, 238, 239, 240, 243, 244, 245, 245, 248, 251, 253, 254, 255, 270, 273, 282, 287, 290, 291, 293, 318, 319, 321, 322, 322, 416, 507, 516, 528, 530, 531, 650, 652, 653, 655, 656, 657, 661, 662, 663, 664, 666, 667, 668, 670, 671, 674, 676, 680, 681]
# # kc_list_ns = [1, 2, 6, 12, 13, 15, 16, 19, 20, 23, 24, 25, 28, 29, 30, 32, 33, 34, 36, 37, 38, 40, 41, 42, 43, 45, 46, 47, 49, 52, 53, 54, 55, 57, 58, 59, 60, 61, 62, 64, 65, 66, 69, 72, 73, 74, 75, 76, 78, 78, 80, 87, 88, 90, 91, 92, 94, 97, 98, 99, 101, 102, 103, 107, 112, 236, 246, 265, 325, 327, 330, 364, 365, 366, 367, 395, 400, 408, 415, 428, 432, 439, 440, 446, 448, 459, 460, 461, 470, 471, 474, 475, 477, 480, 481, 483, 484, 487, 492, 493, 494, 495, 504, 506, 511, 512, 515, 518, 519, 605]
# # kc_list_rt = [109, 271, 275, 276, 278, 281, 282, 284, 285, 286, 289, 293, 293, 295, 296, 297, 298, 301, 314, 317, 334, 341, 344, 349, 353, 353, 357, 359, 361, 377, 379, 383, 384, 391, 392, 393, 406, 411, 413, 419, 422, 425, 444, 449, 452, 453, 454, 458, 482, 486, 489, 500, 524, 526, 527, 533, 534]
# # kc_list_perc = [274, 277, 280, 283, 304, 305, 307, 308, 309, 310, 311, 593, 597, 598, 600, 601, 602, 607, 617, 620, 621, 623]
# # kc_list_grid = [327, 346, 354, 368, 371, 372, 374, 380, 381, 387, 390]
# # #
# # kc = kc_list_grid
# # kc_list = []
# # f = open('KC.txt',encoding='utf8')
# # l = f.readlines()
# # while '\n' in l:
# #     l.remove('\n')
# #
# # for kc_no in kc:
# #     flag = False
# #     des = ""
# #     for item in l:
# #         if str(kc_no) == item[0:item.index('-')-1]:
# #             des = item
# #             flag = True
# #             break
# #     if flag:
# #         kc_list.append(des)
# #     else:
# #         print(kc_no, ' no')
# # for i in range(len(kc_list)):
# #     if '\n' in kc_list[i]:
# #         kc_list[i] = kc_list[i].replace('\n',"")
# #
# # print(kc_list)
#
# import spacy
# import nl_core_news_md
# from pattern.nl import pluralize,conjugate,PRESENT,SG
# pluralize_nl, conjugate_nl, PRESENT_NL, SG_NL = pluralize, conjugate, PRESENT, SG
# nlp_dutch = nl_core_news_md.load()
# doc = nlp_dutch('Hoeveel besteden Tom')
# pos_set = []
# for token in doc:
#     pos_set.append((str(token), str(token.pos_)))
# print(pos_set)
# f_text = str(pos_set[0][0]) + ' '
# index = 1
# while index < len(pos_set):
#         pos = pos_set[index]
#         pre_pos = pos_set[index - 1]
#         pre_pre_pos = pos_set[max(0, index - 2)]
#         post_pos = pos_set[min(len(pos_set) - 1, index + 1)]
#         index += 1
#         # 3-rd single present
#         if pos[1] in ['VERB','AUX'] and pre_pos[1] in ['NOUN','PROPN']:
#             f_text += conjugate_nl(verb=pos[0], tense=PRESENT_NL, number=SG_NL)
#             f_text += ' '
#             continue
#         elif pos[1] in ['VERB','AUX'] and post_pos[1] in ['NOUN','PROPN']:
#             f_text += conjugate_nl(verb=pos[0], tense=PRESENT_NL, number=SG_NL)
#             f_text += ' '
#             continue
#         # pluralize
#         elif pos[1] == 'NOUN' and (
#                 (pre_pos[1] == 'NUM' and pre_pos[0] not in ['een', '1'] and index == len(pos_set))
#                 or (pre_pos[1] == 'NUM' and pre_pos[0] not in ['een', '1'] and post_pos[1] not in ['NOUN'])
#                 or (pre_pre_pos[1] == 'NUM' and pre_pre_pos[0] not in ['een', '1'] and pre_pos[0] not in ['ml','l'])
#                 or (pre_pos[1] in ['NOUN', 'ADJ'] and pre_pre_pos[0] in ['many', 'some', 'several', 'more'])
#                 or (pre_pos[0] in ['many', 'some', 'several', 'more'] and post_pos[1] not in ['NOUN'])
#         ):
#             f_text += pluralize_nl(pos[0]).replace('\'','')
#             f_text += ' '
#             continue
#         # hebben....done
#         elif pos[1] == 'AUX' and post_pos[1] == 'ADJ':
#             pos_set.remove(post_pos)
#             pos_set.append(post_pos)
#             post_pos = pos_set[min(len(pos_set) - 1, index)]
#             print(post_pos)
#             if post_pos[1] == 'PROPN':
#                 print(conjugate_nl(verb=pos[0], tense=PRESENT_NL, number=SG_NL))
#                 f_text += conjugate_nl(verb=pos[0], tense=PRESENT_NL, number=SG_NL)
#                 f_text += ' '
#                 continue
#         f_text += pos[0]
#         f_text += ' '
#
# print(f_text)