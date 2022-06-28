
import random
import re


class MineSweeper:
    def __init__(self,dim_size,num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        
        # Creating board for the given dimensions 
        self.board = self.generate_board()

        self.assign_values_to_board()

        self.dug = set()
    
    def generate_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # print(board)

        # now we are going to implant the bombs

        # find location to plant the bomb using random
        bombs_planted = 0
        while bombs_planted<self.num_bombs:
            location = random.randint(0,self.dim_size**2-1)
            row = location//self.dim_size
            col = location%self.dim_size

            if board[row][col] != '*':
                board[row][col] = '*'
                bombs_planted += 1
            
        return board

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] != '*':
                    self.board[r][c] = self.find_count_of_nearby_bombs(r,c)
                
    def find_count_of_nearby_bombs(self,row,col):
        count = 0
        for r in range(max(0,row-1),min(self.dim_size-1, row+1)+1):
            for c in range(max(0,col-1),min(self.dim_size-1,col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    count += 1
        return count

    def dig(self,row,col):
        if (row,col) in self.dug:
            print('You are Diggging already digged Spot')
            return True
        self.dug.add((row,col))
        # print(f'{row} and {col}')
        if self.board[row][col] == '*':
            return False
        if self.board[row][col] > 0 :
            return True
        
        for r in range(max(0,row-1), min(self.dim_size-1,row+1)+1):
            for c in range(max(0,col-1), min(self.dim_size-1,col+1)+1):
                if (r,c) not in self.dug:
                    self.dig(r,c)

        return True

    def __str__(self):
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep
        
        







# play the game
def play(dim_size=10,num_bombs=10):
    game = MineSweeper(dim_size,num_bombs)
    safe = True
    while len(game.dug)< dim_size**2-num_bombs:
        print(game)
        user_input = re.split(',(\\s)*', input("Enter location as Row,Column: "))
        # print(user_input)
        row,col = int(user_input[0]),int(user_input[-1])

        if row<0 or row>=dim_size or col<0 or col>= dim_size:
            continue

        safe = game.dig(row,col)

        if not safe:
            break
    
    if safe:
        print("Congratulations, You Won!!!")
    else:
        print("Game Over!!!")
    
    game.dug = [(r,c) for r in range(dim_size) for c in range(dim_size)]
    print(game)
    

if __name__ == "__main__":
    play()