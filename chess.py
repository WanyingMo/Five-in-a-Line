import pygame
from random import randint
from time import sleep
import tkinter as tk
import tkinter.messagebox
import pickle

border = 15#The record of board's border
mark = 10
MAX = 10000000#A big enough value
def Exploring(map, color):#scan function
    record = [[[0 for high in range(5)] for col in range(15)] for row in range(15)] #initilize a 3-dimensional list
    for i in range(15):
        for j in range(15):
            if map[i][j] == 0:#if it is null
                m = i
                n = j
                #if the up side chess the same color
                while n - 1 >= 0 and map[m][n - 1] == color:
                    n -= 1
                    record[i][j][0] += mark  #if same color, +10
                if n-1>=0 and map[m][n - 1] == 0:
                    record[i][j][0] += 1    #blank +1
                if n-1 >= 0 and map[m][n - 1] == -color:
                    record[i][j][0] -= 2    #other color, -2
                m = i
                n = j
                #if the down side the same color
                while (n + 1 < border  and map[m][n + 1] == color):
                    n += 1
                    record[i][j][0] += mark
                if n + 1 < border  and map[m][n + 1] == 0:
                    record[i][j][0] += 1
                if n + 1 < border  and map[m][n + 1] == -color:
                    record[i][j][0] -= 2
                m = i
                n = j
                #if left side chess the same color
                while (m - 1 >= 0 and map[m - 1][n] == color):
                    m -= 1
                    record[i][j][1] += mark
                if m - 1 >= 0 and map[m - 1][n] == 0:
                    record[i][j][1] += 1
                if m - 1 >= 0 and map[m - 1][n] == -color:
                    record[i][j][1] -= 2
                m = i
                n = j
                #if right side chess the same color
                while (m + 1 < border  and map[m + 1][n] == color):
                    m += 1
                    record[i][j][1] += mark
                if m + 1 < border  and map[m + 1][n] == 0:
                    record[i][j][1] += 1
                if m + 1 < border  and map[m + 1][n] == -color:
                    record[i][j][1] -= 2
                m = i
                n = j
                #if left-down side chess the same color
                while (m - 1 >= 0 and n + 1 < border  and map[m - 1][n + 1] == color):
                    m -= 1
                    n += 1
                    record[i][j][2] += mark
                if m - 1 >= 0 and n + 1 < border  and map[m - 1][n + 1] == 0:
                    record[i][j][2] += 1
                if m - 1 >= 0 and n + 1 < border  and map[m - 1][n + 1] == -color:
                    record[i][j][2] -= 2
                m = i
                n = j
                #if up-right side chess the same color
                while (m + 1 < border  and n - 1 >= 0 and map[m + 1][n - 1] == color):
                    m += 1
                    n -= 1
                    record[i][j][2] += mark
                if m + 1 < border  and n - 1 >= 0 and map[m + 1][n - 1] == 0:
                    record[i][j][2] += 1
                if m + 1 < border  and n - 1 >= 0 and map[m + 1][n - 1] == -color:
                    record[i][j][2] -= 2
                m = i
                n = j
                #if up-left side chess the same color
                while (m - 1 >= 0 and n - 1 >= 0 and map[m - 1][n - 1] == color):
                    m -= 1
                    n -= 1 
                    record[i][j][3] += mark
                if m - 1 >= 0 and n - 1 >= 0 and map[m - 1][n - 1] == 0:
                    record[i][j][3] += 1
                if m - 1 >= 0 and n - 1 >= 0 and map[m - 1][n - 1] == -color:
                    record[i][j][3] -= 2
                m = i
                n = j
                #if right-down side chess the same color
                while m + 1 < border  and n + 1 < border  and map[m + 1][n + 1] == color:
                    m += 1
                    n += 1
                    record[i][j][3] += mark
                if m + 1 < border  and n + 1 < border  and map[m + 1][n + 1] == 0:
                    record[i][j][3] += 1
                if m + 1 < border  and n + 1 < border  and map[m + 1][n + 1] == -color:
                    record[i][j][3] -= 2
    return record

def Estimate(record):#evaluation function
    for i in range(border):
        for j in range(border):
            record[i][j][4] = record[i][j][0]*1000 + record[i][j][1]*100 + record[i][j][2]*10 + record[i][j][3]#计算出该点的评估值（放大经过排序后的评估值）
    max_x = 0
    max_y = 0
    max = 0
    for i in range(border):
        for j in range(border):   #compare the evaluation value
            if max < record[i][j][4]:
                max = record[i][j][4]
                max_x = i
                max_y = j
    return max_x, max_y, max#return the max evaluation value and the location of the board

def Victory(x, y, color, location):#if it's five chess in a line
    c1, c2, c3, c4 = 0, 0, 0, 0
    i = x - 1
    while (i >= 0): #判断左右
        if location[i][y]==color:
            c1 += 1
            i -= 1
        else:
            break
    i = x + 1
    while i < border:
        if location[i][y] == color:
            c1 += 1
            i += 1
        else:
            break
    j = y - 1
    while (j >= 0):#up and down side
        if location[x][j] == color:
            c2 += 1
            j -= 1
        else:
            break
    j = y + 1
    while j < border:
        if location[x][j] == color:
            c2 += 1
            j += 1
        else:
            break
    i, j = x - 1, y - 1
    while (i >= 0 and j >= 0):#slant to the right side
        if location[i][j] == color:
            c3 += 1
            i -= 1
            j -= 1
        else:
            break
    i, j = x + 1, y + 1
    while (i < border and j < border):
        if location[i][j] == color:
            c3 += 1
            i += 1
            j += 1
        else:
            break
    i, j = x + 1, y - 1
    while (i < border and j >= 0):#slant to the left side
        if location[i][j] == color:
            c4 += 1
            i += 1
            j -= 1
        else:
            break
    i, j = x - 1, y + 1
    while (i > 0 and j < border):
        if location[i][j] == color:
            c4 += 1
            i -= 1
            j += 1
        else:
            break

    if c1 >= 4 or c2 >= 4 or c3 >= 4 or c4 >= 4:
        return True
    else:
        return False

def Sort(record):#sort the evaluation value of every direction, to enhance the evaluation of best direction in the following steps
    for i in record:
        for j in i:
            for a in range(5):
                for b in range(3, a - 1, -1):
                    if j[b - 1] < j[b]:
                        k = j[b]
                        j[b - 1] = j[b]
                        j[b] = k
    return record


def AI(ch, m, n):#the first and second round of AI
    a = [1,-1,1,-1,1,-1,0,0]
    b = [1,-1,-1,1,0,0,1,-1]
    rand = randint(0,7)
    while m+a[rand]>=0 and m+a[rand]<border and n+b[rand]>=0 and n+b[rand]<border and ch[m+a[rand]][n+b[rand]]!=0 :
        rand = randint(0,7)
    return m + a[rand], n+b[rand]

def AI_action(key, m, n, color, times):
    if times < 2:
        return AI(key, m, n)
    else:#record1 and record2 is used to let AI win and prevent player's chess win
        record1 = Exploring(key, -color)
        record2 = Exploring(key,color)
        record1 = Sort(record1)
        record2 = Sort(record2)
        max_x1, max_y1, max1 = Estimate(record1)
        max_x2, max_y2, max2 = Estimate(record2)
        if max1>max2 and max2<MAX:
            return max_x1,max_y1
        else:
            return max_x2,max_y2

class chess(object):
    def __init__(self):
        self.checkerboard = [[0 for high in range(15)] for col in range(15)] 

    def play_chess(self, x, y, color):
        if (x < 0 or x > border - 1 or y < 0 or y > border - 1):
            return
        self.checkerboard[x][y] = color

    def Empty(self, m, n):
        if self.checkerboard[m][n] != 0:
            return False
        else:
            return True
        
        

def GUI():
   window=tk.Tk()
   window.title('Five-in-a-Row')
   window.geometry('512x512')
   #load picture on the board
   canvas=tk.Canvas(window,height=512,width=512)
   imagefile=tk.PhotoImage(file='C:\\Users\\HP\\Desktop\\chess\\chess.gif')
   image=canvas.create_image(0,0,anchor='nw',image=imagefile)
   canvas.pack(side='top')
   #label user and password
   tk.Label(window,text='User:').place(x=150,y=50)
   tk.Label(window,text='Password:').place(x=150,y=90)
   var_usr_name=tk.StringVar()
   entry_usr_name=tk.Entry(window,textvariable=var_usr_name)
   entry_usr_name.place(x=200,y=50)
   var_usr_pwd=tk.StringVar()
   entry_usr_pwd=tk.Entry(window,textvariable=var_usr_pwd,show='*')
   entry_usr_pwd.place(x=200,y=90)
   #log in function
   def log_in():
      usr_name=var_usr_name.get()
      usr_pwd=var_usr_pwd.get()
      #try to get user information from local dictionary, if it does not exist, set up a local database
      try:
          with open('usr_info.pickle','rb') as usr_file:
              usrs_info=pickle.load(usr_file)
      except FileNotFoundError:
          with open('usr_info.pickle','wb') as usr_file:
              usrs_info={'admin':'admin'}
              pickle.dump(usrs_info,usr_file)
      #if User matches the password
      if usr_name in usrs_info:
          if usr_pwd == usrs_info[usr_name]:
              tk.messagebox.showinfo(title='welcome',message='Welcome：'+usr_name)
              window.destroy()
              main()
          else:
              tk.messagebox.showerror(message='Wrong Password')
      elif usr_name=='' or usr_pwd=='' :
          tk.messagebox.showerror(message='User or Password is null')
      else:
          is_signup=tk.messagebox.askyesno('Welcome','You have not sign up, do you want to sign up now?')
          if is_signup:
             sign_up()
    #sign up function
   def sign_up():
      def signtowcg():
          nn=new_name.get()
          np=new_pwd.get()
          npf=new_pwd_confirm.get()
          try:
              with open('usr_info.pickle','rb') as usr_file:
                  exist_usr_info=pickle.load(usr_file)
          except FileNotFoundError:
              exist_usr_info={}
          if nn in exist_usr_info:
              tk.messagebox.showerror('Error','User already exist')
          elif np =='' or nn=='':
              tk.messagebox.showerror('Error','User or password is null')
          elif np !=npf:
              tk.messagebox.showerror('Error','password is wrong')
          #if sign up information is right, record into local database
          else:
              exist_usr_info[nn]=np
              with open('usr_info.pickle','wb') as usr_file:
                  pickle.dump(exist_usr_info,usr_file)
              tk.messagebox.showinfo('Welcome','Sign up successfully!')
              window_sign_up.destroy()
      window_sign_up=tk.Toplevel(window)
      window_sign_up.geometry('350x200')
      window_sign_up.title('Sign up')
      new_name=tk.StringVar()
      tk.Label(window_sign_up,text='User：').place(x=10,y=10)
      tk.Entry(window_sign_up,textvariable=new_name).place(x=150,y=10)
      new_pwd=tk.StringVar()
      tk.Label(window_sign_up,text='Please input password：').place(x=10,y=50)
      tk.Entry(window_sign_up,textvariable=new_pwd,show='*').place(x=150,y=50)
      new_pwd_confirm=tk.StringVar()
      tk.Label(window_sign_up,text='Please input password again：').place(x=10,y=90)
      tk.Entry(window_sign_up,textvariable=new_pwd_confirm,show='*').place(x=150,y=90)
      bt_confirm_sign_up=tk.Button(window_sign_up,text='sign up',command=signtowcg)
      bt_confirm_sign_up.place(x=150,y=130)
   def explain():
      window_sign_up=tk.Toplevel(window)
      window_sign_up.geometry('200x200')
      window_sign_up.title('Instruction')
      tk.Label(window_sign_up,text='Welcome, dear player！\nThis game is a PVE game\nblack chess is player，white chess is Ai，\nHave fun!').place(x=10,y=10)
   bt_login=tk.Button(window,text='Sign in',command=log_in)
   bt_login.place(x=150,y=130)
   bt_logup=tk.Button(window,text='Sign up',command=sign_up)
   bt_logup.place(x=220,y=130)
   bt_logquit=tk.Button(window,text='Instruction',command=explain)
   bt_logquit.place(x=290,y=130)
   #Main cycle
   window.mainloop()
    
def main():
  key=chess()
  pygame.init()
  background = 'C:\\Users\\HP\\Desktop\\chess\\map.png'
  white_image = 'C:\\Users\\HP\\Desktop\\chess\\white.png'
  black_image = 'C:\\Users\\HP\\Desktop\\chess\\black.png'
  screen = pygame.display.set_mode((750, 750), 0, 32)
  background = pygame.image.load(background).convert()
  white = pygame.image.load(white_image).convert_alpha()
  black = pygame.image.load(black_image).convert_alpha()
  white = pygame.transform.smoothscale(white, (int(white.get_width() * 1.5), int(white.get_height() * 1.5)))
  black = pygame.transform.smoothscale(black, (int(black.get_width() * 1.5), int(black.get_height() * 1.5)))

  screen.blit(background, (0, 0))
  font = pygame.font.SysFont("黑体", 40)
  #Prevent these events put into queue
  pygame.event.set_blocked([1, 4, pygame.KEYUP, pygame.JOYAXISMOTION, pygame.JOYBALLMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION])
  #Admit these events put into queue
  pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, 12, pygame.KEYDOWN])
  dot_list = [(25 + i * 50 - white.get_width() / 2, 25 + j * 50 - white.get_height() / 2) for i in range(border) for j in range(border)]
  color = -1
  times = 0
  flag = False
  while not flag:
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  exit()
              elif event.type == pygame.MOUSEBUTTONDOWN:
                  x, y = pygame.mouse.get_pos() #Get the location of the mouse on the game screen
                  if 25 <= x <= 725 and 25 <= y <= 725 and ((x - 25) % 50 <= border or (x - 25) % 50 >= 0) and ((y - 25) % 50 <= border or (y - 25) % 50 >= 0):
                      color = -1 * color
                      m = int(round((x - 25) / 50))
                      n = int(round((y - 25) / 50))
                      if not key.Empty(m, n):#If there is a chess
                          continue
                      key.play_chess(m, n, color)
                      screen.blit(black, dot_list[border * m + n])#Player put his chess
                      if Victory(m, n, color, key.checkerboard):#If black chess win
                          screen.blit(font.render('Gameover,Black wins', True, (0, 0, 255)), (80, 600))
                          flag=True
                          exit()
                          break
                      color = -1 * color
                      sleep(0.1)
                      x, y = AI_action(key.checkerboard, m, n, color, times)
                      times += 1#round +1
                      key.play_chess(x, y, color)
                      screen.blit(white, dot_list[border * x + y])
                      if Victory(x, y, color, key.checkerboard):
                          screen.blit(font.render('Gameover,White wins', True, (0, 0, 255)), (80, 600))
                          flag=True
                          break
          if flag:
              screen.blit(font.render('The window will close in 10 seconds', True, (0, 0, 255)), (100, 400))
          pygame.display.update()
          if flag:
              sleep(10)
              pygame.quit()
              exit()    
GUI()

