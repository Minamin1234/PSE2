import tkinter as tk
import tkinter.filedialog as fd
import PIL.Image
import PIL.ImageTk
import sklearn.datasets
import sklearn.svm
import PIL.Image
import numpy

def s(n):
    sum = 0
    for i in range(1,n+1):
        sum += i
    return sum


def on_click_10():
    L_label["text"] = f"= {s(10)}"
    
def on_click_20():
    L_label["text"] = f"= {s(20)}"

def on_click_30():
    L_label["text"] = f"= {s(30)}"

root = tk.Tk()
root.geometry("400x400")
root.title("mondai02")

btn_10 = tk.Button(text="10",command=on_click_10)
btn_20 = tk.Button(text="20",command=on_click_20)
btn_30 = tk.Button(text="30",command=on_click_30)

L_label = tk.Label()

btn_10.pack()
btn_20.pack()
btn_30.pack()
L_label.pack()

tk.mainloop()