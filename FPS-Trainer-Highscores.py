import json
import os
import os.path
import tkinter as tk
from functools import partial
import random
from tkinter.messagebox import askyesno, showinfo

window = tk.Tk()
window.geometry("1000x500")
window.resizable(False, False)
window.config(bg="blue")
window.title("FPS Trainer V1")

timer = 20
points = 0
bindingList = ["<w>", "<a>", "<s>", "<d>", "<space>", "<Button-1>", "<Double-Button-1>", "<Triple-Button-1>"]
printTask = ["press: w", "press: a", "press: s", "press: d", "press: space", "Single click", "Double click", "Triple click", ]
highscoresDict = None

def startupGame(startButton):
    startButton.destroy()
    window.config(bg="gray")
    labelScore.after(1000, time)
    runGame()


def runGame():
    chosenTaskposition = random.randrange(0,8)
    createButton(chosenTaskposition)



def time():
    global timer
    timer -= 1
    labelScore.config(text=("Time remaining: " + str(timer) + "                                                                                                         " + "Points: " + str(points)), font=("arial", 12))
    if timer == 0:
        window.after(2000, popupMSG)
    else:
        labelScore.after(1000, time)


def createButton(position):
    if timer > 0:
        xCord = random.randrange(50,950)
        yCord = random.randrange(100,450)
        button = tk.Button()
        button.config(text=printTask[position])
        button.pack(ipadx=10, ipady=10)
        button.place(x=xCord,y=yCord)
        if position <= 5:
            window.bind(bindingList[position], partial(PressedClicked, position, button))
        else:
            button.bind(bindingList[position], partial(PressedClicked, position, button))


def scoreName():
    showinfo(title= "New highscore!!!", message= "U heeft een highscore behaald! Vul a.u.b een naam in voor de score")
    scoreLabel = tk.Label(bg='gray', text="Vul hier naam in:", font=("arial", 18))
    scoreLabel.place(x=400, y=250)
    entryScore = tk.Entry()
    entryScore.place(x=400, y=280)
    scoreButton = tk.Button(text="Invullen", command=scoreButtoncheck)
    scoreButton.place(x=500, y=280)
    print("waiting...")
    scoreButton.wait_variable()
    print("done waiting.")


def scoreButtoncheck():
    ...


def popupMSG():
    global timer
    global points
    scoreName()
    anwser = askyesno(title="Game over", message=("Wilt u opnieuw spelen?"))
    if anwser == False:
        window.destroy()
    elif anwser == True:
        highscores()
        window.config(bg="blue")
        timer = 20
        points = 0
        labelScore.config(bg="black", fg="white", text=("Time remaining: " + str(timer) + "                                                                                                         " + "Points: " + str(points)), font=("arial", 12))
        startButton = tk.Button()
        startButton.config(text="Click here to start", command=partial(startupGame, startButton))
        startButton.pack(ipadx=50, ipady=10, expand=True)


def highscores():
    global points
    global highscoresDict
    file_path = 'highscores.json'
    if points > 0:
        if os.path.exists(file_path) == False:
            with open(file_path, 'x') as file:
                print('file created')
        if os.stat(file_path).st_size == 0:
            highscoresDict = {}
            ...
            data = json.dumps(highscoresDict)
            with open(file_path, 'w') as file:
                file.write(data)
        else:
            print("File exists")



def PressedClicked(position, givenButton, self):
    global points
    points += 1
    if position <= 5:
        window.unbind(bindingList[position])
    else:
        givenButton.unbind(bindingList[position])
    givenButton.destroy()
    runGame()
    


labelScore = tk.Label()
labelScore.config(bg="black", fg="white", text=("Time remaining: " + str(timer) + "                                                                                                         " + "Points: " + str(points)), font=("arial", 12))
labelScore.pack(ipadx=10, ipady=15, fill='x')

startButton = tk.Button()
startButton.config(text="Click here to start", command=partial(startupGame, startButton))
startButton.pack(ipadx=50, ipady=10, expand=True)

window.mainloop()
