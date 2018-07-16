# -*- coding: utf8 -*-
import sys
import copy

class Board:
    target = {}
    gridw = 0
    gridh = 0
    size = 0
    def __init__(self, grid):
        self.grid = grid
        
    def cell_xy(self, cell_to_find):
        '''
        cellの位置を返す
        '''
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == cell_to_find:
                    return x, y

    def heuristic(self):
        '''
        A*のヒューリスティック関数、ターゲットとのマンハッタン距離で計算
        '''
        manhattan_distance = 0
        for cell in range(self.size):
            x,y = self.cell_xy(cell)
            manhattan_distance += abs(x - Board.target[cell][0]) + abs(y - Board.target[cell][1])
        return manhattan_distance
    
    def take_move(self, move):
        """
        移動させる
        """
        x, y = move
        blank_x, blank_y = self.cell_xy(0)

        #swap 
        self.grid[y][x], self.grid[blank_y][blank_x]  = 0, self.grid[y][x]

    def create_moves(self):
        '''
        blankの移動できる位置のリスト
        '''
        #blankの現在位置
        x, y = self.cell_xy(0)

        up = y - 1
        down = y + 1
        left = x - 1
        right = x + 1

        moves = []
        if up > -1: moves.append((x, up))
        if down < Board.gridh : moves.append((x, down))
        if left > -1: moves.append((left, y))
        if right < Board.gridw : moves.append((right, y))
        return moves
    
    def print_grid(self):
        for row in self.grid:
            print row

class Node:
    def __init__(self, board, g_score = 0, move = None, came_from = None):
        self.board = board

        #結果のシーケンスを表示用
        self.move = move
        self.came_from = came_from

        self.g_score = g_score
        self.f_score = g_score + board.heuristic() #f(n)

    def print_move_sequence(self):
        '''
        結果のシーケンスを表示する
        '''
        moves = []
        node = self
        while node.came_from:
            moves.append((node.move[0] + 1, node.move[1] + 1))#(左上を（1,1）に)
            node = node.came_from
        moves.reverse()
        
        print(str(len(moves)) + " Moves:" + str(moves) + "\n")
    
    def create_children(self):
        nodes = []
        for move in self.board.create_moves():
            next_board = copy.deepcopy(self.board)
            next_board.take_move(move)
            nodes.append(Node(next_board, self.g_score + 1, move, self))
        return nodes

class AstarSolver:
    def find_node_in_set(self,nodeset,node_to_find):
        '''
        gridで比較
        '''
        for node in nodeset:
            if node.board.grid == node_to_find.board.grid:
                return node
        return None

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

    def solve(self,board):
        openset = [Node(board)]
        closedset = []

        while True:
            node = self.get_lowest_node(openset)

            if node.board.heuristic() == 0:
                print("Solved!")
                node.print_move_sequence()
                break
            else:
                openset.remove(node)
                for child in node.create_children():
                    if self.find_node_in_set(closedset,child):
                        continue

                    node_in_open_set = self.find_node_in_set(openset,child)
                    if not node_in_open_set:
                        openset.append(child)
                    elif child.g_score < node_in_open_set.g_score:
                        openset.remove(node_in_open_set)
                        openset.append(child)

                closedset.append(node)

class Helper:
    def __init__(self, gridw=3, gridh=4):
        Board.gridw  = gridw
        Board.gridh  = gridh
        Board.size = gridw * gridh

        #ターゲット
        Board.target = {}
        for cell in range(Board.size):
            Board.target[cell] = cell % Board.gridw, cell / Board.gridw

    def str2grid(self,inputstr):
        cells = [int(n) for n in inputstr.split(" ")]
        grid = []
        for y in xrange(Board.gridh):
            row = []
            for x in xrange(Board.gridw):
                row.append(cells[y * Board.gridw + x])
            grid.append(row)
        return grid

def main():
    #create 3x4 board, and final target 
    helper = Helper() #Helper(3,4) 

    astar = AstarSolver()

    with open(sys.argv[1]) as file:
        inputs = file.readlines()

    for inputstr in inputs:
        #read cells to grid
        grid = helper.str2grid(inputstr)
        board = Board(grid)

        #print grid
        board.print_grid()

        #solve
        astar.solve(board)

if __name__ == "__main__":
    main()
