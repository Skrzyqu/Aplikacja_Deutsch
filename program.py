from typing import Tuple
import customtkinter
import sqlite3
from CTkMessagebox import CTkMessagebox
import tkinter
from tkinter import ttk
from tkinter import *

class Session(customtkinter.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_rowconfigure((0,3), weight=1)
        self.grid_columnconfigure(1, weight=3)

        connection = sqlite3.connect('translator.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM kartkówka_04_04')
        self.rows = cursor.fetchall()
        connection.close()

        self.currentId = 0
        self.wrongAnswers = []
        self.wrongAnswer = 0
        self.id = 0

        self.translationLabel = customtkinter.CTkLabel(self, text=self.rows[self.currentId][1], font=('Calviri', 20),  anchor='center')
        self.translationLabel.grid(row=0, column=1, padx=50, pady=30, sticky='sewn')

        self.answerBar = customtkinter.CTkEntry(self, placeholder_text='Odpowiedź', width=600, height=30)
        self.answerBar.grid(row=1, column=1, padx=50, pady=30, sticky='new')

        frame = customtkinter.CTkFrame(self, fg_color='transparent')
        frame.grid(row=2, column=1, sticky='s')

        self.aBtn = customtkinter.CTkButton(frame, text='ä', fg_color='#FFFD88', text_color='black', command=self.aLetter, width=30, height=30)
        self.aBtn.grid(row=1, column=0, sticky='s', padx=5)
        
        self.aaBtn = customtkinter.CTkButton(frame, text='Ä', fg_color='#FFFD88', text_color='black', command=self.aaLetter, width=30, height=30)
        self.aaBtn.grid(row=1, column=1, sticky='s', padx=5)
        
        self.oBtn = customtkinter.CTkButton(frame, text='ö', fg_color='#FFFD88', text_color='black', command=self.oLetter, width=30, height=30)
        self.oBtn.grid(row=1, column=2, sticky='s', padx=5)
        
        self.ooBtn = customtkinter.CTkButton(frame, text='Ö', fg_color='#FFFD88', text_color='black', command=self.ooLetter, width=30, height=30)
        self.ooBtn.grid(row=1, column=3, sticky='s', padx=5)
        
        self.uBtn = customtkinter.CTkButton(frame, text='ü', fg_color='#FFFD88', text_color='black', command=self.uLetter, width=30, height=30)
        self.uBtn.grid(row=1, column=4, sticky='s', padx=5)
        
        self.uuBtn = customtkinter.CTkButton(frame, text='Ü', fg_color='#FFFD88', text_color='black', command=self.uuLetter, width=30, height=30)
        self.uuBtn.grid(row=1, column=5, sticky='s', padx=5)
        
        self.ssBtn = customtkinter.CTkButton(frame, text='ß', fg_color='#FFFD88', text_color='black', command=self.ssLetter, width=30, height=30)
        self.ssBtn.grid(row=1, column=6, sticky='s', padx=5)
        
        self.infoLabel  = customtkinter.CTkLabel(self, text='')
        self.infoLabel.grid(row=0, column=1, padx=50, pady=30, sticky='sew')

    def showNextQuestion(self):
        if self.rows:
            self.translationLabel.configure(text=self.rows[self.currentId][1])
            self.answerBar.delete(0, 'end')
            
        elif self.wrongAnswers:
                self.translationLabel.configure(text=self.wrongAnswers[self.currentId][1])
                self.answerBar.delete(0, 'end')
        
        elif not self.rows and not self.wrongAnswers:
                print('Obie są puste')
                self.endInfo()

    def checkAnswer(self):
        answer  = self.answerBar.get()
        if self.rows:
            if answer == self.rows[self.currentId][2]:
                self.infoLabel.configure(text=f'Poprawna odpowiedź', text_color='green')
                self.rows.remove(self.rows[self.currentId])

            else:
                self.infoLabel.configure(text=f'Błedna odpowieź. \n Poprawna: {self.rows[self.currentId][2]}', text_color='red')
                self.wrongAnswers.append(self.rows[self.currentId])
                self.wrongAnswer += 1
                self.rows.remove(self.rows[self.currentId])

            if self.wrongAnswer >= 20:
                self.showInfo()
                self.returnWrongAnswer()
                self.wrongAnswerWindow()
                self.wrongAnswer = 0
                self.wrongAnswers = []

            if self.currentId > len(self.rows) -1:
                self.currentId = 0

            self.showNextQuestion()
        else:
            if self.wrongAnswers:
                if answer == self.wrongAnswers[self.currentId][2]:
                    self.infoLabel.configure(text=f'Poprawna odpowiedź', text_color='green')
                    self.wrongAnswers.remove(self.wrongAnswers[self.currentId])
                    
                else:
                    self.infoLabel.configure(text=f'Błedna odpowieź. \n Poprawna: {self.wrongAnswers[self.currentId][2]}', text_color='red')
                    self.currentId += 1

                if self.currentId > len(self.wrongAnswers) -1:
                    self.currentId = 0
                
                self.showNextQuestion()
               

    def showInfo(self):
        CTkMessagebox(title='Info', message='20 razy źle odpowiedziałeś, otwarto nowe okno żeby zbić błędne odpowiedzi!!')

    def endInfo(self):
        CTkMessagebox(title='Info', message='Brawo znasz wszystkie słówka!')
    
    def aLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'ä')
    def aaLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'Ä')
    def oLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'ö')
    def ooLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'Ö')
    def uLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'ü')
    def uuLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'Ü')
    def ssLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'ß')

    def wrongAnswerWindow(self):
        self.master.changeFrameWrongWindow()

    def returnWrongAnswer(self):
        return self.wrongAnswers

class wrongWindow(customtkinter.CTkFrame):
    def __init__(self, parent, *args, wrongAnswers=None, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.wrongAnswers = wrongAnswers if wrongAnswers is not None else []
        self.currentId = 0
        self.grid_columnconfigure((0,2), weight=1)
        self.grid_rowconfigure((0,3), weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        self.translationLabel = customtkinter.CTkLabel(self, text=self.wrongAnswers[self.currentId][1], font=('Calviri', 20),  anchor='center')
        self.translationLabel.grid(row=0, column=1, padx=50, pady=30, sticky='sewn')

        self.answerBar = customtkinter.CTkEntry(self, placeholder_text='Odpowiedź', width=600, height=30)
        self.answerBar.grid(row=1, column=1, padx=50, pady=30, sticky='new')

        frame = customtkinter.CTkFrame(self, fg_color='transparent')
        frame.grid(row=2, column=1, sticky='s')

        self.aBtn = customtkinter.CTkButton(frame, text='ä', fg_color='#FFFD88', text_color='black', command=self.aLetter, width=30, height=30)
        self.aBtn.grid(row=1, column=0, sticky='s', padx=5)
        
        self.aaBtn = customtkinter.CTkButton(frame, text='Ä', fg_color='#FFFD88', text_color='black', command=self.aaLetter, width=30, height=30)
        self.aaBtn.grid(row=1, column=1, sticky='s', padx=5)
        
        self.oBtn = customtkinter.CTkButton(frame, text='ö', fg_color='#FFFD88', text_color='black', command=self.oLetter, width=30, height=30)
        self.oBtn.grid(row=1, column=2, sticky='s', padx=5)
        
        self.ooBtn = customtkinter.CTkButton(frame, text='Ö', fg_color='#FFFD88', text_color='black', command=self.ooLetter, width=30, height=30)
        self.ooBtn.grid(row=1, column=3, sticky='s', padx=5)
        
        self.uBtn = customtkinter.CTkButton(frame, text='ü', fg_color='#FFFD88', text_color='black', command=self.uLetter, width=30, height=30)
        self.uBtn.grid(row=1, column=4, sticky='s', padx=5)
        
        self.uuBtn = customtkinter.CTkButton(frame, text='Ü', fg_color='#FFFD88', text_color='black', command=self.uuLetter, width=30, height=30)
        self.uuBtn.grid(row=1, column=5, sticky='s', padx=5)
        
        self.ssBtn = customtkinter.CTkButton(frame, text='ß', fg_color='#FFFD88', text_color='black', command=self.ssLetter, width=30, height=30)
        self.ssBtn.grid(row=1, column=6, sticky='s', padx=5)
        
        self.infoLabel  = customtkinter.CTkLabel(self, text='')
        self.infoLabel.grid(row=0, column=1, padx=50, pady=30, sticky='sew')

    def showNextQuestion(self):
        if self.wrongAnswers:
            self.translationLabel.configure(text=self.wrongAnswers[self.currentId][1])
            self.answerBar.delete(0, 'end')
        else:
            self.showInfo()
            self.master.changeFrameSession()

    def checkWrongAnswer(self):
        answer  = self.answerBar.get()
        if answer == self.wrongAnswers[self.currentId][2]:
            self.infoLabel.configure(text=f'Poprawna odpowiedź', text_color='green')
            self.wrongAnswers.remove(self.wrongAnswers[self.currentId])
        else:
            self.infoLabel.configure(text=f'Błedna odpowieź. \n Poprawna: {self.wrongAnswers[self.currentId][2]}', text_color='red')
            self.currentId += 1
        

        if self.currentId > len(self.wrongAnswers) -1:
            self.currentId = 0
        
        self.showNextQuestion()

    def aLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'ä')
    def aaLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'Ä')
    def oLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'ö')
    def ooLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'Ö')
    def uLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'ü')
    def uuLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'Ü')
    def ssLetter(self):
        self.answerBar.insert(customtkinter.INSERT, 'ß')
    
    def showInfo(self):
        CTkMessagebox(title='Info', message='Brawo! Odpowiedziałeś poprawnie napisałeś te 20 słówek. Wracamy!')

class Listing(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background='#black', foreground='white', fieldbackground='#black', rowheight=25)

        connection =  sqlite3.connect('translator.db')
        cursor =  connection.cursor()
        cursor.execute('SELECT * FROM kartkówka_04_04')
        rows = cursor.fetchall()
        connection.close()

        treeFrame = ttk.Frame(self)
        treeFrame.pack(expand=True, fill='both')

        self.tree = ttk.Treeview(treeFrame)
        self.tree['columns'] = ('id', 'polski', 'niemiecki')
        self.tree["show"] = "headings"

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        
        self.tree.column('id', width=30)
        vsb = ttk.Scrollbar(treeFrame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')

        for row in rows:
            self.tree.insert('', 'end', values=row)
    
        self.tree.pack(expand=True, fill='both')

    def delete_selected(self):
        self.selectedItem = self.tree.selection()
        if self.selectedItem:
            self.selected_values = self.tree.item(self.selectedItem)['values']

            self.agreeAsk()
            
    def agreeAsk(self):
        askMessage = CTkMessagebox(title='Usunąć?', message='Czy na pewno chcesz usunąć ten rekord z bazy danych?', icon='question', option_1='Potwierdź', option_2='Anuluj')
        response = askMessage.get()

        if response == 'Potwierdź':
            connection = sqlite3.connect('translator.db')
            cursor = connection.cursor()
            cursor.execute('DELETE FROM kartkówka_04_04 WHERE id=? AND polski=? AND niemiecki=?', self.selected_values)
            connection.commit()
            connection.close()
            self.tree.delete(self.selectedItem)

class Adding(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_rowconfigure((0,4), weight=1)

        self.entryGerman = customtkinter.CTkEntry(self, placeholder_text='Niemieckie', width=300, height=50)
        self.entryGerman.grid(row=1, column=1, padx=30, pady=15)
        
        self.entryPolish = customtkinter.CTkEntry(self, placeholder_text='Polskie', width=300, height=50)
        self.entryPolish.grid(row=2, column=1, padx=30, pady=5)

        frame = customtkinter.CTkFrame(self, fg_color='transparent')
        frame.grid(row=3, column=1)

        self.aBtn = customtkinter.CTkButton(frame, text='ä', fg_color='#FFFD88', text_color='black', command=self.aLetter, width=30, height=30)
        self.aBtn.grid(row=0, column=0, sticky='s', padx=5)
        
        self.aaBtn = customtkinter.CTkButton(frame, text='Ä', fg_color='#FFFD88', text_color='black', command=self.aaLetter, width=30, height=30)
        self.aaBtn.grid(row=0, column=1, sticky='s', padx=5)
        
        self.oBtn = customtkinter.CTkButton(frame, text='ö', fg_color='#FFFD88', text_color='black', command=self.oLetter, width=30, height=30)
        self.oBtn.grid(row=0, column=2, sticky='s', padx=5)
        
        self.ooBtn = customtkinter.CTkButton(frame, text='Ö', fg_color='#FFFD88', text_color='black', command=self.ooLetter, width=30, height=30)
        self.ooBtn.grid(row=0, column=3, sticky='s', padx=5)
        
        self.uBtn = customtkinter.CTkButton(frame, text='ü', fg_color='#FFFD88', text_color='black', command=self.uLetter, width=30, height=30)
        self.uBtn.grid(row=0, column=4, sticky='s', padx=5)
        
        self.uuBtn = customtkinter.CTkButton(frame, text='Ü', fg_color='#FFFD88', text_color='black', command=self.uuLetter, width=30, height=30)
        self.uuBtn.grid(row=0, column=5, sticky='s', padx=5)
        
        self.ssBtn = customtkinter.CTkButton(frame, text='ß', fg_color='#FFFD88', text_color='black', command=self.ssLetter, width=30, height=30)
        self.ssBtn.grid(row=0, column=6, sticky='s', padx=5)

    def addWord(self):
        GermanWord = self.entryGerman.get()
        PolishWord = self.entryPolish.get()

        connection = sqlite3.connect('translator.db')
        cursor = connection.cursor()

        try:
            cursor.execute('INSERT INTO kartkówka_04_04 (polski, niemiecki) VALUES (?, ?)', (PolishWord, GermanWord))
            connection.commit()
            self.entryGerman.delete(0, 'end')
            self.entryPolish.delete(0, 'end')
        except Exception as e:
            self.errorMessage()
        
        finally:
            connection.close()
    
    def errorMessage(self):
        CTkMessagebox(title='Error', message='Nie udało się dodać słówka do bazy danych!!', icon='cancel')


    def aLetter(self):
        self.entryGerman.insert(customtkinter.INSERT, 'ä')
    def aaLetter(self):
        self.entryGerman.insert(customtkinter.INSERT, 'Ä')
    def oLetter(self):
        self.entryGerman.insert(customtkinter.INSERT, 'ö')
    def ooLetter(self):
        self.entryGerman.insert(customtkinter.INSERT, 'Ö')
    def uLetter(self):
        self.entryGerman.insert(customtkinter.INSERT, 'ü')
    def uuLetter(self):
        self.entryGerman.insert(customtkinter.INSERT, 'Ü')
    def ssLetter(self):
        self.entryGerman.insert(customtkinter.INSERT, 'ß')

class Settings(customtkinter.CTkFrame):
    pass

class mainPage(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class upperFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_rowconfigure((0,4), weight=1)

class lowerFrame(customtkinter.CTkFrame):
    def __init__(self, parent, right_frame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.grid_columnconfigure((0,2), weight=1)
        self.grid_rowconfigure((0,2), weight=1)

        self.defaultButton = customtkinter.CTkButton(self, height=90, width=300, text='')
        self.defaultButton.grid(row=1, column=1, pady=10,sticky='nsew')

    def addPage(self):
        self.button = customtkinter.CTkButton(self, height=90, width=300, text='Dodaj', fg_color='#16F529', text_color='black', font=('Calibri', 30), command=self.master.upperFrame.addWord)
        self.button.grid(row=1, column=1, pady=10,sticky='nsew')

    def sessionPage(self):
        self.button = customtkinter.CTkButton(self, height=90, width=300, text='Sprawdź', fg_color='#007100', font=('Calibri', 30), command=self.master.upperFrame.checkAnswer)
        self.button.grid(row=1, column=1, pady=10,sticky='nsew')

    def wrongAnswerPage(self):
        self.button = customtkinter.CTkButton(self, height=90, width=300, text='Sprawdź', fg_color='#007100', font=('Calibri', 30), command=self.master.upperFrame.checkWrongAnswer)
        self.button.grid(row=1, column=1, pady=10,sticky='nsew')

    def listPage(self):
        self.button = customtkinter.CTkButton(self, height=90, width=300, fg_color='red', font=('Calibri', 30), text='Usuń zaznaczony rekord', command=self.master.upperFrame.delete_selected)
        self.button.grid(row=1, column=1, pady=10, sticky='nsew')

    def mainPage(self):
        self.button = customtkinter.CTkButton(self, height=90, width=300, fg_color='#16F529', text_color='black', font=('Calibri', 30), text='Rozpocznij sesje', command=self.master.changeFrameSession)
        self.button.grid(row=1, column=1, pady=10, sticky='nsew')

class leftFrame(customtkinter.CTkFrame):
    def __init__(self, parent, right_frame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.right_frame = right_frame

        homePageButton = customtkinter.CTkButton(self, text='Strona główna', fg_color='#25C4F8', text_color='black', height=100, font=('Calibri', 30), corner_radius=0, border_color='black', border_width=2, command=self.mainPage)
        homePageButton.grid(column=0, row=0, sticky='ew', padx=0, pady=0)

        listPageButton = customtkinter.CTkButton(self, text='Lista słów',fg_color='#53E8D4', text_color='black', height=100, font=('Calibri', 30), corner_radius=0, border_color='black', border_width=2, command=self.listPage)
        listPageButton.grid(column=0, row=1, sticky='ew', padx=0, pady=0)

        addPageButton = customtkinter.CTkButton(self, text='Dodaj słowa', fg_color='#F20BF8', height=100, font=('Calibri', 30), corner_radius=0, border_color='black', border_width=2, command=self.addPage)
        addPageButton.grid(column=0, row=2, sticky='ew', padx=0, pady=0)

        choicePageButton = customtkinter.CTkButton(self, text='Wybierz materiał', fg_color='#150390', height=100, font=('Calibri', 30), corner_radius=0, border_color='black', border_width=2)
        choicePageButton.grid(column=0, row=3, sticky='ew', padx=0, pady=0)

        settingsPageButton = customtkinter.CTkButton(self, text='Ustawienia', fg_color='#1E0C2D', height=100, font=('Calibri', 30), corner_radius=0, border_color='black', border_width=2)
        settingsPageButton.grid(column=0, row=4, sticky='ew', padx=0, pady=0)
        

    def mainPage(self):
        self.right_frame.changeFrameMain()

    def addPage(self):
        self.right_frame.changeFrameAdding()

    def listPage(self):
        self.right_frame.changeFrameListing()

class rightFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.upperFrame = upperFrame(self, border_color='black', border_width=2)
        self.upperFrame.grid(row=0, column=0, sticky='nsew')

        self.sessionFrame = Session(self, border_color='black', border_width=2)
        self.sessionFrame.grid(row=0, column=0, sticky='nsew')
        self.sessionFrame.grid_remove()

        self.lowerFrame = lowerFrame(self, right_frame=self, height=100, border_color='black', border_width=2)
        self.lowerFrame.grid(row=1, column=0, sticky='nsew')
    def changeFrameMain(self):
        self.upperFrame.grid_forget()
        self.upperFrame = mainPage(self, border_color='black', border_width=2)
        self.upperFrame.grid(row=0, column=0, sticky='nsew')
        self.lowerFrame.mainPage()

    def changeFrameAdding(self):
        self.upperFrame.grid_forget()
        self.upperFrame = Adding(self, border_color='black', border_width=2)
        self.upperFrame.grid(row=0, column=0, sticky='nsew')
        self.lowerFrame.addPage()

    def changeFrameSession(self):
        self.upperFrame.grid_forget()
        self.upperFrame = self.sessionFrame
        self.upperFrame.grid(row=0, column=0, sticky='nsew')
        self.lowerFrame.sessionPage()
    
    def changeFrameWrongWindow(self):
        self.upperFrame.grid_forget()
        wrongAnswers = self.upperFrame.returnWrongAnswer()
        self.upperFrame = wrongWindow(self, wrongAnswers=wrongAnswers ,border_color='black', border_width=2)
        self.upperFrame.grid(row=0, column=0, sticky='nsew')
        self.lowerFrame.wrongAnswerPage()

    def changeFrameListing(self):
        self.upperFrame.grid_forget()
        self.upperFrame = Listing(self, border_color='black', border_width=2)
        self.upperFrame.grid(row=0, column=0, sticky='nsew')
        self.lowerFrame.listPage()
    
class mainFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        self.rightFrame = rightFrame(self)
        self.rightFrame.grid(row=0, column=1, sticky='nsew')

        self.leftFrame = leftFrame(self, right_frame=self.rightFrame)
        self.leftFrame.grid(row=0, column=0, sticky='nsew')

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        appWidth = 1100
        appHeight = 600
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        x = (screenWidth / 2) - (appWidth / 2)
        y = (screenHeight / 2) - (appHeight / 2)
        self.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')

        self.title('Fiszki')

        customtkinter.set_appearance_mode('dark')
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.mainFrame = mainFrame(self)
        self.mainFrame.grid(row=0, column=0, sticky='nsew')

        self.mainFrame.rightFrame.changeFrameMain()

app=App()
app.resizable(False, False)
app.mainloop()