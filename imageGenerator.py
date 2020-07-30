from __future__ import print_function
import PIL.Image as img
import os
from textGenerator import database
obj_10_list = database['obj_10']

def image_numobj(img_obj, num, img_dir):
    width, height = img_obj.size
    img_white = img.new('RGB', (width, height), (255, 255, 255))
    scale = int((num+1)/2)
    first_row_num = scale
    hl = 3 / 20
    region = img_obj.resize((int(width/5), int(height/5)), img.ANTIALIAS)
    index = 0
    r = l = 0
    ws = (1-0.2*first_row_num)/(first_row_num+1)
    if num == 1:
        img_white.paste(region, (int(0.4*width), int(0.4*height)), region)
    else:
        for n in range(num):
            if n == first_row_num:
                index = 0
            if n < first_row_num:
                img_white.paste(region, (int(width * (ws + index * (0.2 + ws))), int(height * hl)), region)
                index += 1
            else:
                img_white.paste(region, (int(width * (ws + index * (0.2 + ws))), int(height * (hl + 1 / 2))), region)
                index += 1
    img_white.save(img_dir)

def image_splice(word, num1, num2):
    obj_name = word
    img_dir = "Under10_objimage" + "\\" + obj_name + '_' + str(num1) + '+' + str(num2) + '.png'
    if os.path.isfile(img_dir):
        return img_dir
    IMG = "Under10_objimage" + "\\" + obj_name + ".png"

    im = img.open(IMG)
    im = im.convert('RGBA')
    width, height = im.size
    color_0 = im.getpixel((2, 2))
    print(type(color_0), color_0[0])
    for h in range(height):
        for l in range(width):
            dot = (l, h)
            color_1 = im.getpixel(dot)
            if color_1 == color_0:
                color_1 = color_1[:-1] + (0,)
                im.putpixel(dot, (color_0[0], color_0[1], color_0[2], 0))
    width, height = im.size
    img_white = img.new('RGB', (int(width * 2.2), height), (255, 255, 255))
    img_obj = im.resize((int(width / 5), int(height / 5)), img.ANTIALIAS)
    im_symbol = img.open("Under10_objimage\\symbol_plus.png")
    im_symbol = im_symbol.convert('RGBA')
    img_symbol = im_symbol.resize((int(width / 5), int(height / 5)), img.ANTIALIAS)
    img_white.paste(img_symbol, (width, int(0.4 * height)), img_symbol)
    if num1 <= 5:
        for n in range(num1):
            img_white.paste(img_obj, (int(width - (n+1) * 0.2 * width), int(0.4 * height)), img_obj)

    elif num1 > 5:
        for n in range(int((num1+1)/2)):
            img_white.paste(img_obj, (int((1 - int((num1+1)/2) * 0.2 + n*0.2) * width), int(0.5 * height)), img_obj)
        for n in range(num1 - int((num1+1)/2)):
            img_white.paste(img_obj, (int((1 - int((num1+1)/2) * 0.2 + n*0.2) * width), int(0.3 * height)),
                            img_obj)

    if num2 <= 5:
        for n in range(num2):
            img_white.paste(img_obj, (int(width + (n+1) * 0.2 * width), int(0.4 * height)), img_obj)
    elif num2 > 5:
        for n in range(int((num2+1)/2)):
            img_white.paste(img_obj, (int((1.2 + n*0.2) * width), int(0.5 * height)), img_obj)
        for n in range(num2 - int((num2+1)/2)):
            img_white.paste(img_obj, (int((1.2 + n*0.2) * width), int(0.3 * height)),
                            img_obj)
    if num1 <= 5 and num2 <= 5:
        img_white = img_white.crop((int((1 - num1 * 0.2) * width), 0, int((1.2 + num2 * 0.2) * width), height))
    elif 5 <= num1 <= 10 and num2 <= 5:
        img_white = img_white.crop((int((1 - (num1 - int(num1 / 2)) * 0.2) * width), 0, int((1.2 + num2 * 0.2) * width), height))
    elif num1 <= 5 and 5 <= num2 <= 10:
        img_white = img_white.crop((int((1 - num1 * 0.2) * width), 0,  int((1.2 + (num2 - int(num2 / 2)) * 0.2) * width), height))
    elif 5 <= num1 <= 10 and 5 <= num2 <= 10:
        img_white = img_white.crop((int((1 - (num1 - int(num1 / 2)) * 0.2) * width), 0,  int((1.2 + (num2 - int(num2 / 2)) * 0.2) * width), height))
    img_white.save(img_dir)
    print(img_dir)
    return img_dir

def image_generator(word, num):
    obj_name = word
    if obj_name in obj_10_list:
        img_dir = "Under10_objimage" + "\\" + obj_name + '_' + str(num) + '.png'
        if os.path.isfile(img_dir):
            return img_dir
        IMG = "Under10_objimage" + "\\" + obj_name + ".png"
        im = img.open(IMG)
        im = im.convert('RGBA')
        width, height = im.size
        color_0 = im.getpixel((2, 2))
        print(type(color_0), color_0[0])
        for h in range(height):
            for l in range(width):
                dot = (l, h)
                color_1 = im.getpixel(dot)
                if color_1 == color_0:
                    color_1 = color_1[:-1] + (0,)
                    im.putpixel(dot, (color_0[0], color_0[1], color_0[2], 0))
        image_numobj(im, num,img_dir)
        return img_dir
    else:
        return None

    # IMG = "data\imgapple.png"


if __name__ == "__main__":
    text = 'Tom has 9 banana'
    image_splice('pencil', 9,10)




# if width == height:
#     region = im
# else:
#     if width > height:
#         delta = (width-height)/2
#         box = (delta, 0, delta + height, height)
#     else:
#         delta = (height-width)/2
#         box = (0, delta, width, delta+width)
#     region = im.crop(box)

