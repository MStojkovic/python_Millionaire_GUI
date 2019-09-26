# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 18:54:29 2018

@author: Igor
"""

from tkinter import *
from functools import partial
import random
import time

class App:
    def __init__(self, master):
        self.frame = Frame(master, bg="royal blue", height = 50, width = 200)
        self.frame.pack()
        self.btn_list = []
        self.wait = IntVar()
        self.theEnd = 0
        self.prizes = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 250000, 500000, 1000000]
        self.menu()
        
        
    def menu(self):
        photo = PhotoImage(file = "milionario.gif")
        self.photoLabel = Label(self.frame, image = photo)
        self.photoLabel.image = photo
        self.photoLabel.grid(row = 0)
        
        self.newGame = Button(self.frame, text = "New Game", borderwidth = 1, width = 50, bg = "blue", command =self.game)
        self.newGame.grid(row = 1)
        
        self.exitButton = Button(self.frame, text = "Exit", borderwidth = 1, width = 50, bg = "blue", command = self.frame.quit)
        self.exitButton.grid(row = 2)
        
    def generateQuestions(self):
        fileQuestions = open('domande.txt', 'r')
        rows = fileQuestions.readlines()
        fileQuestions.close()
        
        self.questions = []
        self.answers = []
        self.correctAnswers = []
        
        self.questionFill(rows)
        
        fileAnswers = open('risposte.txt', 'r')
        rows = fileAnswers.readlines()
        fileAnswers.close()
        self.answerFill(rows)
                
    def questionFill(self, rows):

        for row in rows:
            if (row[0] != '*'):
                question = {
                        'text': row.strip('\n'),
                        'used': 0
                }
                self.questions.append(question)
    def asignCorrectLetter(self, counter):
        if (counter == 0):
            return ('A:')
        elif (counter == 1):
            return ('B:')
        elif (counter == 2):
            return ('C:')
        else:
            return ('D:')
                
    def answerFill(self, rows):
        
        answersList = []
        
        for row in rows:
            if (row[0] != '*'):
                answersList = row.split('/')
                counter = 0
                answerList = []
                for answer in answersList:
                    if (answer[0] == '-'):
                        answerList.append(self.asignCorrectLetter(counter) + answer.strip('-'))
                        counter += 1
                    else:
                        answerList.append(self.asignCorrectLetter(counter) + answer.strip('+'))
                        self.asignCorrectAnswer(counter)
                        counter += 1
                answerList[3] = answerList[3].strip('\n')
                answerDict = {
                        "A":answerList[0],
                        "B":answerList[1],
                        "C":answerList[2],
                        "D":answerList[3]
                }
                self.answers.append(answerDict)
    
    
        
    def asignCorrectAnswer(self, counter):
        if (counter == 0):
            self.correctAnswers.append('a')
        elif (counter == 1):
            self.correctAnswers.append('b')
        elif (counter == 2):
            self.correctAnswers.append('c')
        else:
            self.correctAnswers.append('d')
                
    def game(self):
        self.generateQuestions()
        
        self.photoLabel.grid_remove()
        self.newGame.grid_remove()
        self.exitButton.grid_remove()
        
        self.introductionLabel = Label(self.frame, text = '', height = 2, width = 150, bg = "royal blue", anchor = "center", borderwidth = 1)
        self.introductionLabel.grid(row = 0, columnspan = 2, sticky = "we")
        
        self.questionLabel = Label(self.frame, text= '', height = 5, width = 150, bg = "blue", anchor = "center", borderwidth = 1)
        self.questionLabel.grid(row = 1, columnspan = 2, sticky = "we")

        btnRow = 2
        btnCol = 0
        for i in range(4):
            self.button = Button(self.frame, text = '', borderwidth = 1, height = 2, width = 50, bg = "blue", activebackground = "yellow", anchor = "center", command = lambda idx = i: self.onClick(idx))
            self.button.grid(row = btnRow, column = btnCol)
            if (btnCol == 0):
                btnCol += 1
            else:
                btnRow += 1
                btnCol = 0
                
            self.btn_list.append(self.button)

        self.izlaz = Button(self.frame, text="QUIT", fg="red", command=self.exitGame)
        self.izlaz.grid(row = 4, columnspan = 2)
        
        level = 0 #razina pitanja 0-14
        self.questionGroup = 0 #skupina pitanja po pragovima u milijunasu 0-2
        play = 1

        while play:           
            self.introductionLabel.configure(text = ('Domanda per ' + str(self.prizes[level]) + ' kn'))
            self.questionNumber = self.questionGroup * 30 + self.generateRandomInt()

            self.questionLabel.configure(text = self.questions[self.questionNumber]["text"])
            self.btn_list[0].configure(text = self.answers[self.questionNumber]["A"], state = "normal", bg = "blue") 
            self.btn_list[1].configure(text = self.answers[self.questionNumber]["B"], state = "normal", bg = "blue")
            self.btn_list[2].configure(text = self.answers[self.questionNumber]["C"], state = "normal", bg = "blue")
            self.btn_list[3].configure(text = self.answers[self.questionNumber]["D"], state = "normal", bg = "blue")

            self.btn_list[0].wait_variable(self.wait)        
            
            time.sleep(2)
            if (self.theEnd < 1):
                level += 1
                if (level > 14):
                  self.introductionLabel.configure(text = 'Congratulazioni, avete vinto 1000000kn') 
                  self.removeFromGrid()
                elif (level == 5):
                    self.questionGroup += 1
                elif (level == 10):
                    self.questionGroup += 1
            else:
                play = 0
                if (level < 5):
                    self.introductionLabel.configure(text = 'La risposta e sbagliata, avete vinto 0 kn')
                elif (level < 10):
                    self.introductionLabel.configure(text = 'La risposta e sbagliata, avete vinto 1000 kn')
                else:
                    self.introductionLabel.configure(text = 'La risposta e sbagliata, avete vinto 32000 kn')
                for btn in self.btn_list:
                    if (self.answerValidation(btn.cget("text"))):
                        btn.configure(bg = "chartreuse")
                 
            """ self.newGameButton = Button(self.frame, text = "New Game", borderwidth = 1, bg = "blue", command =self.game)
            self.newGame.grid(row = 5, columnspan = 2)"""
                    
        
    def removeFromGrid(self):
        self.questionLabel.grid_remove()
        for b in self.btn_list:
            b.grid_remove()
        
    def onClick(self, idx):
        for b in self.btn_list:
            b.configure(state = "disabled")
                
            if (self.answerValidation(self.btn_list[idx].cget("text"))):
                self.btn_list[idx].configure(bg = "chartreuse")
            else:
                self.btn_list[idx].configure(bg = "red")
                self.theEnd = 1
            #time.sleep(3)    
            self.wait.set(1)
    
    def answerValidation(self, ans):
        ans = ans.split(':')
        if (ans[0].lower() == self.correctAnswers[self.questionNumber]):
            return 1
        else:
            return 0
        
    def generateRandomInt(self):
        
        keepGoing = 1
        while (keepGoing):
            number = random.randint(0, 29)
            questionNumber = number + self.questionGroup * 30
            if (self.questions[questionNumber]["used"] == 0):
                self.questions[questionNumber]["used"] = 1
                keepGoing = 0
                return number 
            else:
                number = random.randint(0, 29)
    
    def exitGame(self):
        self.wait.set(0)
        root.destroy()
        
root = Tk()

app = App(root)

root.mainloop()
root.destroy()                    
                    
                    
                
            
            
        
        
        
        
        
        
        
        