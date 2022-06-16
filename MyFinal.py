#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, dialog
from PIL import Image, ImageDraw, ImageTk
import threading
import os


# In[2]:


img_size = 300

def thread(f, *args):
    t = threading.Thread(target = f, args = args)
    t.setDaemon(True)
    t.start()
    
def resize_img(img, size):
    """Resize the image to specific size"""
    w = img.width
    h = img.height
    if w > h:
        result = img.resize((size, int(size/w*h)))
    elif h > w:
        result = img.resize((int(size/h*w), size))
    else:
        result = img.resize((size, size))
    return result

def show(value):
    """show value of scale"""
    v = int(float(value))
    lebel_value = tk.Label(win, text = " " + str(v) + "% ", font = ('Arial', 12))
    lebel_value.grid(row = 5, column = 1, columnspan = 2, padx = 20, pady = 20)

def check_bound(ary):
    """check 0 <= RGB <= 255"""
    for i in range(3):
        if ary[i] > 255:
            ary[i] = 255
        if ary[i] < 0:
            ary[i] = 0
    return ary
    
def wait():
    """show text before done"""
    wait = tk.Label(win, text = '請稍候......', font = ('Arial', 12), background = "White")
    wait.grid(row = 1, column = 2, rowspan = 2, columnspan = 2, padx = 20, pady = 20)


# In[3]:


def load():
    """load image and show"""
    global img_tk, path, img, img_new, log
    path = filedialog.askopenfilename(parent = win,
                                      title = "Load Image",
                                      filetypes = (("JPG files", "*.jpg"),\
                                                   ("ALL files", "*.*")))
    img = Image.open(path)
    img_resized = resize_img(img, img_size)
    img_tk = ImageTk.PhotoImage(img_resized)
    
    #show origin image
    img_label = tk.Label(win, width = img_size, height = img_size, image = img_tk)
    img_label.grid(row = 1, rowspan = 2, column = 0, columnspan = 2, padx = 20, pady = 20, sticky = 'nw')
    
    #show preview image
    preview_label = tk.Label(win, width = img_size, height = img_size, image = img_tk)
    preview_label.grid(row = 1, rowspan = 2, column = 2, columnspan = 2, padx = 20, pady = 20,                       sticky = 'nw')
    
def save():
    """save image"""
    global img_new
    path = filedialog.asksaveasfilename(parent = win,
                                      title = "Save Image",
                                      filetypes = (("JPG files", "*.jpg"),))
    img_new.save(str(path) + '.jpg')
    
def reset():
    global log
    log = []
    """reset image to origin image"""
    preview_label = tk.Label(win, width = img_size, height = img_size, image = img_tk)
    preview_label.grid(row = 1, rowspan = 2, column = 2, columnspan = 2, padx = 20, pady = 20,                       sticky = 'nw')


# In[4]:


def button_bd():
    global scale
    
    scale = ttk.Scale(win, length = 300, from_ = -100, to = 100,                      command = show)
    scale.grid(row = 4, column = 1, columnspan = 2, padx = 20, pady = 20)
    
    lebel_value = tk.Label(win, text = " 0% ", font = ('Arial', 12))
    lebel_value.grid(row = 5, column = 1, columnspan = 2, padx = 20, pady = 20)
    
    bt_check = tk.Button(win, text = "套用", font = ('Arial', 12),                    width = 10, height = 2,                    command = lambda : thread(button_brighten_check))
    bt_check.grid(row = 4, column = 3, padx = 20, pady = 20)
    
def button_brighten_check():
    global img_new, img_new_tk
    
    wait()
    
    img_new = Image.fromarray(brighten())
    img_resize = resize_img(img_new, img_size)
    img_new_tk = ImageTk.PhotoImage(img_resize)
    
    preview_label = tk.Label(win, width = img_size, height = img_size,                             image = img_new_tk)
    preview_label.grid(row = 1, rowspan = 2, column = 2, columnspan = 2, padx = 20, pady = 20,                       sticky = 'nw')

def brighten():
    """brighten"""
    global img_new, img_new_tk
    
    img_odd = img
    img_ary = np.array(img_odd)
    temp = np.zeros(img_ary.shape)
    new_ary = np.zeros(img_ary.shape).astype('uint8')
    
    v = float(scale.get())
    v /= 100
    
    
    if v > 0:
        e = 10**(-6)
        for i in range(img_ary.shape[0]):
            for j in range(img_ary.shape[1]):
                temp[i][j][0] = img_ary[i][j][0]*(1/(1+e-v))
                temp[i][j][1] = img_ary[i][j][1]*(1/(1+e-v))
                temp[i][j][2] = img_ary[i][j][2]*(1/(1+e-v))
                new_ary[i][j] = check_bound(temp[i][j])
        
    elif v < 0:
        for i in range(img_ary.shape[0]):
            for j in range(img_ary.shape[1]):
                temp[i][j][0] = img_ary[i][j][0] *(1+v)
                temp[i][j][1] = img_ary[i][j][1] *(1+v)
                temp[i][j][2] = img_ary[i][j][2] *(1+v)
                new_ary[i][j] = check_bound(temp[i][j])
    else:
        new_ary = img_ary            
    return new_ary


# In[5]:


def button_contrast():
    global scale
    
    scale = ttk.Scale(win, length = 300, from_ = -100, to = 100,                      command = show)
    scale.grid(row = 4, column = 1, columnspan = 2, padx = 20, pady = 20)
    
    lebel_value = tk.Label(win, text = " 0% ", font = ('Arial', 12))
    lebel_value.grid(row = 5, column = 1, columnspan = 2, padx = 20, pady = 20)
    
    bt_check = tk.Button(win, text = "套用", font = ('Arial', 12),                    width = 10, height = 2,                    command = lambda : thread(button_contrast_check))
    bt_check.grid(row = 4, column = 3, padx = 20, pady = 20)
    
def button_contrast_check():
    global img_new, img_new_tk
    
    wait()
    
    img_new = Image.fromarray(contrast())
    img_resize = resize_img(img_new, img_size)
    img_new_tk = ImageTk.PhotoImage(img_resize)
    
    preview_label = tk.Label(win, width = img_size, height = img_size,                             image = img_new_tk)
    preview_label.grid(row = 1, rowspan = 2, column = 2, columnspan = 2, padx = 20, pady = 20,                       sticky = 'nw')
    
def contrast():
    """change contrast ratio"""
    global img_new, img_new_tk
    
    img_odd = img
    img_ary = np.array(img_odd)
    temp = np.zeros(img_ary.shape)
    new_ary = np.zeros(img_ary.shape).astype('uint8')
    
    a = float(scale.get())
    c = (259*(a+255)) / (255*(259-a))
    t = 128 #threshold
    
    for i in range(img_ary.shape[0]):
        for j in range(img_ary.shape[1]):
            temp[i][j][0] = t + (img_ary[i][j][0] - t)*c
            temp[i][j][1] = t + (img_ary[i][j][1] - t)*c
            temp[i][j][2] = t + (img_ary[i][j][2] - t)*c
            new_ary[i][j] = check_bound(temp[i][j])         
    return new_ary


# In[6]:


def button_contrast():
    global scale
    
    scale = ttk.Scale(win, length = 300, from_ = -100, to = 100,                      command = show)
    scale.grid(row = 4, column = 1, columnspan = 2, padx = 20, pady = 20)
    
    lebel_value = tk.Label(win, text = " 0% ", font = ('Arial', 12))
    lebel_value.grid(row = 5, column = 1, columnspan = 2, padx = 20, pady = 20)
    
    bt_check = tk.Button(win, text = "套用", font = ('Arial', 12),                    width = 10, height = 2,                    command = lambda : thread(button_contrast_check))
    bt_check.grid(row = 4, column = 3, padx = 20, pady = 20)
    
def button_contrast_check():
    global img_new, img_new_tk
    
    wait()
    
    img_new = Image.fromarray(contrast())
    img_resize = resize_img(img_new, img_size)
    img_new_tk = ImageTk.PhotoImage(img_resize)
    
    preview_label = tk.Label(win, width = img_size, height = img_size,                             image = img_new_tk)
    preview_label.grid(row = 1, rowspan = 2, column = 2, columnspan = 2, padx = 20, pady = 20,                       sticky = 'nw')
    
def contrast():
    """change contrast ratio"""
    global img_new, img_new_tk
    
    img_odd = img
    img_ary = np.array(img_odd)
    temp = np.zeros(img_ary.shape)
    new_ary = np.zeros(img_ary.shape).astype('uint8')
    
    a = float(scale.get())
    c = (259*(a+255)) / (255*(259-a))
    t = 128 #threshold
    
    for i in range(img_ary.shape[0]):
        for j in range(img_ary.shape[1]):
            temp[i][j][0] = t + (img_ary[i][j][0] - t)*c
            temp[i][j][1] = t + (img_ary[i][j][1] - t)*c
            temp[i][j][2] = t + (img_ary[i][j][2] - t)*c
            new_ary[i][j] = check_bound(temp[i][j])         
    return new_ary


# In[7]:


def button_T():
    global scale
    
    scale = ttk.Scale(win, length = 300, from_ = -100, to = 100,                      command = show)
    scale.grid(row = 4, column = 1, columnspan = 2, padx = 20, pady = 20)
    
    lebel_value = tk.Label(win, text = " 0% ", font = ('Arial', 12))
    lebel_value.grid(row = 5, column = 1, columnspan = 2, padx = 20, pady = 20)
    
    bt_check = tk.Button(win, text = "套用", font = ('Arial', 12),                    width = 10, height = 2,                    command = lambda : thread(button_T_check))
    bt_check.grid(row = 4, column = 3, padx = 20, pady = 20)
    
def button_T_check():
    global img_new, img_new_tk
    
    wait()
    
    img_new = Image.fromarray(T())
    img_resize = resize_img(img_new, img_size)
    img_new_tk = ImageTk.PhotoImage(img_resize)
    
    preview_label = tk.Label(win, width = img_size, height = img_size,                             image = img_new_tk)
    preview_label.grid(row = 1, rowspan = 2, column = 2, columnspan = 2, padx = 20, pady = 20,                       sticky = 'nw')
    
def T():
    """change contrast ratio"""
    global img_new, img_new_tk
    
    img_odd = img
    img_ary = np.array(img_odd)
    temp = np.zeros(img_ary.shape)
    new_ary = np.zeros(img_ary.shape).astype('uint8')
    
    a = float(scale.get())
    if a > 0:
        r = a
        g = a/5
        b = -a
    else:
        r = a
        g = -a/2
        b = -a
    
    for i in range(img_ary.shape[0]):
        for j in range(img_ary.shape[1]):
            temp[i][j][0] = img_ary[i][j][0] + r
            temp[i][j][1] = img_ary[i][j][1] + g
            temp[i][j][2] = img_ary[i][j][2] + b
            new_ary[i][j] = check_bound(temp[i][j])
            
    return new_ary


# In[8]:


#Window setting
win = tk.Tk()
win.title("圖片編輯器(⁎˃ᆺ˂)")
win.geometry('900x700')


#Lebel of origin image
ori = tk.Label(win, text = '原圖', font = ('Arial', 12))
ori.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 20)

#Lebel of The start staion
pre = tk.Label(win, text = '預覽', font = ('Arial', 12))
pre.grid(row = 0, column = 2, columnspan = 2, padx = 20, pady = 20)

#Button of load image
bt_load = tk.Button(win, text = "讀取檔案", font = ('Arial', 12),                    width = 15, height = 2, command = load)
bt_load.grid(row = 1, column = 4, padx = 20, pady = 20)

#Button of save image
bt_save = tk.Button(win, text = "儲存檔案", font = ('Arial', 12),                    width = 15, height = 2, command = save)
bt_save.grid(row = 2, column = 4, padx = 20, pady = 20)

#Button of dark or brighten
bt_bd = tk.Button(win, text = "亮度", font = ('Arial', 12),                    width = 10, height = 2,                    command = lambda : thread(button_bd))
bt_bd.grid(row = 3, column = 0, padx = 20, pady = 20)

#Button of contrast
bt_cont = tk.Button(win, text = "對比度", font = ('Arial', 12),                    width = 10, height = 2,                    command = lambda : thread(button_contrast))
bt_cont.grid(row = 3, column = 1, padx = 20, pady = 20)

#Button of sharpness
bt_shar = tk.Button(win, text = "濾鏡", font = ('Arial', 12),                    width = 10, height = 2,                    command = lambda : thread(button_T))
bt_shar.grid(row = 3, column = 2, padx = 20, pady = 20)

#Button of reset
bt_res = tk.Button(win, text = "重設圖片", font = ('Arial', 12),                    width = 10, height = 2,                    command = lambda : thread(reset))
bt_res.grid(row = 3, column = 3, padx = 20, pady = 20)


win.mainloop()


# In[ ]:





# In[ ]:





# In[ ]:




