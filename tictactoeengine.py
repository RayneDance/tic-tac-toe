import pygame, gameobj, math, random

class toeEngine:

    def __init__(self):

        self.gameobjects = []
        self.uicomponents = []
        self.score = [0,0]
        self.playerturn = True
        self.xsurface = "images/xmark.png"
        self.osurface = "images/omark.png"
        self.gameover = False
        self.aiboard = []

        self.boardlocations = {	"topleft": [10,10],
                                "topmid": [210, 10],
                                "topright": [410, 10],
                                "midleft": [10, 210],
                                "midmid": [210, 210],
                                "midright": [410, 210],
                                "botleft": [10, 410],
                                "botmid": [210, 410],
                                "botright": [410, 410]
                                }
        self.board = gameobj.gameObj("Board")
        self.board.setSurface("images/gameboard.png")
        
        #new game button
        self.newgame = gameobj.gameObj("New Game")
        self.newgame.setSurface("images/newgame.png")
        self.newgame.setCoords([10, 610])

        self.uicomponents.append(self.newgame)

        # scoreboard

        self.scoreboard = gameobj.gameObj("Scoreboard", 200, 600)
        self.scoreboard.setSurface("images/scoreboard.png")
        self.uicomponents.append(self.scoreboard)

        self.p1score = gameobj.gameObj("P1", 210, 630)
        self.p2score = gameobj.gameObj("P2", 350, 630)
        font = pygame.font.SysFont("verdanams", 72)
        text = font.render("0", True, (0,0,0))
        self.p1score.setSurface(text)
        self.p2score.setSurface(text)
        self.uicomponents.append(self.p1score)
        self.uicomponents.append(self.p2score)

        #fill out the board the 'ai' will run on.
        for i in range(9):
            self.aiboard.append(0)

    def getBoardSurface(self):
        return self.board.getSurface()

    def getBoardRect(self):
        return self.board.getRect()

    def getUISurface(self):
        return self.getSurface()
    
    def getUIRect(self):
        return self.getSurface()

    def getUIComponents(self):
        return self.uicomponents

    def addGameObject(self, piece, x, y):
        self.gameobjects.append(gameobj.gameObj(None, x, y, piece))

        #adds names to any added pieces
        for i in self.boardlocations.items():
            if i[1] == [x, y]:
                self.gameobjects[len(self.gameobjects)-1].setName(i[0])

        if piece == 0:
            self.gameobjects[len(self.gameobjects)-1].setSurface(self.xsurface)
            self.gameobjects[len(self.gameobjects)-1].setParental(0)
        else:
            self.gameobjects[len(self.gameobjects)-1].setSurface(self.osurface)
            self.gameobjects[len(self.gameobjects)-1].setParental(1)
        return

    def getGameObjects(self):
        return self.gameobjects

    def onClick(self, coords):
        piece = 1
        if self.playerturn:
            piece = 0

        if coords[1] > 600:
            #ui click
            if coords[0] < 200:
                self.clearBoard()
                return

        if self.checkVictory() != -1:
            self.playerturn = True
            return

        xy = self.boardlocations[self.__transMouse(coords)]

        
        #abort click event on game board if piece is already in place.
        for i in self.getGameObjects():
            if i.getCoords() == xy:
                return
        self.updateAIBoard(self.__transMouse(coords))

        self.addGameObject(piece, xy[0], xy[1])

        self.playerturn = not self.playerturn
        vic = self.checkVictory()
        if vic >=0:
            self.playerturn = True
            
        #cats game
        if vic == -2:
            self.clearBoard()

    def __transMouse(self, coords):

        if coords[0] < 200:
            if coords[1] < 200:
                return "topleft"
            else:
                if coords[1] < 400:
                    return "midleft"
                else:
                    return "botleft"
        elif coords[0] < 400:
            if coords[1] < 200:
                return "topmid"
            elif coords [1] < 400:
                return "midmid"
            else:
                return "botmid"
        elif coords[1] < 200:
            return "topright"
        elif coords[1] < 400:
            return "midright"
        else:
            return "botright"

        return 0

    def checkVictory(self):
        # 0 for player
        playermoves = []
        computermoves = []
        for i in self.getGameObjects():
            if i.getParental() == 1:
                computermoves.append(i.getCoords())
            else:
                playermoves.append(i.getCoords())
        if (len(playermoves) < 3 and len(computermoves) < 3):
            return -1
        
        i = 0
        while i < len(playermoves):
            playermoves[i] = self.__transMouse(playermoves[i])
            i += 1

        i = 0
        while i < len(computermoves):
            computermoves[i] = self.__transMouse(computermoves[i])
            i += 1
        
        if self.checkMoves(playermoves):
            if not self.gameover:
                self.gameover = not self.gameover
                self.score[0] += 1
                self.updateScoreboard()
            return 0
        elif self.checkMoves(computermoves):
            if not self.gameover:
                self.gameover = not self.gameover
                self.score[1] += 1
                self.updateScoreboard()
            return 1
        
        for i in range(9):
            if self.aiboard[i] == 0:
                return -1
        
        return -2


    def checkMoves(self, moves):
        
        grid = []
        for i in range(10):
            grid.append(0)
        
        for i in moves:
            if i == "topleft":
                grid[0] = 1
            elif i == "topmid":
                grid[1] = 1
            elif i == "topright":
                grid[2] = 1
            elif i == "midleft":
                grid[3] = 1
            elif i == "midmid":
                grid[4] = 1
            elif i == "midright":
                grid[5] = 1
            elif i == "botleft":
                grid[6] = 1
            elif i == "botmid":
                grid[7] = 1
            elif i == "botright":
                grid[8] = 1

        if grid[0]:
            if grid[1] and grid[2]:
                return True
            elif grid[3] and grid[6]:
                return True
            elif grid[4] and grid[8]:
                return True
        
        if grid[4]:
            if grid[3] and grid[5]:
                return True
            elif grid[1] and grid[7]:
                return True
            elif grid[2] and grid[6]:
                return True

        if grid[6] and grid[7] and grid[8]:
            return True
        if grid[2] and grid[5] and grid [8]:
            return True

        return False

    def clearBoard(self):
        self.gameobjects = []
        self.playerturn = True
        self.gameover = not self.gameover

        for i in range(0,9):
            self.aiboard[i] = 0

    def updateScoreboard(self):
        font = pygame.font.SysFont("verdanams", 72)

        for i in self.uicomponents:
            if i.name == "P1":
                i.setSurface(font.render(str(self.score[0]), True, (0,0,0)))

            if i.name == "P2":
                i.setSurface(font.render(str(self.score[1]), True, (0,0,0)))
    
    def AIMove(self):
        gameobs = self.getGameObjects()

        ourmove = random.randint(0, 8)
        while self.aiboard[ourmove] == 1:
            ourmove = random.randint(0, 8)

        #print("AI move: "+str(ourmove))
        #self.aiboard[ourmove] = 1
        print(self.aiboard)
        print(ourmove)
        coords = [100,100]
        if ourmove < 3:
            #print("1-3")
            coords = [(ourmove+1)*151, 100]
            self.onClick(coords)
            return
        if ourmove < 6:
           # print("4-6")
            ourmove = ourmove -2
            print(ourmove*160)
            coords = [(ourmove)*160,300]
            self.onClick(coords)
            return

        if ourmove < 9:
           # print("5-9")
            ourmove = ourmove -5
            print(ourmove*152)
            coords = [(ourmove)*160,500]
            self.onClick(coords)
            return

        

    def updateAIBoard(self, move):

        if move == "topleft":
            self.aiboard[0] = 1
            print(move)
            return
        if move == "topmid":
            self.aiboard[1] = 1
            print(move)
            return
        if move == "topright":
            self.aiboard[2] = 1
            print(move)
            return
        if move == "midleft":
            self.aiboard[3] = 1
            print(move)
            return
        if move == "midmid":
            self.aiboard[4] = 1
            print(move)
            return
        if move == "midright":
            self.aiboard[5] = 1
            print(move)
            return
        if move == "botleft":
            self.aiboard[6] = 1
            print(move)
            return
        if move == "botmid":
            self.aiboard[7] = 1
            print(move)
            return
        if move == "botright":
            self.aiboard[8] = 1
            print(move)
            return
            



