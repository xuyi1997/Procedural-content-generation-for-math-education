from tkinter import *
import sys
sys.setrecursionlimit(5000)
import hashlib
import time
from KC_set import kc_list,kc_list_equation,kc_list_ns,kc_list_rt,kc_list_perc,kc_list_grid
import tkinter.font as tkFont
from ttkwidgets.autocomplete import AutocompleteCombobox

LOG_LINE_NUM = 0



class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):
        ft1 = tkFont.Font(family='Arial', size=10, weight=tkFont.BOLD)
        ft_text = tkFont.Font(family='Arial', size=15)
        self.init_window_name.title("math quiz generator")
        #self.init_window_name.geometry('320x160+10+10')
        self.init_window_name.geometry('1000x700+10+10')
        # self.init_window_name["bg"] = "pink"
        # self.init_window_name.attributes("-alpha",0.9)

        self.choose_lable = Label(self.init_window_name, text="Please choose a Knowledge Component",font=ft1)
        self.choose_lable.grid(row=0, column=0, columnspan=2)



        # Drop down box
        from tkinter import ttk
        # self.drop_down_box = Combobox_Autocomplete(self.init_window_name, kc_list, listbox_width=150, highlightthickness=1)
        # self.drop_down_box.focus()
        self.drop_down_box = AutocompleteCombobox(self.init_window_name, completevalues=kc_list, width=150)
        self.drop_down_box.grid(row=1, column=0,columnspan=2)




        self.choose_language_label = Label(self.init_window_name, text="Please choose language",font=ft1)
        self.choose_language_label.grid(row=2, column=0)
        self.choose_language_box = ttk.Combobox(self.init_window_name, values=['English', 'Dutch'], width=50)
        self.choose_language_box.grid(row=3, column=0)
        self.is_retrieve = BooleanVar()
        self.choose_retrieve_button = ttk.Checkbutton(self.init_window_name, text='Retrieve Image or Not',
                                                      variable=self.is_retrieve)
        self.choose_retrieve_button.grid(row=3, column=1)

        # Button
        self.str_generate_button = Button(self.init_window_name, text="Generate", bg="lightblue", width=10,
                                          command=self.generator)
        self.str_generate_button.grid(row=4, column=0, columnspan=2)
        self.result_data_label = Label(self.init_window_name, text="Generated question",font=ft1)
        self.result_data_label.grid(row=9, column=0)

        self.result_data_Text = Text(self.init_window_name,width=50)
        self.result_data_Text.grid(row=10, column=0)
        self.answer_label = Label(self.init_window_name, text="Answer",font=ft1)
        self.answer_label.grid(row=9, column=1)
        self.answer_data_Text = Text(self.init_window_name,width=50)
        self.answer_data_Text.grid(row=10, column=1)
        self.image_label = Label(self.init_window_name, text="Image",font=ft1)
        self.image_label.grid(row=11, column=0,columnspan=2)
        self.image_data_Text = Text(self.init_window_name,width=100)
        self.image_data_Text.grid(row=12, column=0,columnspan=2)
        self.img_label = Label(self.init_window_name, image=None)




    def generator(self):
        self.img_label.grid_forget()
        kc = self.drop_down_box.get()
        language = self.choose_language_box.get()
        kc_no = kc[0:kc.index('-') - 1]
        from overall_menu import Menu
        if language == 'Dutch':
            m = Menu(int(kc_no), 'nl', self.is_retrieve.get())
        else:
            m = Menu(int(kc_no), 'en', self.is_retrieve.get())
        question, answer, img_dir_list = m.menu()
        if len(question) == 0:
            question = "Sorry we can not generate text question for this KC"
        self.result_data_Text.delete(1.0,'end')
        self.result_data_Text.insert(END,question)
        self.answer_data_Text.delete(1.0,'end')
        self.answer_data_Text.insert(END,answer)
        from PIL import Image, ImageTk
        self.image_data_Text.delete(1.0, 'end')
        for img_dir in img_dir_list:
            self.image_data_Text.insert(END, str(img_dir))
            self.image_data_Text.insert(END, '\n')
            # img = Image.open(img_dir)
            # w, h = img.size
            # ws = 500
            # hs = h * ws / w
            # img = img.resize((ws,int(hs)), Image.ANTIALIAS)
            # photo = ImageTk.PhotoImage(img)
            # self.img_label.config(image=photo)
            # self.img_label.grid(row=12, column=0, columnspan=2)

        self.init_window_name.mainloop()



def gui_start():
    init_window = Tk()
    ZMJ_PORTAL = MY_GUI(init_window)

    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()


gui_start()
