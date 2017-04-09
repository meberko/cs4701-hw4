import numpy as np
import matplotlib.pyplot as plt
import sys

letters = ['A','B','C','D','E','F','G','H','I']
numbers = ['1','2','3','4','5','6','7','8','9']

class SudoSolver:
    def __init__(self, boardStr):
        self.board = {}
        i=j=0
        for l in letters:
            for n in numbers:
                self.board[l+n] = boardStr[9*i+(j%9)]
                j+=1
            i+=1

    def printBoard(self):
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

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print 'Usage: python driver.py <input_string>'
        sys.exit()
    if len(sys.argv[1])!=81:
        print 'Input Error: Sudoku string must be exactly 81 characters long'
        sys.exit()
    ss = SudoSolver(sys.argv[1])
    ss.printBoard()
