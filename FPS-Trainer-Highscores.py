import json
import os
import os.path
import tkinter as tk
from functools import partial
import random
from tkinter.messagebox import askyesno, showerror, showinfo

# window creation
window = tk.Tk()
window.geometry("1000x500")
window.resizable(False, False)
window.config(bg="blue")
window.title("FPS Trainer V1")

# global variables
timer = 20
points = 0
name = None
bindingList = ["<w>", "<a>", "<s>", "<d>", "<space>", "<Button-1>", "<Double-Button-1>", "<Triple-Button-1>"]
printTask = ["press: w", "press: a", "press: s", "press: d", "press: space", "Single click", "Double click", "Triple click", ]
file_path = 'highscores.json'
highscoresDict = None

# resposible for destroying menu and activating components  /
def startupGame(startButton):
    startButton.destroy()
    window.config(bg="gray")
    labelScore.after(1000, time)
    runGame()

# Sends chosen random number for button creation  /
def runGame():
    chosenTaskposition = random.randrange(0,8)
    createButton(chosenTaskposition)

# responsible for keeping track of time and updating the label  /
def time():
    global timer
    timer -= 1
    labelScore.config(text=("Time remaining: " + str(timer) + "                                                                                                         " + "Points: " + str(points)), font=("arial", 12))
    if timer == 0:
        window.after(2000, scoreIsHighscore)
    else:
        labelScore.after(1000, time)

# responsible for checking if score is highscore  /
def scoreIsHighscore():
    highscoresCreation()
    with open(file_path, 'r') as file:
        data = json.load(file)
        if len(data) == 0:
            print("First time!!!")
            scoreName()
        else:
            result = dictLengthCheck(data)
            if result == True:
                boolResult = dictItemDel(data)
                if boolResult == True:
                    scoreName()
                else:
                    popupMSG()
            else:
                scoreName()


# checks wether length dictionary == 10
def dictLengthCheck(dataDict):
    return True if len(dataDict) == 10 else False


# handles item deletion if dict length == 10
def dictItemDel(loadedDict):
    min_value = min(loadedDict.itervalues())
    remaining = loadedDict.viewkeys() - (k for k, v in loadedDict.iteritems() if v == min_value)
    if remaining < points:
        return False
    else:
        del loadedDict[remaining]
        with open(file_path, 'w') as file:
            encodedStr = json.dumps(loadedDict)
            file.write(encodedStr)
        return True


# creates button, binds and positions button  /
def createButton(position):
    if timer > 0:
        xCord = random.randrange(50,950)
        yCord = random.randrange(100,450)
        button = tk.Button()
        button.config(text=printTask[position])
        button.place(x=xCord,y=yCord)
        if position <= 5:
            window.bind(bindingList[position], partial(PressedClicked, position, button))
        else:
            button.bind(bindingList[position], partial(PressedClicked, position, button))

# responsible for setting name to highscore  /
def scoreName():
    global scoreLabel, entryScore, scoreButton
    parameter = False
    showinfo(title= "New highscore!!!", message= "U heeft een highscore behaald! Vul a.u.b een naam in voor de score")
    scoreLabel = tk.Label(bg='gray', text="Vul hier naam in:", font=("arial", 18))
    scoreLabel.place(x=400, y=250)
    entryScore = tk.Entry(width=20)
    entryScore.place(x=400, y=280)
    with open(file_path, 'r') as file:
        data = json.load(file)
        if len(data) == 0:
            parameter = True
    scoreButton = tk.Button(text="Invullen")
    scoreButton.bind('<Button-1>', partial(scoreButtoncheck, parameter))
    scoreButton.place(x=530, y=280)

# Checking if entry is alpha and first time add dict item  /
def scoreButtoncheck(firsttime, self):
    global scoreLabel, entryScore, scoreButton
    checkingvar = entryScore.get()
    if checkingvar.isalpha() == True:
        global name
        checkingvar = checkingvar.lower()
        name = checkingvar
        scoreLabel.destroy()
        entryScore.destroy()
        scoreButton.destroy()
        highscoresDict = {}
        if firsttime == True:
            with open(file_path, 'w') as file:
                highscoresDict[name] = points
                json.dump(highscoresDict, file)
        else:
            with open(file_path, 'r') as file:
                highscoresDict = json.load(file)
                highscoresDict[name] = points
                sortedDict = dict(sorted(highscoresDict.items(), key=lambda item: item[1]))
            with open(file_path, 'w') as file:
                json.dump(sortedDict, file)
        popupMSG()        
    else:
        showerror(title="Alleen alphabetische letters!!!", message="Alleen letters zijn toegestaan!")    

# responsible for rerunning the program and reseting values to their original state  /
def popupMSG():
    global timer, points, name
    anwser = askyesno(title="Game over", message=("Wilt u opnieuw spelen?"))
    if anwser == False:
        window.destroy()
    elif anwser == True:
        window.config(bg="blue")
        timer = 20
        points = 0
        name = None
        labelScore.config(bg="black", fg="white", text=("Time remaining: " + str(timer) + "                                                                                                         " + "Points: " + str(points)), font=("arial", 12))
        startButton = tk.Button()
        startButton.config(text="Click here to start", command=partial(startupGame, startButton))
        startButton.pack(ipadx=50, ipady=10, expand=True)

# creates file and creates dictionary in file  /
def highscoresCreation():
    global highscoresDict
    if os.path.exists(file_path) == False:
        with open(file_path, 'x') as file:
            print('file created')
    if os.stat(file_path).st_size == 0:
        highscoresDict = {}
        data = json.dumps(highscoresDict)
        with open(file_path, 'w') as file:
            file.write(data)
            print('dictionary created')
    else:
        print("File exists")


# responsible for unbinding buttons and destroying them after keybind pressed or mouse clicked  /
def PressedClicked(position, givenButton, self):
    global points, labelScore
    points += 1
    labelScore.config(bg="black", fg="white", text=("Time remaining: " + str(timer) + "                                                                                                         " + "Points: " + str(points)), font=("arial", 12))
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