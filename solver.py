# -*- coding: utf8 -*-
import sys
import math
import copy

class Board:
    def __init__(self,  gridw=3,gridh=4, grid=None):
        self.gridw = gridw
        self.gridh = gridh
        size = gridw * gridh

        self.cells_list=[]

        #Grid中のcellのList
        for x in range(size):
            self.cells_list.append(x)
        
        self.grid = grid
        self.blank = self.cell_xy(0)
        
        #ターゲット
        self.target = {}
        for x in range(size+1):
            self.target[x] = x % self.gridw, x / self.gridw

    def cell_xy(self,cell_to_find):
        '''
        cellの位置を返す
        '''
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == cell_to_find:
                    return x,y

    def heuristic(self):
        '''
        A*のヒューリスティック関数、ターゲットとのマンハッタン距離で計算
        '''
        manhattan_distance = 0
        for cell in self.cells_list:
            x,y = self.cell_xy(cell)
            manhattan_distance += math.fabs(x - self.target[cell][0]) + math.fabs(y - self.target[cell][1])
        return manhattan_distance

    
    def take_move(self, move):
        """
        移動させる
        """
        x, y = move
        e_x, e_y = self.blank

        #swap 
        temp = self.grid[y][x]
        self.grid[y][x] = 0
        self.grid[e_y][e_x] = temp

        #set blank positon
        self.blank = x, y 

    def create_moves(self):
        '''
        blankの移動できる位置のリスト
        '''
        x, y = self.blank

        up = y - 1
        down = y + 1
        left = x - 1
        right = x + 1

        moves = []
        if up > -1: moves.append((x, up))
        if down < self.gridh : moves.append((x, down))
        if left > -1: moves.append((left, y))
        if right < self.gridw : moves.append((right, y))
        return moves
    
    def print_grid(self):
        for  row in self.grid:
                print row
        #print ""

class Node:
    def __init__(self, board, move, g_score, last):
        self.board = board

        #結果のシーケンスを表示用
        self.move = move
        self.last = last

        self.g_score = g_score
        self.f_score = g_score + board.heuristic() #f(n)
    
    def create_children(self):
        nodes = []

        for move in self.board.create_moves():
            board = copy.deepcopy(self.board)
            board.take_move(move)

            nodes.append(Node(board, move, self.g_score + 1, self))
        
        return nodes


class AstarSlover:
    def get_lowest_node(self,nodeset):
        '''
        f_scoreの一番低いノードを返す
        '''
        lowest = nodeset[0].f_score
        lowest_node = nodeset[0]
        for node in nodeset:
            if lowest > node.f_score:
                lowest = node.f_score
                lowest_node = node
        return lowest_node

    def get_move_sequance(self,node):
        '''
        結果のシーケンスを表示する
        '''
        moves = []
        while node.last:
            moves.append((node.move[0]+1,node.move[1]+1))
            node = node.last
        moves.reverse()

        print("Sloved!")
        print(str(len(moves))+" Moves:"+str(moves))

    def slove(self,board):
        openset = [Node(board, None, 0, None)]
        closedset = []

        while True:
            node = self.get_lowest_node(openset)
            
            if node.board.heuristic() == 0:
                self.get_move_sequance(node)
                break
            else:
                openset.remove(node)
                for new_node in node.create_children():
                    if new_node in closedset:
                        continue
                    if new_node not in openset:
                        openset.append(new_node)
                closedset.append(node)

class Helper:
    def transtr2grid(self,inputstr):
        cells = [int(n) for n in inputstr.split(" ")]
        grid = []
        for y in xrange(4):
            row = []
            for x in xrange(3):
                row.append(cells[y*3+x])
            grid.append(row)
        return grid

def main():
    #inputstr = "1 4 2 6 0 3 7 11 5 9 8 10"
    with open(sys.argv[1]) as file:
        inputstr = file.readline()
    astar = AstarSlover()
    helper = Helper()

    grid = helper.transtr2grid(inputstr)

    board = Board(3,4,grid)
    board.print_grid()
    astar.slove(board)

if __name__ == "__main__":
    main()
