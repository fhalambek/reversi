from tkinter import *
from time import sleep
from threading import Thread
from bot import easy, greedy, weighted

#NE POKRETATI IZ SHELLA - 
#NECE SE NISTA LOSE DESIT,
#AL JE PERFORMANS VISESTRUKO GORI

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
              
OPTION_BUTTON_WIDTH = 100
OPTION_BUTTON_HEIGHT = 50

statsText = "Stats"
winsByPlayerText = "Wins by player"
winsByColorText = "Wins by color"
disksText = "Disks"
mainMenuText = "Main Menu"
playText = "Play"
modeText = "Mode"
rulesText = "Rules"
settingsText = "Settings"
creditsText = "Credits"
bvbText = "Bot VS Bot"
hvbText = "Human VS Bot"
hvhText = "Human VS Human"
easyText = "Easy"
mediumText = "Medium"
hardText = "Hard"
selectBotText = ("SelectBot1", "SelectBot2")
mainMenuButtonText = (playText, rulesText, settingsText, creditsText)
modeMenuButtonText = (bvbText, hvbText, hvhText)
botMenuButtonText = (easyText, mediumText, hardText)

blockInOut = (False, False)
botSpeed = .001



class Game(Frame):
    def __init__(self):
        Frame.__init__(self)
        global IMAGES, backImage
        IMAGES = (PhotoImage(), PhotoImage(file = "black50.png"), PhotoImage(file = "white50.png"))
        backImage = PhotoImage(file = "back.png")
        self.master.title("Reversi")
        self.master.resizable(False, False)
        self.master.geometry(WINDOW_DIMS)
        self.halves = [None, ImageView(self, position = 1, color = WINDOW_BG[0], hierarchy = (0, 0)), MenuView(master = self, position = 2, color = WINDOW_BG[1], hierarchy = (1, 0)), None]
        self.pack(expand = YES, fill = BOTH)
        self.master.protocol("WM_DELETE_WINDOW", lambda: closeWindow(self.master))
    def switch(self, target, reverse, position):#wtf, Python? varijabilno ime klase??!
        self.halves[3 - reverse * 3] = HIERARCHY[target[0]][target[1]][0](master = self, position = 3 - reverse * 3, color = WINDOW_BG[target[0]%2], hierarchy = target)
        runnables = [self.frameSwapAnimationRight, self.frameSwapAnimation]
        thread = Thread(target = runnables[position + reverse > 1], args = (reverse,))
        block(o = 0)
        thread.start()
    def frameSwapAnimation(self, reverse):
        flag = None
        for i, j in enumerate(self.halves):
            if(j):
                again = j.replace(i + (reverse*2 - 1))
                if(again[0]): flag = again[1]
        del self.halves[self.halves.index(None)]
        self.halves[-reverse].destroy()
        self.halves[-reverse] = None
        self.halves.insert(3 - 3*reverse, None)
        if(flag and reverse):
            self.switch(HIERARCHY[HIERARCHY[flag[0]][flag[1]][2][0]][HIERARCHY[flag[0]][flag[1]][2][1]][2], reverse, 2)
        elif(flag):
            self.switch((flag[0] + 1, flag[1]), 0, 2)
        block(0, 0)
        
    def frameSwapAnimationRight(self, reverse):
        again = self.halves[3].replace(2)
        self.halves[2].destroy()
        del self.halves[2]
        self.halves.append(None)
        if(again[0]): self.switch((again[1][0] + 1, again[1][1]), 0, 2)
        block(0, 0)
            
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

class ImageView(Half):
    def __init__(self, master, position, color, hierarchy):
        Half.__init__(self, master, position, color, hierarchy)

class TextView(Half):
    def __init__(self, master, position, color, hierarchy):
        Half.__init__(self, master, position, color, hierarchy)

class SettingsView(Half):
    def __init__(self, master, position, color, hierarchy):
        Half.__init__(self, master, position, color, hierarchy)

class MenuView(Half):
    def __init__(self, master, position, color, hierarchy):
        Half.__init__(self, master, position, color, hierarchy)
        self.actionBar = ActionBar(self, HIERARCHY[hierarchy[0]][hierarchy[1]][2], color)
        self.optionButtons = []
        for i in range(len(HIERARCHY[hierarchy[0]][hierarchy[1]][-1])):
            self.optionButtons.append(Button(self, text = HIERARCHY[hierarchy[0]][hierarchy[1]][-1][i]))
            self.optionButtons[i].targetFrame = HIERARCHY[hierarchy[0]][hierarchy[1]][3][i]
            self.optionButtons[i].bind("<Button-1>", self.buttonClick)
            self.optionButtons[i].place(x = (500 - 2*MARGIN_X) // 2, y = int((i+1)*(500 - 2*MARGIN_Y)/(len(HIERARCHY[hierarchy[0]][hierarchy[1]][-1])+1)), width = OPTION_BUTTON_WIDTH, height = OPTION_BUTTON_HEIGHT, anchor = CENTER)
    def replace(self, newPosition):
        super(MenuView, self).replace(newPosition)
        self.actionBar.enableButton(not(newPosition - 1))
        return (0,)
    def buttonClick(self, event):
        if(self.myHierarchy[0] < 3):
            PM.bots = [None, 8, 8]
        if(event.widget.cget("text") in botMenuButtonText):
            PM.bots[-1] = 8
            PM.bots[selectBotText.index(HIERARCHY[self.myHierarchy[0]][self.myHierarchy[1]][1]) + 1] = botMenuButtonText.index(event.widget.cget("text"))
        self.master.switch(event.widget.targetFrame, 0, self.myPosition)     

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
        resetBoard()
        PM.startGame() #srediti da se ovo pokrece tek nakon sto se postavi view
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
        GameView.setStats(self)

    def upDate(self):
        for i in (1, -1): self.labels[i].upDate()
        for i in self.charts: i.upDate()

    def replace(self, newPosition):
        super(StatsView, self).replace(newPosition)
        self.actionBar.enableButton(not(newPosition - 1))
        return (newPosition == 2, self.myHierarchy)

HIERARCHY = (((ImageView, "", (0, 0), (1, 0)),),
             ((MenuView, mainMenuText, (0, 0), ((2, 0), (2, 1), (2, 2), (2, 3)), mainMenuButtonText),),
             ((MenuView, modeText, (1, 0), ((3, 0), (3, 1), (3, 2)), modeMenuButtonText), (TextView, rulesText, (1, 0)), (SettingsView, settingsText, (1, 0)), (TextView, creditsText, (1, 0))),
             ((MenuView, selectBotText[0], (2, 0), ((4, 0),)*4, botMenuButtonText), (MenuView, selectBotText[0], (2, 0), ((4, 1),)*4, botMenuButtonText), (StatsView, hvhText, (2, 0), (4, 2))),
             ((MenuView, selectBotText[1], (3, 0), ((5, 0),)*4, botMenuButtonText), (StatsView, hvbText, (3, 1), (5, 1)), (GameView, hvhText, (3, 2))),
             ((StatsView, bvbText, (4, 0), (6, 0)), (GameView, hvbText, (4, 1))),
             ((GameView, bvbText, (5, 0)),))

class PM(object):
    player = 1
    bots = [None, 8, 8]
    seatChanged = 1 #srediti ovo i blokirati input po potrebi
    def switchPlayer(newPlayer):
        PM.player = newPlayer
        PM.bot = PM.bots[newPlayer*PM.seatChanged]
    def startGame():
        if(PM.bots != [None, 8, 8]):
            myThread = Thread(target = PM.runnable)
            myThread.start()
    def runnable():
        while(not(blockInOut[1])):
            sleep(botSpeed)
            if(PM.bot != 8 and not(blockInOut[1])):
                x, y = BOTS[PM.bot](table, Cell.availableCoordinates[PM.player], PM.player, -PM.player)
                cellPress(x, y)
    def changeSeats():
        PM.seatChanged *= -1

class Cell(Button):
    availableCoordinates = [[],[],[]]
    def __init__(self, master, coordinates, fill):
        Button.__init__(self, master = master, image = IMAGES[fill], width = CELL_SIZE, height = CELL_SIZE, bg = CELL_BG, bd = 1, highlightthickness = 1, padx = 0, pady = 0)
        self.bind("<Button>", cellPress)
        self.coordinates = coordinates
        self.reset()
        self.grid(row = coordinates[0], column = coordinates[1])
        
    def switch(self, fill):
        self.fill = fill
        self.config(image = IMAGES[fill])

    def reset(self):
        self.availableCoordinates = [[],[],[]]
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
def closeWindow(window):
    block()
    window.destroy()

def getAvailableCoordinates():
    Cell.availableCoordinates = [[],[],[]]
    for i in range(8):
        for j in range(8):
            table[i][j].availableCoordinates = [[],[],[]]
            table[i][j].lenAC = [[0] * 9, [0] * 9, [0] * 9]
            if(table[i][j].fill == 0):
                for r, s in DIRECTIONS:
                    if p(i + r, j + s) and table[i + r][j + s].fill:
                        for k in (-1, 1):
                            temp = len(table[i][j].availableCoordinates[k])
                            table[i][j].availableCoordinates[k] += getCellsToColor((r, s), (i, j), k)
                            table[i][j].lenAC[k][DIRECTIONS.index((r, s))] = len(table[i][j].availableCoordinates[k]) - temp
                            if(len(table[i][j].availableCoordinates[k]) > 0):
                                Cell.availableCoordinates[k].append((i, j))
                                
def markAvailableCoordinates(mark = True):
    if mark:
        bgd = CELL_BG_HIGHLIGHT
    else:
        bgd = CELL_BG
    for i in Cell.availableCoordinates[PM.player]:
        table[i[0]][i[1]].config(bg = bgd)
    if not(mark):
        for i in Cell.availableCoordinates[-PM.player]:
            table[i[0]][i[1]].config(bg = bgd)

def resetBoard():
    PM.switchPlayer(1)
    PM.changeSeats()
    for i in range(8):
        for j in range(8):
            table[i][j].reset()
    getAvailableCoordinates()
    markAvailableCoordinates()
    GameView.stats.upDate()
    

def getScore():
    l = [0, 0, 0]
    for i in range(8):
        for j in range(8):
            l[table[i][j].fill] += 1
    return l

def gameOver():
    global winCount
    score = getScore()
    if(score[-1] > score[1]):
        winColor = -1
    elif(score[1] > score[-1]):
        winColor = 1
    else:
        winColor = 0
    winBot = winColor * PM.seatChanged
    winCount[0][winColor] += 1
    winCount[1][winBot] += 1
    resetBoard()

def cellPress(event, y = 8):
    if(y == 8): coordinates = event.widget.coordinates #necemo se zafrkavat s getterima i setterima
    else: coordinates = event, y
    if(coordinates in Cell.availableCoordinates[PM.player]):
        for r, s in table[coordinates[0]][coordinates[1]].availableCoordinates[PM.player]:
            table[r][s].switch(PM.player)
        table[coordinates[0]][coordinates[1]].switch(PM.player)
        markAvailableCoordinates(False)
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
        self.nameLabel = Label(self, text = statsText, bg = color)
        self.nameLabel.pack(side = TOP, expand = NO, fill = Y)
        self.pack(side = TOP, expand = NO, fill = X)
        self.myColor = color
    def enableButton(self, enabled):
        if(enabled):
            self.backButton.place(x = 0, y = 0)
        else:
            self.backButton.place_forget()

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
        if(self.myColor == PM.player):
            self.config(highlightthickness = 5)
            self.pack(padx = 5, pady = 5)
        else:
            self.config(highlightthickness = 0)
            self.pack(padx = 10, pady = 10)

class ChartFrame(Frame):
    chartNames = [disksText, winsByColorText, winsByPlayerText]
    def __init__(self, master, order, color):
        Frame.__init__(self, master, bg = color)
        self.chartName = Label(self, text = ChartFrame.chartNames[order], bg = color)
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
