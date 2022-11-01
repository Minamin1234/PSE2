import tkinter as tk
import tkinter.filedialog as fd
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

def on_click():
    fpath = fd.askopenfilename()
    print(fpath)
    data = imageToData(fpath)
    predictDigits(data)
    

root = tk.Tk()
root.geometry("200x200")
root.title("mondai01")

btn = tk.Button(text="画像を選択",command=on_click)

btn.pack()

tk.mainloop()