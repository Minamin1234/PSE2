import tkinter as tk
import tkinter.filedialog as fd
import PIL.Image
import PIL.ImageTk

def dispPhoto(path):
    newImage = PIL.Image.open(path).resize((300,300))
    imageData = PIL.ImageTk.PhotoImage(newImage)
    imageLabel.configure(image = imageData)
    imageLabel.image = imageData

def dispPhoto_gray(path):
    newImage = PIL.Image.open(path).convert("L").resize((300,300))

    imageData = PIL.ImageTk.PhotoImage(newImage)
    imageLabel.configure(image = imageData)
    imageLabel.image = imageData

def dispPhoto_mosaic(path):
    newImage = PIL.Image.open(path).convert("L").resize((32,32)).resize((300,300),resample=0)
    imageData = PIL.ImageTk.PhotoImage(newImage)
    imageLabel.configure(image = imageData)
    imageLabel.image = imageData

def openFile():
    fpath = fd.askopenfilename()

    if fpath:
        dispPhoto_mosaic(fpath)

root = tk.Tk()
root.geometry("400x350")

btn = tk.Button(text="ファイルを開く", command= openFile)
imageLabel = tk.Label()
btn.pack()
imageLabel.pack()
tk.mainloop()