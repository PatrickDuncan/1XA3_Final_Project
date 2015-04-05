from graphics import *
from random import randrange
from time import sleep

dimension = eval(input("Enter maze size (1-15): "))
while True:
    if dimension < 1 or dimension > 15:
        dimension = eval(input("Enter maze size (1-15): "))
    else: break
    
class Maze():
    def __init__(self,N):
        self.N=N
        self.north=self.south=self.east=self.west=[]
        self.been=[[1,1]]
        self.end = []
        self.explored = [[1,1]]
        self.search=[]
        #A key at the entrance is quite boring
        self.key=[1,1]
        while self.key == [1,1]:
            self.key=[randrange(1,N+1), randrange(1,N+1)]
        self.keyFound=False
        
    def main(self):
        N=self.N
        self.createGrids()
        self.end = self.knockDown([[1,1]],[1,1])
        keyPath = self.Explore(1, 1)
        keyPath = self.fixPath(keyPath)
        self.explored = [[self.key[0],self.key[1]]]
        self.search=[]
        exitPath = self.Explore(self.key[0],self.key[1])
        exitPath = self.fixPath(exitPath)
        path = self.fixPath(keyPath) + self.fixPath(exitPath)
        del path[path.index(self.key)]
        print('Exit path: ', path)
        self.draw(keyPath, exitPath)
        
    def createGrids(self):
        #Need to assign separately or it'll be call by reference
        #Index of 0 and N+1 border, ie N+2 if starting at [1,1]
        self.north=[[True for i in range(self.N+2)] for j in range(self.N+2)]
        self.east=[[True for i in range(self.N+2)] for j in range(self.N+2)]
        self.south=[[True for i in range(self.N+2)] for j in range(self.N+2)]
        self.west=[[True for i in range(self.N+2)] for j in range(self.N+2)]
        
    def knockDown(self, Been, currentCell):
        if (self.N**2)==len(self.been): #If you've traveled to all spaces, bye
            return currentCell
        #If its trapped
        x=currentCell[0]
        y=currentCell[1]
        if ([x+1,y] in self.been or x+1==self.N+1) \
           and (x-1==0 or [x-1,y] in self.been) \
           and ([x,y+1] in self.been or y+1==self.N+1) \
           and (y-1==0 or [x,y-1] in self.been):
            currentCell = Been.pop()
            return self.knockDown(Been, currentCell)
        else:
            I=J=0
            direct=randrange(0,2)
            if  direct == 0:
                #1 for east, -1 for west
                I = randrange(0,2)
                if I==0: I=-1
            else:    
                #1 for north, -1 for south
                J = randrange(0,2)
                if J==0: J=-1
            if [x+I,y+J] not in self.been and 0<x+I<self.N+1 and 0<y+J<self.N+1:
                #Knock it down!
                if I==1:
                    self.east[x][y] = self.west[x+I][y] = False
                elif I==-1:
                    self.west[x][y] = self.east[x+I][y] = False
                elif J==1:
                    self.north[x][y] = self.south[x][y+J] = False
                elif J==-1:
                    self.south[x][y] = self.north[x][y+J] = False
                self.been += [[x+I,y+J]]
                Been += [[x+I,y+J]]
                return self.knockDown(Been,[x+I,y+J])
            else: 
                return self.knockDown(Been, currentCell)
        
    def draw(self, kP, eP):
        canvas = GraphWin("Maze",600,600)
        canvas.setBackground('white')
        scale = 500//self.N
        size = 550-(500-(scale*self.N))
        frame = Rectangle(Point(50,50),Point(size,size))
        frame.draw(canvas)
        #Vertical lines
        x1 = x2 = 50+scale
        y1, y2 = 50, 50+scale
        for i in range(self.N, 0, -1):
            for j in range(1, self.N):
                if self.east[j][i]:
                    line = Line(Point(x1, y1), Point(x2, y2))
                    line.draw(canvas)
                x1 += scale; x2 += scale
            x1 = x2 = 50+scale
            y1 += scale; y2 += scale
        #Horizontal lines
        y1 = y2 = 50+scale
        x1, x2 = 50, 50+scale
        for i in range(self.N, 1, -1):
            for j in range(1, self.N+1):
                if self.south[j][i]:              
                    line = Line(Point(x1, y1), Point(x2, y2))
                    line.draw(canvas)
                x1 += scale; x2 += scale
            x1, x2 = 50, 50+scale
            y1 += scale; y2 += scale
        c = scale//5 #Constant to make it smaller than the entire square.
        #Draw start
        sx1, sx2 = 50+c, (50+scale)-c
        sy1, sy2 = (size-scale)+c, size-c
        start = Rectangle(Point(sx1,sy1),Point(sx2,sy2))
        start.setFill('green')
        start.draw(canvas)
        tx, ty = sx1+((scale-2*c)/2), sy1+((scale-2*c)/2)
        startText = Text(Point(tx,ty), 'Start')
        startText.setFill('white')
        startText.draw(canvas)
        #Draw exit
        ex1 = (scale*self.end[0])+50+c-scale
        ex2 = (scale*self.end[0])+50-c
        ey1 = size-(self.end[1]*scale)+c
        ey2 = size-(self.end[1]*scale)+scale-c
        end = Rectangle(Point(ex1,ey1),Point(ex2,ey2))
        end.setFill('red')
        end.draw(canvas)
        tx, ty = ex1+((scale-2*c)/2), ey1+((scale-2*c)/2)
        startText = Text(Point(tx,ty), 'Exit')
        startText.setFill('white')
        startText.draw(canvas)
        #Draw key
        kx1 = (scale*self.key[0])+50+c-scale
        kx2 = (scale*self.key[0])+50-c
        ky1 = size-(self.key[1]*scale)+c
        ky2 = size-(self.key[1]*scale)+scale-c
        key = Rectangle(Point(kx1,ky1),Point(kx2,ky2))
        key.setFill('blue')
        key.draw(canvas)
        tx, ty = kx1+((scale-2*c)/2), ky1+((scale-2*c)/2)
        startText = Text(Point(tx,ty), 'Key')
        startText.setFill('white')
        startText.draw(canvas)
        #Key Path
        for i in range(1,len(kP)-1):
            sleep(0.05)
            x1 = (scale*kP[i][0])+50+c-scale
            x2 = (scale*kP[i][0])+50-3*c
            y1 = size-(kP[i][1]*scale)+3*c
            y2 = size-(kP[i][1]*scale)+scale-c
            key = Rectangle(Point(x1,y1),Point(x2,y2))
            key.setFill('yellow')
            key.draw(canvas)
        #Exit Path
        for i in range(1,len(eP)-1):
            sleep(0.05)
            x1 = (scale*eP[i][0])+50+3*c-scale
            x2 = (scale*eP[i][0])+50-c
            y1 = size-(eP[i][1]*scale)+c
            y2 = size-(eP[i][1]*scale)+scale-3*c
            key = Rectangle(Point(x1,y1),Point(x2,y2))
            key.setFill('green')
            key.draw(canvas)
        

    def Explore(self, x, y):
        if not self.keyFound and [x, y] == self.key:
            self.keyFound = True
            return self.explored
        if self.keyFound and [x, y] == self.end:
            return self.explored
        if not self.north[x][y] and [x,y+1] not in self.explored:
            self.explored += [[x, y+1]]
            self.search += [[x, y]]
            return self.Explore(x, y+1)
        elif not self.east[x][y] and [x+1,y] not in self.explored:
            self.explored += [[x+1, y]]
            self.search += [[x, y]]
            return self.Explore(x+1, y)
        elif not self.south[x][y] and [x,y-1] not in self.explored:
            self.explored += [[x, y-1]]
            self.search += [[x, y]]
            return self.Explore(x,y-1)
        elif not self.west[x][y] and [x-1,y] not in self.explored:
            self.explored += [[x-1, y]]
            self.search += [[x, y]]
            return self.Explore(x-1,y)
        else:
            previousCell = self.search.pop()
            x0, y0 = previousCell[0], previousCell[1]
            self.explored += [[x,y]]
            return self.Explore(x0,y0)

    def fixPath(self, path):
        i=0
        while i < len(path):
            if path[i] in path[:i]:
                index = path.index(path[i])
                path = path[:index]+path[i+1:]
                i=-1
            i+=1
        return path
            
m=Maze(dimension); m.main()





        
            
