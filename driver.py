import numpy as np
import matplotlib.pyplot as plt
import sys
import math
from random import shuffle

letters = ['A','B','C','D','E','F','G','H','I']
numbers = ['1','2','3','4','5','6','7','8','9']
squares = [
            ['A1','A2','A3','B1','B2','B3','C1','C2','C3'],
            ['A4','A5','A6','B4','B5','B6','C4','C5','C6'],
            ['A7','A8','A9','B7','B8','B9','C7','C8','C9'],
            ['D1','D2','D3','E1','E2','E3','F1','F2','F3'],
            ['D4','D5','D6','E4','E5','E6','F4','F5','F6'],
            ['D7','D8','D9','E7','E8','E9','F7','F8','F9'],
            ['G1','G2','G3','H1','H2','H3','I1','I2','I3'],
            ['G4','G5','G6','H4','H5','H6','I4','I5','I6'],
            ['G7','G8','G9','H7','H8','H9','I7','I8','I9']
        ]

class SudoSolver:
    def __init__(self, boardStr):
        self.dim = int(math.sqrt(len(boardStr)))
        self.sqrdim = int(math.sqrt(self.dim))
        self.board = {}
        self.doms = {}
        self.vars = []
        self.arcs = []
        i=j=0

        # Construct board
        for l in letters:
            for n in numbers:
                self.board[l+n] = int(boardStr[9*i+(j%9)])
                j+=1
            i+=1

        # Construct vars (empty spaces) and doms
        for k in self.board.keys():
            if self.board[k]==0:
                self.vars.append(k)
                self.doms[k] = range(1,10)
            else:
                self.doms[k] = [self.board[k]]

        # Construct arcs
        for xi in self.vars:
            self.AddArcs(xi)

    # AC3 Solve
    def AC3Solve(self):
        # While there are remaining arcs
        while self.arcs:
            # Pop an arc and revise
            currX = self.arcs.pop(0)
            xi = currX[0]
            xj = currX[1]
            if self.Revise(xi,xj):
                if len(self.doms[xi]) == 0:
                    return False
                self.AddArcs(xi,xj)
        return True

    def Revise(self,xi,xj):
        revised = False
        for d in self.doms[xi]:
            if self.doms[xj]==[d]:
                self.doms[xi].remove(d)
                revised=True
        return revised

    def AddArcs(self,xi,xjx=None):
        for xj in self.GetRow(xi):
            if xi!=xj and xj!=xjx:
                self.arcs.append([xi,xj])
        for xj in self.GetCol(xi):
            if xi!=xj and xj!=xjx:
                self.arcs.append([xi,xj])
        for xj in self.GetSqu(xi):
            if xi!=xj and xj!=xjx:
                self.arcs.append([xi,xj])

    # Backtrack Solve
    def BacktrackSolve(self, currGrid, row=0, col=0):
        # Get next var and check completeness
        coord = self.GetUnassignedCoord(currGrid, row, col)
        row = coord[0]
        col = coord[1]
        if row==-1:
            return True
        # Iterate through ALL possible values
        for val in range(1,10):
            if self.IsConsistent(currGrid,row,col,val):
                # Add { var = currGrid[row][col] = val }
                currGrid[row][col] = val
                result = self.BacktrackSolve(currGrid, row, col)
                if result:
                    return True
                # Remove { var = currGrid[row][col] = val }
                currGrid[row][col] = 0
        return False

    def IsConsistent(self, grid, currRow, currCol, val):
        # Check row consistency
        rowConsistent = True
        for col in range(self.dim):
            if val==grid[currRow][col]:
                rowConsistent = False
        if rowConsistent:
            # Check column consistency
            columnConsistent = True
            for row in range(self.dim):
                if val==grid[row][currCol]:
                    columnConsistent = False
            if columnConsistent:
                # Check square consistency
                sqrX = self.sqrdim*(currRow/self.sqrdim)
                sqrY = self.sqrdim*(currCol/self.sqrdim)
                for x in range(sqrX, sqrX+self.sqrdim):
                    for y in range(sqrY, sqrY+self.sqrdim):
                        if val==grid[x][y]:
                            return False
                return True
        return False

    # Getters
    def GetRow(self,idx):
        rowidx = []
        ro = idx[0]
        for n in range(0,len(numbers)):
            rowidx.append(ro+numbers[n])
        return rowidx

    def GetCol(self,idx):
        colidx = []
        co = idx[1]
        for n in range(0,len(letters)):
            colidx.append(letters[n]+co)
        return colidx

    def GetSqu(self,idx):
        for s in squares:
            if idx in s:
                return s

    def GetGrid(self, instr):
        grid = []
        for i in range(0,self.dim):
            row = []
            for j in range(0,self.dim):
                row.append(int(instr[self.dim*i+j]))
            grid.append(row)
        return grid

    def GetGridStr(self, grid):
        gridstr=''
        for i in range(0,self.dim):
            for j in range(0,self.dim):
                gridstr+=str(grid[i][j])
        return gridstr

    def GetUnassignedCoord(self, grid, currRow, currCol):
        # Iterate thru undiscovered
        for i in range(currRow,self.dim):
            for j in range(currCol,self.dim):
                if grid[i][j]==0:
                    return (i,j)
        # Iterate thru ALL
        for i in range(0,self.dim):
            for j in range(0,self.dim):
                if grid[i][j]==0:
                    return (i,j)
        return (-1,-1)

    # Utility Functions
    def PrintDomains(self):
        for k in sorted(self.doms.keys()):
            print(('%s: ')%(k))
            print self.doms[k]

    def PrintBoard(self):
        print
        print '\t',
        for n in numbers:
            print n+'\t',
        print
        print
        for l in letters:
            print l+'\t',
            for n in numbers:
                print str(self.board[l+n])+'\t',
            print

    def FillBoard(self):
        for k in sorted(self.doms.keys()):
            if len(self.doms[k])==1:
                self.board[k] = self.doms[k][0]

    def MakeString(self):
        finalString = ""
        for k in sorted(self.doms.keys()):
            finalString = finalString + str(self.board[k])
        if not '0' in finalString:
            print '********************************************\n\t\tSOLVED\t\t\n********************************************\n'
        return finalString

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print 'Usage: python driver.py <input_string>'
        sys.exit()
    if len(sys.argv[1])!=81:
        print 'Input Error: Sudoku string must be exactly 81 characters long'
        sys.exit()
    ss = SudoSolver(sys.argv[1])

    # AC3 Solution
    #ss.AC3Solve()
    #ss.FillBoard()
    #newstr = ss.MakeString()
    #if newstr!=sys.argv[1]:
    #    print newstr

    # Backtrack Solution
    grid = ss.GetGrid(sys.argv[1])
    with open('output.txt', 'a') as f:
        if ss.BacktrackSolve(grid):
            f.write(ss.GetGridStr(grid)+'\n')
        else:
            f.write('\n')
