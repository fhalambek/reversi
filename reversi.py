from tkinter import *
from time import sleep
from threading import Thread
from bot import easy, greedy, weighted
from os import replace, name
from _tkinter import TclError

pilImported = False

if(name == "posix"):
    error = (ImportError,)
elif(name == "nt"):
    error = (ModuleNotFoundError, ImportError)


try:
    from PIL import Image, ImageTk
    pilImported = True
except error:
    try:
        try:
            import pip
        except error:
            print("pip and Pillow libraries are not installed. Install one of them to view transitions.\n" +
                  "Linux:   sudo apt-get install python3-pip\n         pip install Pillow\n" +
                  "Windows: pip is installed, find it among installation files - Python/Python36-32/Scripts/")
            raise ImportError
        def install(package):
            pip.main(['install', package])
        install("Pillow")
        from PIL import Image, ImageTk
        pilImported = True
    except(PermissionError):
        print("PIL not installed. Try running as administrator to view transitions.")
        pilImported = False
    except error:
        print()
        pilImported = False

MARGIN_X = 10
MARGIN_Y = 10
WINDOW_DIMS = "1000x500"
WINDOW_BG = ["#00BB00", "#44FF44"]
CELL_BG = "#228822"
CELL_BG_HIGHLIGHT = "#44CC44"
CELL_SIZE = 56
DIRECTIONS = [((i//3)-1, (i%3)-1) for i in range(9)]
PLAYERS = [None, "black", "white"]
BOTS = [easy, greedy, weighted]
LANGUAGES = ("hrvatski", "English")
OPTION_BUTTON_WIDTH = 125
OPTION_BUTTON_HEIGHT = 50

blockInOut = (False, False) #program input i output
co = False #cells input
ci = False #cells output
botSpeed = .5
animationSpeed = .01
animationsEnabled = True
stopBot = True
pause = False

class Game(Frame):
    def __init__(self):
        Frame.__init__(self)
        global IMAGES, backImage, DISKS
        IMAGES = (PhotoImage(), PhotoImage(file = "res/drawables/disks/black74.png"), PhotoImage(file = "res/drawables/disks/white74.png"))
        DISKS = []
        for i in range(9):
            DISKS.append([PhotoImage(file = "res/drawables/disks/black" + str(j) + str(i) + ".png") for j in range(7)])
        DISKS.append([PhotoImage(file = "res/drawables/disks/white" + str(i) + "4.png") for i in range(7)])
        backImage = PhotoImage(file = "res/drawables/back.png")
        self.master.title("Reversi")
        self.master.resizable(False, False)
        self.master.geometry(WINDOW_DIMS)
        SettingsView.loadSettings()
        Game.loadStrings() #maknuti kasnije
        self.halves = [None, ImageView(self, position = 1, color = WINDOW_BG[0], hierarchy = (0, 0)), MenuView(master = self, position = 2, color = WINDOW_BG[1], hierarchy = (1, 0)), None]
        self.pack(expand = YES, fill = BOTH)
        self.master.protocol("WM_DELETE_WINDOW", lambda: closeWindow(self.master))
    def switch(self, target, reverse, position):
        global stopBot, pause
        pause = False
        stopBot = True
        cBlock()
        if(blockInOut[0] or blockInOut[1]): return
        block(o = False)
        self.halves[3 - reverse * 3] = HIERARCHY[target[0]][target[1]][0](master = self, position = 3 - reverse * 3, color = WINDOW_BG[target[0]%2], hierarchy = target)
        runnables = [self.frameSwapAnimationRight, self.frameSwapAnimation]
        runnables[position + reverse > 1](reverse)
    def frameSwapAnimation(self, reverse):
        def postProcessing(self, reverse):
            flag = None
            for i, j in enumerate(self.halves):
                if(j):
                    again = j.replace(i + (reverse*2 - 1))
                    if(again[0]): flag = again[1]
            del self.halves[self.halves.index(None)]
            self.halves[-reverse].destroy()
            self.halves[-reverse] = None
            self.halves.insert(3 - 3*reverse, None)
            block(0, 0)
            if(flag and reverse):
                self.switch(HIERARCHY[HIERARCHY[flag[0]][flag[1]][2][0]][HIERARCHY[flag[0]][flag[1]][2][1]][2], reverse, 2)
            elif(flag):
                self.switch((flag[0] + 1, flag[1]), 0, 2)
        if(pilImported):
            transition = TransitionImage(master = self,
                                         position = 2 - reverse,
                                         transparent = False,
                                         hierarchy = self.halves[3*(1-reverse)].myHierarchy)
            self.after(10, self.halves[2-reverse].move, 0, transition, postProcessing, self, reverse)
        else:
            postProcessing(self, reverse)
    def frameSwapAnimationRight(self, reverse):
        def postProcessing(self, reverse):
            again = self.halves[3].replace(2)
            self.halves[2].destroy()
            del self.halves[2]
            self.halves.append(None)
            if(again[0]): self.switch((again[1][0] + 1, again[1][1]), 0, 2)
            block(0, 0)
        if(pilImported):
            transition = TransitionImage(master = self,
                                         position = 2,
                                         transparent = True,
                                         hierarchy = self.halves[3].myHierarchy,
                                         hierarchy2 = self.halves[2].myHierarchy)
            self.after(10, transition.setAlpha, 0, postProcessing, self, reverse)
        else:
            postProcessing(self, reverse)
    def loadStrings():
        if(language == "eng"):
            Game.initializeStrings()
            return
        file = open("res/strings/" + language + ".txt", "r", encoding = "cp1250")
        lines = file.readlines()
        global stringsDict
        for line in lines:
            key, value = tuple(line.split(":"))  #maknuti ovaj repr ako nam ne treba
            stringsDict[key] = value[:-1]
        file.close()
        
    def initializeStrings():
        global stringsDict, selectBotText, mainMenuButtonText, modeMenuButtonText, botMenuButtonText
        stringsDict = {"Stats":"Stats",
                       "Wins by player":"Wins by player",
                       "Wins by color":"Wins by color",
                       "Disks":"Disks",
                       "Main Menu":"Main Menu",
                       "Play":"Play",
                       "Mode":"Mode",
                       "Rules":"Rules",
                       "Settings":"Settings",
                       "About":"About",
                       "Bot VS Bot":"Bot VS Bot",
                       "Human VS Bot":"Human VS Bot",
                       "Human VS Human":"Human VS Human",
                       "Easy":"Easy",
                       "Medium":"Medium",
                       "Hard":"Hard",
                       "Select bot 1":"Select bot 1",
                       "Select bot 2":"Select bot 2",
                       "Language":"Language",
                       "Bot speed":"Bot speed",
                       "Animations":"Animations",
                       "On":"On",
                       "Off":"Off",
                       "Pause":"Pause",
                       "Resume":"Resume"}
        selectBotText = ("Select bot 1", "Select bot 2")
        mainMenuButtonText = ("Play", "Rules", "Settings", "About")
        modeMenuButtonText = ("Bot VS Bot", "Human VS Bot", "Human VS Human")
        botMenuButtonText = ("Easy", "Medium", "Hard")

class TransitionImage(Button):
    def __init__(self, master, position, transparent, hierarchy, hierarchy2 = None):
        Label.__init__(self, master, image = IMAGES[0], width = 500, height = 500, bd = 0, highlightthickness = 0, bg = WINDOW_BG[hierarchy[0]%2])
        self.transparent = transparent
        if(transparent):
            self.lastImage = Image.open("res/drawables/ss/pic"+str(hierarchy2[0])+str(hierarchy2[1])+".png")
        self.rawImage = Image.open("res/drawables/ss/pic"+str(hierarchy[0])+str(hierarchy[1])+".png")
        self.sourceImage = self.rawImage.copy()
        self.rawImage.close()
        self.place(x = 500*(position - 1), y = 0)
    def setAlpha(self, frameNumber, postProcess, master, reverse):
        if(frameNumber > 50):
            self.destroy()
            postProcess(master, reverse)
            return
        if(self.transparent):
            self.frameImage = ImageTk.PhotoImage(Image.blend(self.lastImage, self.sourceImage, frameNumber*1/50))
        else:
            self.sourceImage.putalpha(frameNumber * 5)
            self.frameImage = ImageTk.PhotoImage(self.sourceImage)
        self.config(image = self.frameImage)
        master.after(10, self.setAlpha, frameNumber + 1, postProcess, master, reverse)
     
class Half(Frame):
    def __init__(self, master, position, color, hierarchy):
        Frame.__init__(self, master, bg = color, padx = MARGIN_X, pady = MARGIN_Y)
        self.place(x = (position-1) * 500, y = 0, width = 500, height = 500)
        self.myHierarchy = hierarchy
        self.myColor = color
        self.myPosition = position
    def replace(self, newPosition):
        self.place(x = (newPosition - 1) * 500)
        self.myPosition = newPosition
        return (0,)
    def move(self, frameNumber, t, pp, master, reverse):
        if(frameNumber > 50):
            t.setAlpha(0, pp, master, reverse)
            return
        self.place(x = 500*(1 - reverse) + (2*reverse - 1)*frameNumber*10, y = 0)
        self.lift(t)
        master.after(10, self.move, frameNumber + 1, t, pp, master, reverse)

class ImageView(Half):
    def __init__(self, master, position, color, hierarchy):
        Half.__init__(self, master, position, color, hierarchy)

class TextView(Half):
    def __init__(self, master, position, color, hierarchy):
        Half.__init__(self, master, position, color, hierarchy)
        self.actionBar = ActionBar(self, HIERARCHY[hierarchy[0]][hierarchy[1]][2], color)
        file = open("res/strings/"+HIERARCHY[hierarchy[0]][hierarchy[1]][1] + "_" + language + ".txt", "r", encoding = "cp1250")
        text = ""
        for line in file.readlines():
            text += line
        self.textMsg = Message(self, text = text, bg = color, justify = CENTER, anchor = CENTER)
        self.textMsg.pack()
        file.close()

class SettingsView(Half):
    def __init__(self, master, position, color, hierarchy):
        Half.__init__(self, master, position, color, hierarchy)
        self.actionBar = ActionBar(self, HIERARCHY[hierarchy[0]][hierarchy[1]][2], color) 
        self.languageLabel = Label(self, text = stringsDict["Language"], bg = color, highlightthickness = 0)
        self.languageLabel.pack()
        var = StringVar()
        var.set(language)
        self.languageOM = OptionMenu(self, var, *LANGUAGES, command = self.omCommand)
        self.languageOM.config(bg = color, highlightthickness = 0)
        self.languageOM.pack()
        self.botSpeedLabel = Label(self, text = stringsDict["Bot speed"], bg = color, highlightthickness = 0)
        self.botSpeedLabel.pack()
        self.botSpeedScale = Scale(self, from_ = 1,
                                   to = 100,
                                   orient = HORIZONTAL,
                                   command = SettingsView.sCommand,
                                   length = OPTION_BUTTON_WIDTH,
                                   bg = color,
                                   troughcolor = WINDOW_BG[1],
                                   highlightthickness = 0,
                                   cursor = "hand2")
        self.botSpeedScale.set((1-botSpeed)*100)
        self.botSpeedScale.pack()
        self.animationsLabel = Label(self, text = stringsDict["Animations"], bg = color, highlightthickness = 0)
        self.animationsLabel.pack()
        v = IntVar()
        v.set(animationsEnabled)
        self.rb = []
        for i, j in enumerate(("Off", "On")):
            self.rb.append(Radiobutton(self,
                                       text = stringsDict[j],
                                       variable = v,
                                       value = i,
                                       command = lambda: SettingsView.rbCommand(v.get()),
                                       indicatoron = 0,
                                       bg = color,
                                       selectcolor = WINDOW_BG[1]))
            self.rb[i].pack()
    def rbCommand(var):
        global animationsEnabled
        animationsEnabled = var
        SettingsView.saveSettings()
    def sCommand(var):
        global botSpeed
        botSpeed = 1-(int(var)/100)
        SettingsView.saveSettings()
    def refreshLanguage(self):
        self.actionBar.refreshLanguage()
        for i, j in zip(("Language", "Bot speed", "Animations", "Off", "On"), (self.languageLabel, self.botSpeedLabel, self.animationsLabel, self.rb[0], self.rb[1])):
            j.config(text = stringsDict[i])
    def omCommand(self, var):
        global language
        language = var[:3].lower()
        Game.loadStrings()
        for i in self.master.halves:
            if i: i.refreshLanguage()
        SettingsView.saveSettings()
    def loadSettings():
        file = open("Preferences/Settings.txt", "r")
        global language, botSpeed, animationsEnabled
        for i in file.readlines():
            key, value = tuple(i.split(":"))
            if(key == "language"):
                language = value[:-1]
            elif(key == "botSpeed"):
                botSpeed = float(value[:-1])
            elif(key == "animations"):
                animationsEnabled = ("On" in value)
        file.close()
        return
    def saveSettings():
        option = "Off\n"
        if(animationsEnabled):
            option = "On\n"
        text = "language:" + language + "\nbotSpeed:" + str(botSpeed) + "\nanimations:" + option
        file = open("Preferences/SettingsTemp.txt","w")
        file.write(text)
        file.close()
        replace("Preferences/SettingsTemp.txt", "Preferences/Settings.txt")
        return
        

    
class MenuView(Half):
    def __init__(self, master, position, color, hierarchy):
        Half.__init__(self, master, position, color, hierarchy)
        self.actionBar = ActionBar(self, HIERARCHY[hierarchy[0]][hierarchy[1]][2], color)
        self.optionButtons = []
        for i in range(len(HIERARCHY[hierarchy[0]][hierarchy[1]][-1])):
            self.optionButtons.append(Button(self, text = stringsDict[HIERARCHY[hierarchy[0]][hierarchy[1]][-1][i]], highlightthickness = 0))
            self.optionButtons[i].targetFrame = HIERARCHY[hierarchy[0]][hierarchy[1]][3][i]
            self.optionButtons[i].bind("<Button-1>", self.buttonClick)
            self.optionButtons[i].place(x = (500 - 2*MARGIN_X) // 2, y = int((i+1)*(500 - 2*MARGIN_Y)/(len(HIERARCHY[hierarchy[0]][hierarchy[1]][-1])+1)), width = OPTION_BUTTON_WIDTH, height = OPTION_BUTTON_HEIGHT, anchor = CENTER)
    def replace(self, newPosition):
        super(MenuView, self).replace(newPosition)
        self.actionBar.enableButton(not(newPosition - 1), 0)
        return (0,)
    def buttonClick(self, event):
        if(blockInOut[0] or blockInOut[1]):
            return
        if(self.myHierarchy[0] < 3):
            PM.bots = [None, 8, 8]
        for i, j in enumerate(botMenuButtonText):
            if(event.widget.cget("text") == stringsDict[j]):
                PM.bots[-1] = 8
                PM.bots[selectBotText.index(HIERARCHY[self.myHierarchy[0]][self.myHierarchy[1]][1]) + 1] = i
        self.master.switch(event.widget.targetFrame, 0, self.myPosition)
    def refreshLanguage(self):
        self.actionBar.refreshLanguage()
        for i in range(len(self.optionButtons)):
            self.optionButtons[i].config(text = stringsDict[HIERARCHY[self.myHierarchy[0]][self.myHierarchy[1]][-1][i]])

class GameView(Half):
    stats = None
    def __init__(self, master, position, color, hierarchy):
        Half.__init__(self, master, position, color, hierarchy)
        global table, winCount
        table = []
        winCount = [[0, 0, 0], [0, 0, 0]]
        for i in range(8):
            table.append([])
            for j in range(8):
                table[i].append(Cell(self, (i, j), 0))
    def replace(self, newPosition):
        super(GameView, self).replace(newPosition)
        if(newPosition == 2):
            global stopBot
            resetBoard()
            stopBot = False
            PM.startGame() #srediti da se ovo pokrece tek nakon sto se postavi view
        return (0,)
    def setStats(stats):
        GameView.stats = stats

class StatsView(Half):
    def __init__(self, master, position, color, hierarchy):
        Half.__init__(self, master, position, color, hierarchy)
        self.actionBar = ActionBar(self, HIERARCHY[hierarchy[0]][hierarchy[1]][2], color)
        self.turnFrame = Frame(self, bg = color)
        self.labels = [None, TurnLabel(self.turnFrame, 1), TurnLabel(self.turnFrame, -1)]
        self.turnFrame.pack(side = TOP, expand = YES, fill = X)
        self.charts = [ChartFrame(self, i, color) for i in (0, 1, 2)]
        self.pauseButton = Button(self, text = stringsDict["Pause"], command = self.pause, highlightthickness = 0)
        self.pauseButton.place(x = 240, y = 120, anchor = CENTER)
        GameView.setStats(self)
    def pause(self):
        global pause
        pause = not(pause)
        text = ("Pause", "Resume")
        self.pauseButton.config(text = stringsDict[text[pause]])
    def upDate(self):
        if(blockInOut[1]):
            return
        try:
            for i in (1, -1): self.labels[i].upDate()
            for i in self.charts: i.upDate()
        except(TclError, RuntimeError):
            return
    def replace(self, newPosition):
        super(StatsView, self).replace(newPosition)
        self.actionBar.enableButton(not(newPosition - 1), 0)
        return (newPosition == 2, self.myHierarchy)

Game.initializeStrings()
HIERARCHY = (((ImageView, "", (0, 0), (1, 0)),),
             ((MenuView, "Main Menu", (0, 0), ((2, 0), (2, 1), (2, 2), (2, 3)), mainMenuButtonText),),
             ((MenuView, "Mode", (1, 0), ((3, 0), (3, 1), (3, 2)), modeMenuButtonText), (TextView, "Rules", (1, 0)), (SettingsView, "Settings", (1, 0)), (TextView, "About", (1, 0))),
             ((MenuView, "Select bot 1", (2, 0), ((4, 0),)*4, botMenuButtonText), (MenuView, "Select bot 1", (2, 0), ((4, 1),)*4, botMenuButtonText), (StatsView, "Stats", (2, 0), (4, 2))),
             ((MenuView, "Select bot 2", (3, 0), ((5, 0),)*4, botMenuButtonText), (StatsView, "Stats", (3, 1), (5, 1)), (GameView, "Human VS Human", (3, 2))),
             ((StatsView, "Stats", (4, 0), (6, 0)), (GameView, "Human VS Bot", (4, 1))),
             ((GameView, "Bot VS Bot", (5, 0)),))

class PM(object):
    player = 1
    bots = [None, 8, 8]
    bot = 8
    seatChanged = 1
    def switchPlayer(newPlayer):
        PM.player = newPlayer
        PM.bot = PM.bots[newPlayer*PM.seatChanged]
    def startGame():
        if(PM.bots != [None, 8, 8]):
            myThread = Thread(target = PM.runnable)
            myThread.start()
    def runnable():
        while(not(blockInOut[1] or stopBot)):
            if(botSpeed or animationsEnabled):
                sleep(botSpeed + animationsEnabled/200)
            if(blockInOut[0] or ci or pause):
                continue
            if(PM.bot != 8 and not(blockInOut[1]) and len(Cell.availableCoordinates[PM.player])): #kompleksnost len je O(1), pa se mogu razbacivati ovako njome
                x, y = BOTS[PM.bot](table, Cell.availableCoordinates[PM.player], PM.player, -PM.player)
                cellPress(x, y)
    def changeSeats():
        PM.seatChanged *= -1

class Cell(Button):
    availableCoordinates = [[],[],[]]
    def __init__(self, master, coordinates, fill):
        Button.__init__(self,
                        master = master,
                        image = IMAGES[fill],
                        width = CELL_SIZE,
                        height = CELL_SIZE,
                        bg = CELL_BG, bd = 1,
                        highlightthickness = name == "nt")
        self.bind("<Button>", cellPress)
        self.coordinates = coordinates
        self.reset()
        self.grid(row = coordinates[0], column = coordinates[1])
        
    def switch(self, fill):
        self.fill = fill
        try:
            self.config(image = IMAGES[fill])
        except(TclError, RuntimeError):
            return

    def reset(self):
        self.availableCoordinates = [[],[],[]] #ovo mozda i ne treba, dosta memorije uzima - tu je za svaki slucaj
        self.lenAC = [[0] * 9, [0] * 9, [0] * 9]
        if(self.coordinates == (3, 3) or self.coordinates == (4, 4)):
            self.switch(-1)
        elif(self.coordinates == (3, 4) or self.coordinates == (4, 3)):
            self.switch(1)
        else:
            self.switch(0)
        
def p(x, y):
    if (x >= 0 and y >= 0 and x < 8 and y < 8):
        return True
    return False
def block(i = True, o = True):
    global blockInOut
    blockInOut = (i, o)
def cBlock(i = True, o = True):
    global ci, co
    ci = i
    co = o
def closeWindow(window):
    cBlock()
    block()
    for i in range(25):
        window.attributes("-alpha", 1-i/25)
        sleep(.03)
    window.destroy()

def getAvailableCoordinates(): #totalno neoptimizirana funkcija, ali zanemarivo - slobodno optimiziraj ako ti se da xD
    Cell.availableCoordinates = [[],[],[]] #resetiraj matricu u kojoj su spremljena ona highlightana polja
    for i in range(8):
        for j in range(8): #za svako polje u tablici
            table[i][j].availableCoordinates = [[],[],[]] #resetiraj polja koja pritisak na to polje mijenja
            table[i][j].lenAC = [[0] * 9, [0] * 9, [0] * 9] #resetiraj duljine po smjerovima
            if(table[i][j].fill == 0): #ako je polje prazno
                for r, s in DIRECTIONS: #za svaki smjer
                    if p(i + r, j + s) and table[i + r][j + s].fill: #ako nije preko ruba to polje i nije prazno
                        for k in (-1, 1): #za obije boje
                            temp = len(table[i][j].availableCoordinates[k]) #duljina trenutne liste s poljima koja ce se obojati pritiskom na trenutno polje
                            table[i][j].availableCoordinates[k] += getCellsToColor((r, s), (i, j), k) #ubaci u tu listu polja koja ce se obojati za ovo polje, ovaj smjer i ovu boju
                            table[i][j].lenAC[k][DIRECTIONS.index((r, s))] = len(table[i][j].availableCoordinates[k]) - temp #broj polja u ovom smjeru
                            if(len(table[i][j].availableCoordinates[k]) > 0 and not((i, j) in Cell.availableCoordinates[k])): #ako postoji nesto sto ce se obojati pritiskom na ovo polje
                                Cell.availableCoordinates[k].append((i, j)) #dodaj polje u listu polja za highlightanje
                                
def markAvailableCoordinates(mark = True): #oznacava polja na koja se moze stati
    if mark:  #mark znaci oznacujemo li nove ili oDznacujemo stare
        bgd = CELL_BG_HIGHLIGHT
    else:
        bgd = CELL_BG
    if(botSpeed < 0.125 and PM.bot != 8): return
    try:
        for i in Cell.availableCoordinates[PM.player]:
            table[i[0]][i[1]].config(bg = bgd)
        if not(mark):
            for i in Cell.availableCoordinates[-PM.player]:
                table[i[0]][i[1]].config(bg = bgd)
    except(TclError, RuntimeError):
        return

def resetBoard(): #prije pocetka svake partije resetira/postavlja plocu
    def createDisksAnimation():
        cBlock(o = False)
        try:
            createDisks(((3, 3, -1), (4, 4, -1), (3, 4, 1), (4, 3, 1)))
            getAvailableCoordinates()
            markAvailableCoordinates()
            GameView.stats.upDate()
        except(TclError, RuntimeError):
            return
        cBlock(False, False)
    PM.changeSeats()
    PM.switchPlayer(1)
    for i in range(8):
        for j in range(8):
            table[i][j].reset()
    if(animationsEnabled):
        cdaThread = Thread(target = createDisksAnimation)
        cdaThread.start()
    else:
        createDisksAnimation()
    
def getScore():
    l = [0, 0, 0]
    for i in range(8):
        for j in range(8):
            l[table[i][j].fill] += 1
    return l

def getFrame(fn, p, d):
    if(fn == 7):
        return IMAGES[p]
    else:
        if(d == 4 and (p == -1 or p == 2)):
            return DISKS[-1][fn]
        return DISKS[(d-4)*p+4][(fn-3)*p+3]

def gameOver():
    global winCount
    score = getScore()
    if(score[-1] > score[1]):
        winColor = -1
    elif(score[1] > score[-1]):
        winColor = 1
    else:
        winColor = 0
    winCount[0][winColor] += 1
    winCount[1][winColor * PM.seatChanged] += 1
    resetBoard()

def cellPress(event, y = 8):
    if(y == 8):
        coordinates = event.widget.coordinates #necemo se zafrkavat s getterima i setterima
    else: coordinates = event, y
    if(coordinates in Cell.availableCoordinates[PM.player] and not(blockInOut[0] or blockInOut[1] or (y == 8 and PM.bot != 8) or ci or co)):
        cBlock(o = False)
        markAvailableCoordinates(False)
        if(animationsEnabled):
            cellAnimationThread = Thread(target = cellAnimation, args = (coordinates,
                                                                         table[coordinates[0]][coordinates[1]].availableCoordinates[PM.player],
                                                                         table[coordinates[0]][coordinates[1]].lenAC[PM.player]))
            cellAnimationThread.start()
        else:
            table[coordinates[0]][coordinates[1]].switch(PM.player)
            for i in range(max(table[coordinates[0]][coordinates[1]].lenAC[PM.player])):
                for j in range(9):
                    if(i < table[coordinates[0]][coordinates[1]].lenAC[PM.player][j] and not(blockInOut[1] or co)):
                        temp = [coordinates[k] + DIRECTIONS[j][k]*(i+1) for k in (0, 1)]
                        table[temp[0]][temp[1]].switch(PM.player)
            PM.switchPlayer(-PM.player) #da, ovaj isti kod je u cellAnimation funkciji, ali 10 redaka vise = >10% rada CPUa manje
            getAvailableCoordinates()
            markAvailableCoordinates()
            GameView.stats.upDate()
            if(not(len(Cell.availableCoordinates[PM.player]) or len(Cell.availableCoordinates[-PM.player]))):
                gameOver()
                return
            elif(not(len(Cell.availableCoordinates[PM.player]))):
                PM.switchPlayer(-PM.player)
                markAvailableCoordinates()
            cBlock(False, False)
        
def createDisks(diskInfo):
    if(animationsEnabled):
        for i in range(len(DISKS[0])):
            for j in diskInfo:
                if(not(blockInOut[1] or co)):
                    table[j[0]][j[1]].config(image = getFrame(fn = i, p = j[2], d = 4))
            sleep(animationSpeed)
            if(blockInOut[1] or co): return
    for i in diskInfo:
        table[i[0]][i[1]].switch(i[2])

def cellAnimation(coordinates, cellsToColor, directionLengths):
    createDisks(((*coordinates, PM.player),))
    for i in range(max(directionLengths)):
        for frameNumber in range(len(DISKS[0])+1):
            for j in range(9):
                if(i < directionLengths[j] and not(blockInOut[1] or co)):
                    temp = [coordinates[k] + DIRECTIONS[j][k]*(i+1) for k in (0, 1)]
                    try:
                        table[temp[0]][temp[1]].config(image = getFrame(fn = frameNumber, p = PM.player, d = j))
                    except(TclError, RuntimeError):
                        return
                    if(frameNumber == 7):
                       table[temp[0]][temp[1]].fill = PM.player 
            sleep(animationSpeed)
    PM.switchPlayer(-PM.player)
    getAvailableCoordinates()
    markAvailableCoordinates()
    GameView.stats.upDate()
    if(not(len(Cell.availableCoordinates[PM.player]) or len(Cell.availableCoordinates[-PM.player]))):
        gameOver()
        return
    elif(not(len(Cell.availableCoordinates[PM.player]))):
        PM.switchPlayer(-PM.player)
        markAvailableCoordinates()
    cBlock(False, False)

def getCellsToColor(direction, coordinates, fill):
    if(direction == (0, 0)):
        return 0
    cR, cC = coordinates[0] + direction[0], coordinates[1] + direction[1]
    c = []
    while (p(cR, cC) and table[cR][cC].fill == fill * -1):
        c.append((cR, cC,))
        cR += direction[0]
        cC += direction[1]
    if(p(cR, cC) and table[cR][cC].fill):
        return c
    return []


class ActionBar(Frame):
    def __init__(self, master, targetFrame, color):
        Frame.__init__(self, master)
        self.config(bg = color)
        self.backButton = Label(self, bg = color, image = backImage, highlightthickness = 0, relief = FLAT, bd = 0)
        self.backButton.bind("<Button-1>", lambda f: self.master.master.switch(targetFrame, 1, self.master.myPosition))
        self.nameLabel = Label(self, text = stringsDict[HIERARCHY[self.master.myHierarchy[0]][self.master.myHierarchy[1]][1]], bg = color)
        self.nameLabel.pack(side = TOP, expand = NO, fill = Y)
        self.place(x = 0, y = 0, width = 480, height = 480)
        self.myColor = color
        self.backEnabled = False
        if(pilImported):
            self.rawImage = Image.open("res/drawables/back" + str(WINDOW_BG.index(color)) + ".png")
            self.sourceImage = self.rawImage.copy()
            self.rawImage.close()
    def enableButton(self, enabled, frameNumber):
        if(pilImported and (enabled != self.backEnabled)):
            if(frameNumber > 25):
                self.backEnabled = enabled
                if(not(enabled)):
                    self.backButton.place_forget()
                return
            self.sourceImage.putalpha((25*(1-enabled) + (2*enabled-1)*frameNumber)*10)
            self.im = ImageTk.PhotoImage(self.sourceImage)
            self.backButton.config(image = self.im)
            if(frameNumber == 0):
                self.backButton.place(x = 0, y = 0, height = 48, width = 48)
            self.after(10, self.enableButton, enabled, frameNumber+1)
        else:
            if(enabled):
                self.backButton.place(x = 0, y = 0)
            else:
                self.backButton.place_forget()
    def refreshLanguage(self):
        self.nameLabel.config(text = stringsDict[HIERARCHY[self.master.myHierarchy[0]][self.master.myHierarchy[1]][1]])

class TurnLabel(Label):
    def __init__(self, master, color):
        Label.__init__(self, master, bg = PLAYERS[color], image = IMAGES[0],
                       width = 50, height = 50, highlightcolor = PLAYERS[color], highlightbackground = PLAYERS[color])
        if (color > 0):
            self.pack(side = LEFT)
        else:
            self.pack(side = RIGHT)
        self.myColor = color
    def upDate(self):
        if(co or blockInOut[1]):
            return
        if(self.myColor == PM.player):
            self.config(highlightthickness = 5)
            self.pack(padx = 5, pady = 5)
        else:
            self.config(highlightthickness = 0)
            self.pack(padx = 10, pady = 10)

class ChartFrame(Frame):
    chartNames = ["Disks", "Wins by color", "Wins by player"]
    def __init__(self, master, order, color):
        Frame.__init__(self, master, bg = color)
        self.chartName = Label(self, text = stringsDict[ChartFrame.chartNames[order]], bg = color, highlightthickness = 0)
        self.chart = Frame(self, height = 50, bg = "white")
        self.blackLabel = Label(self.chart, bg = "black", bd = 0, highlightthickness = 0, height = 50, width = 0, image = IMAGES[0])
        self.blackLabel.pack(side = LEFT, fill = Y)
        self.chartName.pack(side = TOP, fill = X, anchor = W)
        self.chart.pack(side = TOP, fill = X)
        self.pack(side = TOP, fill = X)
        self.order = order
    def upDate(self):
        if (not(self.order)):
            score = getScore()
        else:
            score = winCount[self.order - 1]
        try:
            self.blackLabel.config(width = int((500 - 2*MARGIN_X)*score[1]/(score[-1]+score[1])), bg = "black")
        except(ZeroDivisionError):
            self.blackLabel.config(width = 0, bg = "white")

Game().mainloop()
'''

        print()
        print(table[event.widget.grid_info()["row"]][event.widget.grid_info()["column"]].availableCoordinates[player])
        print(table[event.widget.grid_info()["row"]][event.widget.grid_info()["column"]].lenAC[player])
if __name__ == "__main__":
    root = 
    Game()
    root.mainloop()
dok drzis polje ono se mrvicu smanji
kad pustis pretvori se u tvoju boju, a onda se ostala polja mijenjaju sirenje boje
    
'''
#koristim None, 1 i -1 radi jednostavnosti - da manje bugova ima
