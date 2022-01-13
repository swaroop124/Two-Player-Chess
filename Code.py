import tkinter as tk
import tkinter.messagebox as tkmsg
import os,sys
import string
from tkinter.constants import ANCHOR, BOTH, BOTTOM, SOLID, SUNKEN, TOP, X
import time
from PIL import Image,ImageTk
from PIL.ImageTk import PhotoImage

import TimeSelector

sys.setrecursionlimit(1500)

class ChessBoard(tk.Frame):
    def __init__(self,parent,l,w,minute,increase):
        tk.Frame.__init__(self,parent)
        self.parent=parent
        self.length=l
        self.width=w
        self.config(height=self.length*100,width=self.width*100)
        self.pack()

        

        self.square_colour=None
        self.winner=None
        
        #pyimage2 and pyimage9 is blank.png
        self.white_pieces = ["pyimage1", "pyimage3", "pyimage4", "pyimage5", "pyimage6", "pyimage7"] 
        self.black_pieces = ["pyimage8", "pyimage10", "pyimage11", "pyimage12", "pyimage13", "pyimage14"]
        self.columns=["a","b","c","d","e","f","g","h"]
        
        self.sq1=None  #initially presses square
        self.sq1_button=None
        self.sq2=None  # Second button that is pressed
        self.sq2_button=None
        self.piece_colour=None
        self.button_pressed=0
        self.turns=0
        self.squares={}
        self.white_images={}
        self.black_images={}

        self.wking_move=False
        self.bking_move=False
        self.wrook1_move=False
        self.wrook2_move=False
        self.brook1_move=False
        self.brook2_move=False
        self.castled=True  #CHECKS IF WHITE has CASTLE
        self.castled=True

        self.next_move_start=0
        self.next_move_end=0
        self.total_time=minute
        self.increment=increase
        self.white_time=tk.DoubleVar
        self.black_time=tk.DoubleVar
        self.white_time=self.total_time
        self.black_time=self.total_time
        self.white_label=None
        self.black_label=None

        Frame=tk.Frame(bg="mistyrose")
        Frame.pack(fill=X)
        Frame.columnconfigure(0,weight=1)
        Frame.columnconfigure(1,weight=1)
        tk.Label(Frame,text="White",font="Calibri 24 bold italic",relief=SOLID,borderwidth=4,bg="snow",fg="black").pack(anchor="nw",side="left",padx=20)
        self.white_label=tk.Label(Frame,text=self.white_time,width=5,font="Calibri 24 bold italic",relief=SOLID,borderwidth=4,bg="red",fg="black")
        self.white_label.pack(anchor="nw",side="left")
        tk.Label(Frame,text="Black",font="Calibri 24 bold italic",relief=SOLID,borderwidth=4,bg="dimgray",fg="ghostwhite").pack(anchor="ne",side="right",padx=20)
        self.black_label=tk.Label(Frame,text=self.black_time,width=5,font="Calibri 24 bold italic",relief=SOLID,borderwidth=4,bg="darkkhaki",fg="whitesmoke")
        self.black_label.pack(anchor="ne",side="right")
  
        
        self.set_squares()
    
    def clock(self):
        if self.white_time<=0:
            self.winner="Black"
            self.win()
        if self.black_time<=0:
            self.winner="White"
            self.win()
        
        if self.turns==1:
            self.white_label.config(bg="beige")
            self.black_label.config(bg="red")
        
        if self.turns==2:
            self.white_label.config(bg="red")
            self.black_label.config(bg="darkkhaki")
 
        if self.turns>1 and self.turns%2==1:
            self.white_time-=(self.next_move_end-self.next_move_start)
            self.white_time+=self.increment
            self.black_label.config(bg="red")
            self.white_label.config(bg="beige")
        
        
        if self.turns>2 and self.turns%2==0:
            self.black_time-=(self.next_move_end-self.next_move_start)
            self.black_time+=self.increment
            self.white_label.config(bg="red")
            self.black_label.config(bg="darkkhaki")
           
        self.white_time=round(self.white_time)
        self.black_time=round(self.black_time)
        self.white_label.config(text=self.white_time)
        self.black_label.config(text=self.black_time)

    def set_squares(self):
        #Creates a 8x8 buttons frame and also creates a list with the positions and the buttons
        for x in range(self.width):
            for y in range(self.length):
                if x%2==0 and y%2==0:
                    self.square_colour="darkkhaki"
                elif x%2==1 and y%2==1:
                    self.square_colour="darkkhaki"
                else:
                    self.square_colour="beige"
                
                
                a=["a","b","c","d","e","f","g","h"]
                for i in range(len(a)):
                  L=tk.Label(self,text=f"{a[i]}",width=12,height=2,bg="mistyrose",padx=0)
                  L.grid(row=9,column=i+1)
                  L.configure(highlightthickness=0)
                for i in range(1,9):
                    L=tk.Label(self,text=f"{i}",width=3,height=5,bg="mistyrose")
                    L.grid(row=9-i,column=0)
                    L.configure(highlightthickness=0)
                
                #Creates Buttons on 8x8 grid
                B=tk.Button(self,bg=self.square_colour,activebackground="cyan")
                B.grid(row=8-x,column=y+1)
                
                #Stores the positions and buttons in a dictionary named self.squares
                pos=string.ascii_lowercase[y]+str(x+1)
                self.squares.setdefault(pos,B)
                
                #Calls the select piece function when the button is clicked and passed the button that is pressed to the function
                self.squares[pos].config(command=lambda key=self.squares[pos]: self.piece_selected(key))

    def importing_pieces(self):
        #Creates a list of the white pieces and stores in 'whites'  Similarly for BLACK
        p_white=os.path.join(os.path.dirname(__file__),"White")
        whites=os.listdir(p_white)
        p_black=os.path.join(os.path.dirname(__file__),"Black")
        blacks=os.listdir(p_black)
        
        #Stores the images in the class variable for both black pieces as well as white pieces
        for i in whites:
            img=Image.open(p_white+"\\"+i)
            img=img.resize((80,80),Image.ANTIALIAS)
            img=ImageTk.PhotoImage(image=img)
            self.white_images.setdefault(i,img)

        for i in blacks:
            img=Image.open(p_black+"\\"+i)
            img=img.resize((80,80),Image.ANTIALIAS)
            img=ImageTk.PhotoImage(image=img)
            self.black_images.setdefault(i,img)

    def setting_pieces(self):
        row_1={"a1":"rook.png","b1":"knight.png","c1":"bishop.png","d1":"queen.png","e1":"king.png","f1":"bishop.png","g1":"knight.png","h1":"rook.png"}
        row_8={"a8":"rook.png","b8":"knight.png","c8":"bishop.png","d8":"queen.png","e8":"king.png","f8":"bishop.png","g8":"knight.png","h8":"rook.png"}
        pawn_list=["a","b","c","d","e","f","g","h"]

        for i in row_1:
            start_piece=row_1[i]
            self.squares[i].config(image=self.white_images[start_piece])
            #Link the image of the piece to the square
            self.squares[i].image=self.white_images[start_piece]
        
        for i in row_8:
            start_piece=row_8[i]
            self.squares[i].config(image=self.black_images[start_piece])
            self.squares[i].image=self.black_images[start_piece]

        for i in pawn_list:
            self.squares[i+str(2)].config(image=self.white_images['pawn.png'])
            self.squares[i+str(2)].image=self.white_images['pawn.png']
            self.squares[i+str(7)].config(image=self.black_images['pawn.png'])
            self.squares[i+str(7)].image=self.black_images['pawn.png']
        
        for i in range(3,7):
            for j in pawn_list:
                self.squares[j+str(i)].config(image=self.white_images['blank.png'])

    def piece_selected(self,b):
        if (b["image"] in self.white_pieces and self.button_pressed==0):
            self.piece_colour="white"
        if (b["image"] in self.black_pieces and self.button_pressed==0):
            self.piece_colour="black"
        
        #Checks which colour's turns is going on currently
        if ((self.piece_colour=="white" and self.turns%2==0) or (self.piece_colour=="black" and self.turns%2==1) or self.button_pressed==1):
            if self.button_pressed==0:
                
                self.sq1 = list(self.squares.keys())[list(self.squares.values()).index(b)] #Address of the selected square
                self.sq1_button=b
                self.button_pressed+=1

            elif (self.button_pressed==1):
                self.sq2 = list(self.squares.keys())[list(self.squares.values()).index(b)]
                self.sq2_button=b
                #Prevents self destruction of the same piece if Square 1 and square 2 are the same
                if (self.sq1==self.sq2):
                    self.button_pressed=0
                    return
                

                if ((self.allowed_move()==True) and (self.same_team()==False)):
                    self.next_move_end=time.time()
                    psq1 = self.sq1
                    psq1_button = self.sq1_button["image"]
                    psq2 = self.sq2
                    psq2_button = self.sq2_button["image"]
                    self.squares[self.sq2].config(image=self.sq1_button["image"]) #moves pice in sq1 to sq2
                    self.squares[self.sq2].image = self.sq1_button["image"]
                    self.squares[self.sq1].config(image=self.white_images["blank.png"]) #clears sq1
                    self.squares[self.sq1].image = self.white_images["blank.png"]

                    if self.check()==True and self.castle()==False:
                        self.squares[psq2].config(image=psq2_button) 
                        self.squares[psq2].image = psq2_button
                        self.squares[psq1].config(image=psq1_button)
                        self.squares[psq1].image = psq1_button
                        self.buttons_pressed = 0
                        self.adjacent_king_squares()
                        return
                    else:
                        if psq1_button=="pyimage3":
                            self.wking_move=True
                            self.castled=False
                        elif psq1_button=="pyimage10":
                            self.bking_move=True
                            self.castled=False
                        elif psq1_button=="pyimage7" and psq1=="a1":
                            self.wrook1_move=True
                            self.castled=False
                        elif psq1_button=="pyimage7" and psq1=="h1":
                            self.wrook2_move=True
                            self.castled=False
                        elif psq1_button=="pyimage14" and psq1=="a8":
                            self.brook1_move=True
                            self.castled=False
                        elif psq1_button=="pyimage14" and psq1=="h8":
                            self.brook2_move=True
                            self.castled=False
                        elif (b["image"] == "pyimage5" and psq2.count("8")==1) or (b["image"] == "pyimage12" and psq2.count("1")==1): 
                            # print(self.sq2)
                            self.promo(self.piece_colour,psq2)
                        
                        self.turns+=1
                        self.button_pressed=0
                        self.clock()
                        self.next_move_start=time.time()
                        
                
                
                else:
                    tkmsg.showerror("Invalid Move","The previous move played was invalid!")
                self.button_pressed=0   ###########
            
        else:
            self.buttons_pressed = 0
            return
    
    def adjacent_king_squares(self):
        if self.piece_colour=="white":
            piece="pyimage3"
        elif self.piece_colour=="black":
            piece="pyimage10"
        square=self.find_piece(piece)
        valid_squares=[]
        
        checkmate=True
        
        if square[1]!=str(8) and self.squares[str(square[0])+str(int(square[1])+1)]["image"]=="pyimage2":
            valid_squares.append(str(square[0])+str(int(square[1])+1))
        
        if square[1]!=str(1) and self.squares[str(square[0])+str(int(square[1])-1)]["image"]=="pyimage2":

            valid_squares.append(str(square[0])+str(int(square[1])-1))
        
        if self.columns.index(square[0])!=7 and self.squares[str(self.columns[self.columns.index(square[0])+1])+str(square[1])]["image"]=="pyimage2":

            valid_squares.append(str(self.columns[self.columns.index(square[0])+1])+str(square[1]))
        
        if self.columns.index(square[0])!=1 and self.squares[str(self.columns[self.columns.index(square[0])-1])+str(square[1])]["image"]=="pyimage2":

            valid_squares.append(str(self.columns[self.columns.index(square[0])-1])+str(square[1]))
        
        if square[1]!=str(8) and self.columns.index(square[0])!=7 and self.squares[str(self.columns[self.columns.index(square[0])+1])+str(int(square[1])+1)]["image"]=="pyimage2":

            valid_squares.append(str(self.columns[self.columns.index(square[0])+1])+str(int(square[1])+1))
        
        if square[1]!=str(1) and self.columns.index(square[0])!=7 and self.squares[str(self.columns[self.columns.index(square[0])+1])+str(int(square[1])-1)]["image"]=="pyimage2":
 
            valid_squares.append(str(self.columns[self.columns.index(square[0])+1])+str(int(square[1])-1)) 
        
        if square[1]!=str(8) and self.columns.index(square[0])!=1 and self.squares[str(self.columns[self.columns.index(square[0])-1])+str(int(square[1])+1)]["image"]=="pyimage2":

            valid_squares.append(str(self.columns[self.columns.index(square[0])-1])+str(int(square[1])+1))
        
        if square[1]!=str(1) and self.columns.index(square[0])!=1 and self.squares[str(self.columns[self.columns.index(square[0])-1])+str(int(square[1])-1)]["image"]=="pyimage2":

            valid_squares.append(str(self.columns[self.columns.index(square[0])-1])+str(int(square[1])-1))

        for i in valid_squares:
            if self.check(self.piece_colour,i)==False:

                checkmate=False
                break

        if (checkmate==True):
            if self.piece_colour=="white":
                self.winner="Black"
            if self.piece_colour=="black":
                self.winner="White"
            self.win()

    def win(self):
        tkmsg.showinfo("Game Over!",f"{self.winner} wins!")

    def promo(self,colour,psq2):
        def import_piece(p):
            # print(self.sq2)
            self.squares[psq2].config(image=p)
            self.squares[psq2].image=p
            promo_box.destroy()
            return

        promo_box=tk.Tk()
        promo_box.title("Which piece do you want to promote to?")
        if colour=="white":
            tk.Button(promo_box,text="Rook",command=lambda: import_piece("pyimage7")).grid(row=0,column=0)
            tk.Button(promo_box,text="Knight",command=lambda: import_piece("pyimage4")).grid(row=0,column=1)
            tk.Button(promo_box,text="Bishop",command=lambda: import_piece("pyimage1")).grid(row=1,column=0)
            tk.Button(promo_box,text="Queen",command=lambda: import_piece("pyimage6")).grid(row=1,column=1)
        if colour=="black":
            tk.Button(promo_box,text="Rook",command=lambda: import_piece("pyimage14")).grid(row=0,column=0)
            tk.Button(promo_box,text="Knight",command=lambda: import_piece("pyimage11")).grid(row=0,column=1)
            tk.Button(promo_box,text="Bishop",command=lambda: import_piece("pyimage8")).grid(row=1,column=0)
            tk.Button(promo_box,text="Queen",command=lambda: import_piece("pyimage13")).grid(row=1,column=1)
        promo_box.mainloop()
        return
    
    def clean_path(self,piece):
        if piece=="rook" or piece=="queen":
            #VERTICAL Movement
            if self.sq1[0]==self.sq2[0]:
                initial=min(int(self.sq1[1]),int(self.sq2[1]))
                final=max(int(self.sq1[1]),int(self.sq2[1]))
                for i in range(initial+1,final):
                    cell=self.squares[str(self.sq1[0]+str(i))]
                    if cell["image"]!="pyimage2":
                        return False
            #HORIZONTAL Movement
            if self.sq1[1]==self.sq2[1]:
                initial=min(self.columns.index(self.sq1[0]),self.columns.index(self.sq2[0]))
                final=max(self.columns.index(self.sq1[0]),self.columns.index(self.sq2[0]))
                for i in range(initial+1,final):
                    cell=self.squares[str(self.columns[i]+str(self.sq1[1]))]
                    if cell["image"]!="pyimage2":
                        return False

        if piece=="bishop" or piece=="queen":
            x1=self.columns.index(self.sq1[0])
            x2=self.columns.index(self.sq2[0])
            y1=int(self.sq1[1])
            y2=int(self.sq2[1])

            if x1<x2:
                if y2>y1:#NE
                    for i in range(x1+1,x2):
                        y1+=1
                        cell=self.squares[self.columns[i]+str(y1)]
                        if cell["image"]!="pyimage2":
                            return False
                if y1>y2:#SE
                    for i in range(x1+1,x2):
                        y1-=1
                        cell=self.squares[self.columns[i]+str(y1)]
                        if cell["image"]!="pyimage2":
                            return False
            if x1>x2:
                if y2>y1:#NW
                    for i in range(x1-1, x2, -1):
                        y1+=1
                        cell=self.squares[self.columns[i]+str(y1)]
                        if cell["image"]!="pyimage2":
                            return False
                if y1>y2:#SW
                    for i in range(x1-1, x2, -1):
                        y1-=1
                        cell=self.squares[self.columns[i]+str(y1)]
                        if cell["image"]!="pyimage2":
                            return False

        return True

    def same_team(self):
        if self.piece_colour=="white" and self.sq2_button["image"] in self.white_pieces:
            return True
        elif self.piece_colour=="black" and self.sq2_button["image"] in self.black_pieces:
            return True
        else:
            return False

    def allowed_move(self):

        if self.sq1_button["image"]=="pyimage2" or self.sq1_button["image"]=="pyimage9":
            return False
        
        #Movement for white pawn
        if self.sq1_button["image"]=="pyimage5":
            if (int(self.sq2[1])==int(self.sq1[1])+1) and (self.sq2[0]==self.sq1[0]) and (self.sq2_button["image"]=="pyimage2"):
                return True
            
            if int(self.sq1[1])==2 and (self.sq2[0]==self.sq1[0]) and (int(self.sq2[1])==int(self.sq1[1])+2) and (self.squares[str(self.sq1[0])+str(int(self.sq1[1])+1)])["image"]=="pyimage2":
                return True
            
            if int(self.sq1[1]) == int(self.sq2[1])-1 and abs(self.columns.index(self.sq1[0]) - self.columns.index(self.sq2[0])) == 1 and self.sq2_button["image"] != "pyimage2":
                return True 

        #Movement for Black Pawn
        if self.sq1_button["image"]=="pyimage12":
            if (int(self.sq2[1])==int(self.sq1[1])-1) and (self.sq2[0]==self.sq1[0]) and (self.sq2_button["image"]=="pyimage2"):
                return True
            
            if int(self.sq1[1])==7 and (self.sq2[0]==self.sq1[0]) and (int(self.sq2[1])==int(self.sq1[1])-2) and (self.squares[str(self.sq1[0])+str(int(self.sq1[1])-1)])["image"]=="pyimage2":
                return True
            
            if int(self.sq1[1]) == int(self.sq2[1])+1 and abs(self.columns.index(self.sq1[0]) - self.columns.index(self.sq2[0])) == 1 and self.sq2_button["image"] != "pyimage2":
                return True

        #Movement for rook
        if self.sq1_button["image"]=="pyimage7" or self.sq1_button["image"]=="pyimage14":
            if ((int(self.sq2[1])==int(self.sq1[1])) or (self.sq2[0]==self.sq1[0])) and self.clean_path("rook"):
                return True

        #Movement for knight
        if self.sq1_button["image"]=="pyimage4" or self.sq1_button["image"]=="pyimage11":
            if (abs(int(self.sq1[1]) - int(self.sq2[1])) == 2) and (abs(self.columns.index(self.sq1[0]) - self.columns.index(self.sq2[0])) == 1): #allows tall L moves
                return True
            if (abs(int(self.sq1[1]) - int(self.sq2[1])) == 1) and (abs(self.columns.index(self.sq1[0]) - self.columns.index(self.sq2[0])) == 2): #allows wide L moves
                return True

        #Movement for bishop
        if self.sq1_button["image"]=="pyimage1" or self.sq1_button["image"]=="pyimage8":
            if (abs(int(self.sq2[1])-int(self.sq1[1]))==abs(self.columns.index(self.sq2[0])-self.columns.index(self.sq1[0]))) and self.clean_path("bishop"):
                return True

        #Movement for queen
        if self.sq1_button["image"]=="pyimage6" or self.sq1_button["image"]=="pyimage13":
            if ((int(self.sq2[1])==int(self.sq1[1])) or (self.sq2[0]==self.sq1[0])) and self.clean_path("queen"):
                return True
            if (abs(int(self.sq2[1])-int(self.sq1[1]))==abs(self.columns.index(self.sq2[0])-self.columns.index(self.sq1[0]))) and self.clean_path("queen"):
                return True

        #Movement for king
        if self.sq1_button["image"]=="pyimage3" or self.sq1_button["image"]=="pyimage10":
            if (abs(int(self.sq1[1]) - int(self.sq2[1])) < 2) and (abs(self.columns.index(self.sq1[0]) - self.columns.index(self.sq2[0]))) < 2: #allows 1 square moves
                return True
            if self.castle() is True:
                return True

        return False

    def find_piece(self,p):
        for i in self.squares:
            if (self.squares[i])["image"]==p:
                return i
        return -1

    def check(self,colour=None,sq=None): #prevents a move if king is under attack
        previous_sq1 = self.sq1 #stores current values assigned to values
        previous_sq1_button = self.sq1_button
        previous_sq2 = self.sq2
        previous_sq2_button = self.sq2_button
        if colour==None:
            colour=self.piece_colour
        
        def return_previous_values():
            self.sq1 = previous_sq1
            self.sq1_button = previous_sq1_button
            self.sq2 = previous_sq2
            self.sq2_button = previous_sq2_button
            
        if colour == "white": 
            if sq==None:
                self.sq2 = self.find_piece("pyimage3") #calls find_king function to find pos of king
            else:
                self.sq2=sq
            for key in self.squares: #iterates through each square
                self.sq1 = key
                self.sq1_button = self.squares[self.sq1]
                if self.sq1_button["image"] in self.black_pieces:
                    
                    if self.allowed_move(): #checks to see if the king's current pos is a possible move for the piece
                        tkmsg.showwarning("Check","White King is/will be in Check!")
                        return True
        
        if colour == "black":
            if sq==None:
                self.sq2 = self.find_piece("pyimage10")
            else:
                self.sq2=sq
            for key in self.squares:
                self.sq1 = key
                self.sq1_button = self.squares[self.sq1] 
                if self.sq1_button["image"] in self.white_pieces:
                    if self.allowed_move():
                        tkmsg.showwarning("Check","Black King is/will be in Check!")
                        return True
        return_previous_values()
        return False
     
    def castle(self):
        if self.wking_move==False and self.wrook1_move==False and self.sq2=="c1" and self.check("white")==False and self.check("white","c1")==False:
            for i in range(1,4):
                if self.squares[self.columns[i]+str(1)]["image"]!="pyimage2":
                    return False
            self.squares["a1"].config(image="pyimage2")
            self.squares["a1"].image = "pyimage2"
            self.squares["d1"].config(image="pyimage7")
            self.squares["d1"].image = ("pyimage7")
            self.castled=True
            return True
        if self.wking_move==False and self.wrook2_move==False and self.sq2=="g1" and self.check("white")==False and self.check("white","g1")==False:
            for i in range(5,7):
                if self.squares[self.columns[i]+str(1)]["image"]!="pyimage2":
                    return False
            self.squares["h1"].config(image="pyimage2")
            self.squares["h1"].image = "pyimage2"
            self.squares["f1"].config(image="pyimage7")
            self.squares["f1"].image = ("pyimage7")
            self.castled=True
            return True
        if self.bking_move==False and self.wrook1_move==False and self.sq2=="c8" and self.check("black")==False and self.check("black","c8")==False:
            for i in range(1,4):
                if self.squares[self.columns[i]+str(8)]["image"]!="pyimage2":
                    return False
            self.squares["a8"].config(image="pyimage2")
            self.squares["a8"].image = "pyimage2"
            self.squares["d8"].config(image="pyimage14")
            self.squares["d8"].image = ("pyimage14")
            self.castled=True
            return True
        if self.bking_move==False and self.wrook2_move==False and self.sq2=="g8" and self.check("black")==False and self.check("white","g8")==False:
            for i in range(5,7):
                if self.squares[self.columns[i]+str(8)]["image"]!="pyimage2":
                    return False
            self.squares["h8"].config(image="pyimage2")
            self.squares["h8"].image = "pyimage2"
            self.squares["f8"].config(image="pyimage14")
            self.squares["f8"].image = ("pyimage14")
            self.castled=True
            return True
        
        return False

    

a=TimeSelector.time_selector()
minute,increase=a.split("|")

root=tk.Tk()
root.title("Two Player Chess")
root.geometry("800x800")
root.minsize(740,730)
root.config(bg="mistyrose")
board=ChessBoard(root,8,8,int(minute)*60,int(increase))
board.importing_pieces()
board.setting_pieces()


board.mainloop()
