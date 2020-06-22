import pygame
class gameObj:

    def __init__(self, name = None, x = 0, y = 0, parental = None):
        self.image = None
        self.name = name
        self.x = x
        self.y = y
        self.parental = parental

    def getName(self):
        return self.name

    def getParental(self):
        return self.parental
    
    def setParental(self, parental):
        self.parental = parental
    
    def getSurface(self):
        return self.image
    
    def setSurface(self, image):
        self.image = pygame.image.load(image)

    def getRect(self):
        return self.image.get_rect()

    def setName(self, name):
        self.name = name

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def setCoords(self, coords):
        self.x = coords[0]
        self.y = coords[1]
    
    def getCoords(self):
        coords = [self.x, self.y]
        return coords
