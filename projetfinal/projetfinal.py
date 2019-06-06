from tkinter import *
def pointeur(event):
    chaine['text'] = "Clic détecté en X =" + str(event.x) + ", Y =" + str(event.y)
    
fen = Tk()
cadre = Frame(fen, width =1600, height =900, bg="yellow")
cadre.bind("<Button-1>", pointeur)
cadre.pack()
chaine = Label(fen)
chaine.pack()

fen.mainloop()