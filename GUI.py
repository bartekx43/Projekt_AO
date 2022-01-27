from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import filedialog
from PIL import Image, ImageTk
import zad


def resizeForBlackBg(imageName):
    global pathV
    pathV = imageName
    resizedImage = Image.open(imageName)
    resizedImage = resizedImage.resize((450, 350))
    new_image= ImageTk.PhotoImage(resizedImage)
    return new_image 


#tutaj wstawimy elegancko jakies funkcje co sie dzieja po kliknieciu
def clickedImageChoosing():
    global fileName
    global czarnyImage
    czarnyImage = "bgimages/czarne.png"
    fileName = filedialog.askopenfilename(filetypes = (("jpg","*.jpg"),("png","*.png"),("all files","*.*")))
    print(bool(fileName))
    if not fileName:
        fileName = czarnyImage
    fileName = resizeForBlackBg(fileName)
    wybraneZdjLabel.configure(image = fileName)
    wybraneZdjLabel.place(relx = 0.5, rely =0.3, anchor = CENTER) 


def clickedSend():
    global inputPictureDefinition
    print(pathV)
    inputPictureDefinition = combo.get()
    resultString = zad.evaluate(pathV, inputPictureDefinition)
    textResultLabel.configure(text = "You specified selected image as: " + inputPictureDefinition + ". Our program calculated that it is: " + resultString ,styl = "TButton",  font=('Helvetica 13 bold'))


window = Tk()
window.attributes("-zoomed", True)
bgImage = PhotoImage(file = "bgimages/tlo2.png")
labelBg = Label(window, image=bgImage)
labelBg.place(x=0, y=0, relwidth = 1, relheight =1)
window.title("Analiza obrazow - projekt JS && BB")


#styling
style = Style()
style.configure("TButton", foreground="#FFFFFF", background="#0c2a56")
style.configure("TCombobox", fieldbackground= "#0c2a56", background= "white", foreground="#FFFFFF")


combo = Combobox(window)
combo['values']= ('sea', 'forest', 'glacier', 'street', '--choose category--')
combo.current(4) #set the selected item
combo.place(relx = 0.45, rely = 0.5, anchor = CENTER) 


btnChooseImage = Button(window, text="Choose file", command=clickedImageChoosing, style="TButton")
btnChooseImage.place(relx = 0.55, rely = 0.5, anchor = CENTER)


czarneImage = "bgimages/czarne.png"
czarneImage = resizeForBlackBg(czarneImage)
wybraneZdjLabel = Label(window, image=czarneImage)
wybraneZdjLabel.place(relx = 0.5, rely = 0.3, anchor = CENTER) 


btnCount = Button(window, text="Send to detect", command=clickedSend, style="TButton")
btnCount.place(relx = 0.5, rely = 0.6, anchor = CENTER)


textResultLabel = Label(window, text="")
textResultLabel.place(relx = 0.5, rely = 0.7, anchor = CENTER) 


window.mainloop()