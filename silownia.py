import json
import tkinter
from tkinter import ttk
import threading
import time
window=tkinter.Tk("silownia")
odliczanie=0
licznik=None
karnety=[]
with open("karnety.json") as file:
    karnety=json.loads(file.read())
    file.close()
tabs=tkinter.ttk.Notebook(window)
tab1=tkinter.Frame(tabs)

tab2=tkinter.Frame(tabs)
tabs.add(tab1,text="karnety")
tabs.add(tab2,text="dodaj")
k= tkinter.StringVar(tab1)
k.set(karnety[0]["name"])

dropdown=tkinter.OptionMenu(tab1,k,*[item["name"] for item in karnety])
dropdown.pack()

label=tkinter.Label(tab1,text="pozostało "+str(karnety[0]["seconds"]))
label.pack()
def textchanged(*args):
    global karnety
    karnet=next(item for item in karnety if item["name"]==k.get())  
    label.config(text="pozostało"+str(karnet["seconds"]))

def safechanges():
    global karnety
    with open("karnety.json","w") as file:
        file.write(json.dumps(karnety))

def timer(*args):
    global odliczanie,licznik
    if licznik != None:
        licznik=None
        ind=[i for i,d in enumerate(karnety) if k.get() in d.values()][0]
        karnety[ind]["seconds"]=karnety[ind]["seconds"]-odliczanie
        safechanges()
        return
    odliczanie=0
    def addtime():
        global odliczanie,label,karnety,licznik
        karnet=next(item for item in karnety if item["name"]==k.get())
        while licznik !=None:
            time.sleep(1)
            odliczanie=odliczanie+1
            label.config(text=f"pozostało {karnet['seconds']-odliczanie}")
    licznik=threading.Thread(target=addtime)
    licznik.start()

k.trace("w",textchanged)
button=tkinter.Button(tab1,text="odliczaj",command=timer)
button.pack()
n=tkinter.StringVar(tab2)
n.set("")
textbox=ttk.Entry(tab2,textvariable=n)
textbox.pack()
def addkarnet(*args):
    global n, karnety
    karnety.append({
        "name":n.get(),
        "seconds":0
    })
    safechanges()
button2=tkinter.Button(tab2,text="dodaj",command=addkarnet)
button2.pack()
h= tkinter.StringVar(tab2)
h.set(karnety[0]["name"])

dropdown2=tkinter.OptionMenu(tab2,h,*[item["name"] for item in karnety])
dropdown2.pack()
p=tkinter.StringVar(tab2)
p.set("1")
label2=ttk.Label(tab2,textvariable=p)

slider=ttk.Scale(tab2,orient="horizontal",length=100,from_=1,to=10,variable=p)
slider.pack()
label2.pack()
def addgodziny():
    global p,karnety, h
    ind=[i for i,d in enumerate(karnety) if h.get() in d.values()][0]
    karnety[ind]["seconds"]=karnety[ind]["seconds"]+float(p.get())*3600
    safechanges()
button3=tkinter.Button(tab2,text="dodaj godziny",command=addgodziny)
button3.pack()
tabs.pack(expand=1,fill="both")
window.mainloop()
