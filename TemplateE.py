import matplotlib.pyplot as plt
import random
import matplotlib.patches as patches
<<<<<<< HEAD
from PIL import Image
from PIL import ImageDraw
import math
WIDTH = 600
HEIGHT = 600
CYAN = (0, 255, 255)
PURPLE = (147, 112, 219)
WHITE = (255,255,255)
DIR = "grid_paper.png"
LINE_NUM_X = 20
LINE_NUM_Y = 15
stack = []
=======

def kc_354():
    # calculate the perimeter of a rectangle with the aid of the formula 2 x (l + b) or 2 x l + 2 x b
    N = random.choice([10, 20])
    #width = random.randint(1, N-2)
    #height = random.randint(1, N-2)
    width = 4
    height = 2
    return N, width, height
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5


def show_grid(fig, N, width, height):
    ax = fig.add_subplot(111)
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1.0))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1.0))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1.0))  
    ax.yaxis.set_minor_locator(plt.MultipleLocator(1.0))
    ax.grid(which='major', axis='x', linewidth=0.5, linestyle='-', color='0.25')
    ax.grid(which='minor', axis='x', linewidth=0.5, linestyle='-', color='0.25')
    ax.grid(which='major', axis='y', linewidth=0.5, linestyle='-', color='0.25')
    ax.grid(which='minor', axis='y', linewidth=0.5, linestyle='-', color='0.25')
    ax.set_xticklabels([i for i in range(N+2)])
    ax.set_yticklabels([i for i in range(N+2)])

    x1 = int((N - width) / 2)
    y1 = int((N - height) / 2)
    rec = patches.Rectangle((float(x1), float(y1)), width, height, linewidth=1, color='r')
    ax.add_patch(rec)
    ax.set_aspect(1. / ax.get_data_ratio())
    plt.show()


<<<<<<< HEAD
def grid_paper(img_polygon, line_num):
    line_num_x, line_num_y = line_num[0], line_num[1]
    img_d = ImageDraw.Draw(img_polygon)
    x_len, y_len = img_polygon.size
    x_step = int(x_len / line_num_x)
    y_step = int(y_len / line_num_y)
    for x in range(0, x_len, x_step):
        img_d.line(((x, 0), (x, y_len)), WHITE, width=2)
        # print((x, 0), (x, y_len))
    for y in range(0, y_len, y_step):
        j = y_len - y - 1
        img_d.line(((0, j), (x_len, j)), WHITE, width=2)
        # print((0, j), (x_len, j))
    return img_polygon

def draw_polygon(img_back, line_num, n):
    img_length, img_width = img_back.size
    line_num_x, line_num_y = line_num[0], line_num[1]
    img_polygon = ImageDraw.Draw(img_back)
    dx = (img_length / line_num_x)
    dy = (img_width / line_num_y)
    middle_x = dx * int(line_num_x / 2)
    middle_y = dy * int(line_num_y / 2)
    # draw triangle:
    if n == 3:
        i = random.choice([0, 1])
        if i == 0:
            if stack:
                nd = int(math.sqrt(2 * stack.pop())) + random.choice([1, -1])
            else:
                nd = random.randint(int(line_num_y / 2), line_num_y - 2)  # length of the triangle
                stack.append(nd * nd / 2)
            v1 = (middle_x - int(nd / 2) * dx, middle_y - int(nd / 2) * dy)
            v2 = (v1[0], v1[1] + nd * dy)
            v3 = (v1[0] + nd * dx, v1[1] + nd * dy)
            vertex_list = [v1, v2, v3]
        else:
            if stack:
                nh = int(math.sqrt(stack.pop())) + random.choice([1, -1])
            else:
                nd = random.randint(int(line_num_y / 2), line_num_y - 2)  # length of the triangle
                nh = int(nd / 2)
                stack.append(nh * nh)
            v1 = (middle_x - nh * dx, middle_y + int(nh / 2) * dy)
            v2 = (v1[0] + 2 * nh * dx, v1[1])
            v3 = (v1[0] + nh * dx, v1[1] - nh * dy)
            vertex_list = [v1, v2, v3]

        img_polygon.polygon(vertex_list, fill=PURPLE)
    elif n == 4 or n == 5 or n == 6:
        if stack:
            nx = ny = 0
            while nx * ny == stack[0] or abs(nx * ny - stack[0]) >= 6:
                nx = random.randint(int(line_num_x / 2), line_num_x - 2)  # length of rectangle
                ny = random.randint(int(line_num_y / 2), line_num_y - 2)  # width of rectangle
            stack.pop()
        else:
            nx = random.randint(int(line_num_x / 2), line_num_x - 2)  # length of rectangle
            ny = random.randint(int(line_num_y / 2), line_num_y - 2)  # width of rectangle
            stack.append(nx * ny)
        v1 = (middle_x - int(nx / 2) * dx, middle_y - int(ny / 2) * dy)
        v2 = (v1[0] + nx * dx, v1[1])
        v3 = (v1[0] + nx * dx, v1[1] + ny * dy)
        v4 = (v1[0], v1[1] + ny * dy)
        print(v1, v2, v3, v4)
        if n == 4:
            img_polygon.polygon([v1, v2, v3, v4], fill=PURPLE)
        elif n == 5:
            nt = random.randint(2, int(nx / 2))
            v21 = (v2[0] - nt * dx, v2[1])
            v22 = (v2[0], v2[1] + nt * dy)
            img_polygon.polygon([v1, v21, v22, v3, v4], fill=PURPLE)
        elif n == 6:
            nxs = random.randint(2, int(nx / 2))
            nxy = random.randint(2, int(ny / 2))
            v21 = (v2[0] - nxs * dx, v2[1])
            v22 = (v2[0] - nxs * dx, v2[1] + nxy * dy)
            v23 = (v2[0], v2[1] + nxy * dy)
            img_polygon.polygon([v1, v21, v22, v23, v3, v4], fill=PURPLE)

    return img_back


def template_grid_paper(data, index):
    stack.clear()
    table = data.sheets()[4]
    row_no = int(index)
    kc_id = str(table.cell_value(row_no, table.row_values(0).index("Knowledge Component")))
    kc_des = str(table.cell_value(row_no, table.row_values(0).index("Description")))
    vnum = float(random.choice(eval(table.cell_value(row_no, table.row_values(0).index("number of vertex")))))
    is_show_grid = False
    is_add_label = True
    if 'Y' in table.cell_value(row_no, table.row_values(0).index("show grid")):
        is_show_grid = True
        is_add_label = False
    fnum = int(float(table.cell_value(row_no, table.row_values(0).index("number of figures"))))
    is_fixed_area = False
    if len(str(table.cell_value(row_no, table.row_values(0).index("area constraints")))) > 0:
        is_fixed_area = True
        fixed_area = float(table.cell_value(row_no, table.row_values(0).index("area constraints")))
    task = str(table.cell_value(row_no, table.row_values(0).index("task")))
    text = ""
    is_compare = False
    img_dir = "grid_paper" + "\\" + "grid_paper_" + kc_id + ".png"
    if fnum > 1:
        is_compare = True
    if is_compare:
        img_polygon = Image.new('RGB', (960, 600), WHITE)
        img_length, img_width = 480, 600
        line_num_x, line_num_y = 8, 10
        img_back_1 = Image.new('RGB', (img_length, img_width), CYAN)
        img_back_2 = Image.new('RGB', (img_length, img_width), CYAN)
        line_num = [line_num_x, line_num_y]
        img_polygon_1 = draw_polygon(img_back_1, line_num, vnum)
        vnum = float(random.choice(eval(table.cell_value(row_no, table.row_values(0).index("number of vertex")))))
        img_polygon_2 = draw_polygon(img_back_2, line_num, vnum)
        img_polygon.paste(img_polygon_1, (0, 0))
        img_polygon.paste(img_polygon_2, (480, 0))
        img_polygon = grid_paper(img_polygon, [2 * line_num_x, line_num_y])
        text = "Which one is larger?"
    else:
        img_length = img_width = 600
        line_num_x = line_num_y = 10
        img_back = Image.new('RGB', (img_length, img_width), CYAN)
        line_num = [line_num_x, line_num_y]
        img_polygon = draw_polygon(img_back, line_num, vnum)
        img_polygon = grid_paper(img_polygon, [line_num_x, line_num_y])
        if task == 'area':
            text = "Look at the picture. 1 box is 1 meter long and 1 meter wide. What is the area of the figure?"
        elif task == 'perimeter':
            text = "Look at the picture. 1 box is 1 meter long and 1 meter wide. What is the perimeter of the figure?"

    img_polygon.save(img_dir)
    return text, img_dir


if __name__ == "__main__":
    img_polygon = Image.new('RGB', (600, 600), color='#BEBEBE')
    img_polygon = grid_paper(img_polygon, [10, 10])
    img_polygon.save('grid_paper.png')
    # import xlrd
    # data = xlrd.open_workbook("data\constraints.xlsx")
    # for index in range(1, 12):
    #     text, img_dir = template_grid_paper(data, index)
    #     print(text, img_dir)

=======
if __name__ == "__main__":
    N, width, height = kc_354()
    fig = plt.figure()
    show_grid(fig, N,  width, height)
    print("width: ", width, "height: ", height, "perimeter: ", 2 * (width + height), "area: ", width * height)
>>>>>>> f5a48e54c6e4271f701e4908fefddc0d7a491ca5
