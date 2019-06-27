from tkinter import *
from random import randrange
from math import cos,pi,sin


class Principale(Tk):
    def __init__(self,parent,life=10):
        
        Tk.__init__(self,parent)
        
        self.parent = parent    
        self.flag = 0 
        self.life = [] 
        self.score = 0

        
        for i in range(0,life):
            self.life.append('')
        #permet de créer une fenêtre (canevas)
        can = self.can = Canvas(width=1900, height = 1000,bg='black')
        can.focus()
        
        #attribution touches
        can.bind_all('<space>',self.start)
        can.bind('<Motion>',self.movemouse)
        can.bind('<Button-1>', self.start)

        #menu du bas
        can.create_rectangle(0,880,1900,1000,fill='light grey') 
        can.create_text(800,890,text='Score: ')
        self.tscore =  can.create_text(900,890,text='0')
        #points de vie
        for i in range(0,life):
            self.life[i] = can.create_oval((25*life)-(25*i),893,(25*life)-10-(25*i),883,fill='crimson')

        #mouvements de la balle
        self.pose = 0 
        self.angle = pi/3 
        self.sens = -1
        self.horizon = 1 
        
        a = self.lbrique=[] 
        self.l = [] 

        bcolor=['deepskyblue','royalblue','light blue','blue','mediumpurple']
        i = 1 
        x = 12
        y = 40
        
        #créations des briques
        while x<1900:
            a.append([can.create_rectangle(x,y,x+40,y+10,fill=bcolor[i]),(i%4)+1])
            self.l.append((x,y))
            y+=12
            i+=1
            i = i%5

            if y==160:
                x+=43
                y = 40
                
        #création de la balle
        self.boule = self.can.create_oval(950,850,960,860,fill='crimson')                            
        self.coord = [950,850]

        #création de la barre
        self.barre = can.create_rectangle(935,860,975,865,fill='white')
        self.bar = 935

        can.pack()

    #lancement de la balle
    def start(self,event):
        if self.flag == 0 and len(self.life)!=0: 
            self.go()
            self.flag = 1

    #faire bouger la barre
    def movemouse(self,event): 
        self.bar = a = event.x
        if 5 < a < 1850 and self.pose==0:
            self.can.coords(self.barre,a,860,a+40,865)
    
    #gestion des rebons de balles + destruction des briques avec augmentation du score
    def go(self):

        stop = 0
        x = self.coord[0]
        y = self.coord[1]
        y += sin(self.angle)*self.sens*1.5
        x += (cos(self.angle))*self.horizon*0.3
        self.coord[1]=y
        self.coord[0]=x
        self.can.coords(self.boule,x,y,x+10,y+10)
        
        i = 0
        while i<len(self.l): 
            if self.l[i][1]-2 <= y <= self.l[i][1]+12 and self.l[i][0]-2 <= x <= self.l[i][0]+42:

                self.sens = (-1)*self.sens
                self.lbrique[i][1] += -1
                if self.lbrique[i][1] == 0: 

                    self.can.delete(self.lbrique[i][0])
                    self.score+= 20*(len(self.life))
                    
                    texte = str(self.score)
                    self.can.delete(self.tscore)
                    self.tscore = self.can.create_text(900,890,text=texte)
                    
                    del self.lbrique[i]
                    del self.l[i]
                    if len(self.l)==0:
                        stop = 1
                break
            i+=1

        #collision de la balle avec la barre
        if 860 <= y <= 865 and self.bar-10 < x < self.bar+47:
            if self.bar-10 <= x <= self.bar+5:
                self.angle = 2*pi/3
                self.horizon = 5

            if self.bar+37 <= x <= self.bar+47:
                self.angle = pi/5
                self.horizon = 5

            if self.bar+5 < x < self.bar+40:
                self.angle = pi/3

            self.sens = (-1)*self.sens

        #collision avec les murs  
        if x<10 or x>1850:  
            self.horizon = (-1)*self.horizon
        #collision avec le plafond
        if y<10:
            self.sens = (-1)*self.sens
        #chute + perte de vie
        if y>866 and x>self.bar+47 or y>866 and x<self.bar-10:
            self.can.delete(self.life[0])
            del self.life[0]
            stop = 1
        #repositionnement de départ si on perd une vie
        if stop == 1: 
            self.flag=0
            self.sens = (-1)*self.sens
            self.can.coords(self.boule,950,840,960,830)
            self.can.coords(self.barre,935,860,975,865)
            self.bar = 935
            self.coord=[950,840]
        #affichage game over
        if len(self.life)==0: 
            self.can.create_text(950,500,text='Game Over',fill='white')    
        
        if stop ==0 and self.pose==0: 
            self.can.after(2,self.go)

app = Principale(None)
app.mainloop()