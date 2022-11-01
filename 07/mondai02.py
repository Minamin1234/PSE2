import tkinter as tk
import tkinter.filedialog as fd
import PIL.Image
import PIL.ImageTk
import sklearn.datasets
import sklearn.svm
import PIL.Image
import numpy

def imageToData(filename):
    grayImage = PIL.Image.open(filename).convert("L")
    grayImage = grayImage.resize((8,8),PIL.Image.ANTIALIAS)

    numImage = numpy.asarray(grayImage, dtype = float)
    numImage = numpy.floor(16 - 16 * (numImage / 256))
    numImage = numImage.flatten()
    return numImage

def predictDigits(data):
    digits = sklearn.datasets.load_digits()
    clf = sklearn.svm.SVC(gamma=0.001)
    clf.fit(digits.data,digits.target)
    n = clf.predict([data])
    print(f"予測 = {n}")
    return n

def on_click():
    fpath = fd.askopenfilename()
    print(fpath)
    data = imageToData(fpath)
    res = predictDigits(data)
    
    img = PIL.Image.open(fpath)
    imgd = PIL.ImageTk.PhotoImage(img)
    IL_image.configure(image = imgd)
    IL_image.image = imgd
    L_label["text"] = f"予測 = {res}"
    

root = tk.Tk()
root.geometry("400x400")
root.title("mondai02")

btn = tk.Button(text="画像を選択",command=on_click)
IL_image = tk.Label()
L_label = tk.Label()

btn.pack()
IL_image.pack()
L_label.pack()

tk.mainloop()