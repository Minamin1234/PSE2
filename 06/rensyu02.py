import tkinter as tk
import tkinter.filedialog as fd
import PIL.Image
import PIL.ImageTk

IMG_SIZE = (200,200)  #画像サイズ
MOSAIC_SIZE = (32,32) #モザイクのドットサイズ

# 写真を表示させます。
def dispPhoto(path,il):
    img = PIL.Image.open(path).resize(IMG_SIZE)
    imgData = PIL.ImageTk.PhotoImage(img)
    il.configure(image = imgData)
    il.image = imgData

# グレースケールに変換された画像を表示させます。
def to_gray(path,il):
    img = PIL.Image.open(path).convert("L").resize(IMG_SIZE)
    imgData = PIL.ImageTk.PhotoImage(img)
    il.configure(image = imgData)
    il.image = imgData

# モザイク処理をした画像を表示させます。
def to_mosaic(path,il):
    img = PIL.Image.open(path).convert("L").resize(MOSAIC_SIZE).resize(IMG_SIZE)
    imgData = PIL.ImageTk.PhotoImage(img)
    il.configure(image = imgData)
    il.image = imgData

# 写真を選択させ、選択した写真のパスを返します。
def selectPhoto():
    fpath = fd.askopenfilename()
    if fpath:
        return fpath

# 写真を選択させ、選択した画像を通常/グレースケール変換/モザイク処理された
# 画像をそれぞれ表示させます。
def showphotos():
    currentPhotoPath = selectPhoto()
    dispPhoto(currentPhotoPath,IL_normal)
    to_gray(currentPhotoPath,IL_gray)
    to_mosaic(currentPhotoPath,IL_mosaic)


currentPhotoPath = ""
root = tk.Tk()
root.geometry("800x700")

btn = tk.Button(text="ファイルを開く", command= showphotos)
IL_normal = tk.Label()
IL_gray = tk.Label()
IL_mosaic = tk.Label()
btn.pack()
IL_normal.pack()
IL_gray.pack()
IL_mosaic.pack()
tk.mainloop()