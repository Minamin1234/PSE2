# HT21A099 南 李玖
import os
import tkinter as tk
import tkinter.filedialog as fd

resultfile = "result.txt"  # 出力結果テキストファイル名
initdir = os.path.dirname(__file__)  # ファイルダイアログの初期ディレクトリ
resultfilepath = os.path.join(os.path.dirname(__file__), resultfile)


# 指定したテキストファイルから単語の出現数を求め、結果を指定したテキストファイルに保存する。
def counts(file: str, resultfile: str):
    resultfilepath_ = os.path.join(os.path.dirname(__file__), resultfile)
    data_ = ""
    with open(file, "r") as f:
        data_ = f.read()
    words_ = data_.split()
    notwords_ = []
    for w in words_:
        for s in w:
            if not str.isalnum(s):
                notwords_.append(s)
    for i in range(len(words_)):
        for nw in notwords_:
            words_[i] = words_[i].replace(nw, "")

    wordcnts_ = {}
    maxchar_ = 0
    for w in words_:
        maxchar_ = max(maxchar_, len(w))
        lw = str.lower(w)
        if w in wordcnts_:
            wordcnts_[lw] += 1
        else:
            wordcnts_[lw] = 1
    with open(resultfilepath_, "w") as f:
        for tp in sorted(wordcnts_.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{tp[0]:{maxchar_}}\t{tp[1]:3}\n")
    print("--Done--")
    return wordcnts_


# ボタンがクリックされた際の処理
def on_clicked():
    text.configure(text="")
    file = fd.askopenfilename(initialdir=initdir)
    cnts = counts(file, resultfile)
    text.configure(text=f"完了\n単語数: {len(cnts):3}種類")
    pass


root = tk.Tk()
root.geometry("300x150")

btn = tk.Button(text="ファイルを選択", command=on_clicked)
btn.pack()

text = tk.Label()
text.pack()

tk.mainloop()
