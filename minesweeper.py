class Minesweeper(object):
    '''
    size:           (2-element tuple) size of mine map and game board
    n_mine:         (int) number of mines
    n_remaining:    (int) number of remaining mines
    game_status:    (int) game status:
                        0: ongoing
                        1: win
                        2: lose
    board:          (2D list, size) player game board:
                         : not visited
                        n(0-8): visited with n mines around
                        P: flag as mine
                        #: explosion
    __n_unvisited:  (int) number of unvisited cells
    __map:          (2D ndarray, size) map of mines: 
                        0: cell without mine
                        1: cell with mine
    __mine_count:   (2D ndarray, size) count of mines in the 8 cells around
    '''

    # initialization
    def __init__(self, size=(9,9), n_mine=10):
        self.size = size
        self.n_mine = n_mine
        self.n_remaining = n_mine
        self.game_status = 0
        
        self.__n_unvisited = size[0]*size[1]

        # if n_mine > size, return error
        if n_mine > size[0]*size[1]:
            print("Error: too many mines")
            return
        
        # randomly pick cells for mines
        self.__mines = np.random.choice(size[0]*size[1], n_mine, False)
        
        # generate mine map (size[0]*size[1]; 1: cell with mine, 0: cell without mine)
        self.__map = np.zeros(size, dtype=np.int8)
        for mine in self.__mines:
            self.__map[mine//size[1]][mine%size[1]] = 1

        # generate mine count (size[0]*size[1]; number of mines in 8 cells around)
        self.__mine_count = np.zeros(size, dtype=np.int8)
        for mine in self.__mines:
            i = mine//size[1]
            j = mine%size[1]
            if i>0 and j>0:
                self.__mine_count[i-1][j-1] += 1
            if j>0:
                self.__mine_count[i][j-1] += 1
            if i<size[0]-1 and j>0:
                self.__mine_count[i+1][j-1] += 1
            if i>0: 
                self.__mine_count[i-1][j] += 1
            if i<size[0]-1:
                self.__mine_count[i+1][j] += 1
            if i>0 and j<size[1]-1:
                self.__mine_count[i-1][j+1] += 1
            if j<size[1]-1:
                self.__mine_count[i][j+1] += 1
            if i<size[0]-1 and j<size[1]-1:
                self.__mine_count[i+1][j+1] += 1

        # generate game board (size[0]*size[1])
        self.board = [[" " for i in range(size[1])] for i in range(size[0])]

        # show game board
        self.__show_board()
        

    # private methods: 
    # show game board
    def __show_board(self):
        print("remaining mines: ", end="")
        print(self.n_remaining)
        for j in range(self.size[1]):
            print("----", end="")
        print("-")
        for i in range(self.size[0]):
            print("|", end="")
            for j in range(self.size[1]):
                print(" ", end="")
                print(self.board[i][j], end="")
                print(" |", end="")
            print("")
            for j in range(self.size[1]):
                print("----", end="")
            print("-")
        print("\n")

    # check flags
    def __check_board(self):
        for mine in self.__mines:
            i = mine//self.size[1]
            j = mine%self.size[1]
            if self.board[i][j]!="P":
                self.board[i][j] = "#"
                self.game_status = 2
                print("you lose")
                return
        self.game_status = 1
        print("you win")

    # visit cell quietly
    def __visit_cell(self, cell):
        if len(cell)!=2 or cell[0] not in range(self.size[0]) or cell[1] not in range(self.size[1]):
            print("invalid cell index")
            return
        
        if self.__map[cell[0]][cell[1]] == 1:
            self.board[cell[0]][cell[1]] = "#"
            self.game_status = 2
            print("you lose")
            return
        
        if self.board[cell[0]][cell[1]] != " ":
            return
        
        self.board[cell[0]][cell[1]] = str(self.__mine_count[cell[0]][cell[1]])
        self.__n_unvisited -= 1

        if self.__n_unvisited == 0:
            self.__check_board()

        # iterate if no mine detected
        i = cell[0]
        j = cell[1]
        if self.__mine_count[i][j] == 0: 
            if i>0 and j>0:
                self.__visit_cell((i-1,j-1))
            if j>0:
                self.__visit_cell((i,j-1))
            if i<self.size[0]-1 and j>0:
                self.__visit_cell((i+1,j-1))
            if i>0: 
                self.__visit_cell((i-1,j))
            if i<self.size[0]-1:
                self.__visit_cell((i+1,j))
            if i>0 and j<self.size[1]-1:
                self.__visit_cell((i-1,j+1))
            if j<self.size[1]-1:
                self.__visit_cell((i,j+1))
            if i<self.size[0]-1 and j<self.size[1]-1:
                self.__visit_cell((i+1,j+1))        

    # flag cell quietly
    def __flag_cell(self, cell):
        if len(cell)!=2 or cell[0] not in range(self.size[0]) or cell[1] not in range(self.size[1]):
            print("invalid cell index")
            return
        if self.n_remaining == 0:
            print("no flag remaining; please check existing flags")
            return
        
        if self.board[cell[0]][cell[1]] == " ":
            self.board[cell[0]][cell[1]] = "P"
            self.n_remaining -= 1
            self.__n_unvisited -= 1
        elif self.board[cell[0]][cell[1]] == "P":
            self.board[cell[0]][cell[1]] = " "
            self.n_remaining += 1
            self.__n_unvisited += 1

        if self.__n_unvisited == 0:
            self.__check_board()


    # public methods: 
    # player actions: visit, flag
    def visit(self, cell):
        if self.game_status!=0:
            return
        print("visit", end="")
        print(cell)
        self.__visit_cell(cell)
        self.__show_board()
        
    def flag(self, cell):
        if self.game_status!=0:
            return
        print("flag", end="")
        print(cell)
        self.__flag_cell(cell)
        self.__show_board()
