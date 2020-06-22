import pygame, gameobj

class toeEngine:

    def __init__(self):

        self.gameobjects = []
        self.uicomponents = []
        self.playerturn = True
        self.xsurface = "images/xmark.png"
        self.osurface = "images/omark.png"

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
        
        self.newgame = gameobj.gameObj("New Game")
        self.newgame.setSurface("images/newgame.png")
        self.newgame.setCoords([10, 610])

        self.uicomponents.append(self.newgame)
        

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
            return

        xy = self.boardlocations[self.__transMouse(coords)]

        #abort click event on game board if piece is already in place.
        for i in self.getGameObjects():
            if i.getCoords() == xy:
                return

        self.addGameObject(piece, xy[0], xy[1])

        self.playerturn = not self.playerturn

        self.checkVictory()

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
            return 0
        elif self.checkMoves(computermoves):
            return 1
        
        return -1

    def checkMoves(self, moves):
        #counters
        bot = 0
        mid = 0
        top = 0
        left = 0
        right = 0

        for i in moves:
            if i[0:3] == "top":
                top += 1
            elif i[0:3] == "mid":
                mid += 1
            elif i[0:3] == "bot":
                bot += 1
            
            if i[3:6] == "lef":
                left += 1
            if i[3:6] == "rig":
                right += 1
                
        if bot > 2 or top > 2 or mid > 2 or right > 2 or left > 2:
            return 1
        if "topleft" in moves and "midmid" in moves and "botright" in moves:
            return 1
        if "botleft" in moves and "midmid" in moves and "topright" in moves:
            return 1

        return 0

    def clearBoard(self):
        self.gameobjects = []
        self.playerturn = True


        
            



