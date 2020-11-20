#Autorrzy: Mateusz Konarzewski & Bartsz Konarzewski
# https://pl.wikipedia.org/wiki/Okr%C4%99ty
# Plansza o wielkości 5x5, każdy grasz posiada 3 statki o rozmiarach 1x3

import random
from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax
class Ship:
    def __init__(self, ship_size, begining, position_h_or_v):
        '''
        :param ship_size:
        :type ship_size:
        :param begining:
        :type begining:
        :param position_h_or_v:
        :type position_h_or_v:
        '''
        self.ship_size = ship_size
        self.begining = begining
        self.h_or_v = position_h_or_v
class ShootingBoard():
    def __init__(self, *ai):
        '''
        Function initializing AI shooting board
        :param ai:
        :type ai:
        '''
        self.board = [i for i in range(1, 26)]
        self.hunt_mode = False
        self.last_shoot_was_down = False
        self.hunt_counter = 0
        self.cross_moves = []
        self.last_shoot = 0
    def setBoard(self, board):
        '''
        Setting board
        :param board:
        :type board:
        :return:
        :rtype:
        '''
        self.board = board
    def print_anonimized_board(self):
        """
        Function used to print graphic representation of board
        """
        counter = 0
        for s in self.board:
            if isinstance(s, int) and s > 0:
                print("  ~", end='')
            elif isinstance(s, int) and s < 0:
                print("  x", end='')
            elif isinstance(s, int) and s == 0:
                print("  o", end='')
            else:
                print(" ", s, end='')
            counter = counter + 1
            if counter == 5:
                counter = 0
                print(" ")
    def get_board(self):
        """
        Function to get board as list
        :return: board
        """
        return self.board
    def get_possible_moves(self):
        '''
        Function getting possible moves
        :return:
        :rtype:
        '''
        moves = []
        for i in self.board:
            if isinstance(i, int) and i > 0:
                moves.append(i)
        return moves
    def best_moves(self, l):
        '''
        Function to get most possible ships coordinates
        :param l:
        :type l:
        :return: all_moves
        :rtype: list
        '''
        move = self.cross_moves
        all_moves = self.get_possible_moves()
        if self.last_shoot_was_down:
            if l+5 in all_moves:
                self.cross_moves.append(l+5)
            if l-5 in all_moves:
                self.cross_moves.append(l-5)
            if l+1 in all_moves:
                self.cross_moves.append(l+1)
            if l-1 in all_moves:
                self.cross_moves.append(l-1)
        if self.hunt_counter >= 6:
            hunt_mode = False
            self.cross_moves = []
            self.hunt_counter = 0
            return all_moves
        else:
            if l in self.cross_moves:
                self.cross_moves.remove(l)
            all_moves = self.cross_moves
            self.hunt_counter += 1
        if len(all_moves) <= 0:
            all_moves = self.get_possible_moves()
        return all_moves
    def make_shot(self, move, board):
        '''
        Function  to make shot and check if ship has been hit
        :param move:
        :type move:
        :param board:
        :type board:
        :return: opponent_board
        :rtype: Board
        '''
        opponent_board = board.get_board()
        player_shooting_board = self.get_board()
        shot = opponent_board[move-1]
        if isinstance(shot, int):
            if shot == 0:
                opponent_board[move-1] = -1
                player_shooting_board[move-1] = 's'
                self.last_shoot_was_down = True
                self.hunt_mode = True
            if shot > 0:
                opponent_board[move-1] = 'm'
                player_shooting_board[move-1] = 'm'
                self.last_shoot_was_down = False
            self.setBoard(player_shooting_board)
            self.last_shoot = move
            #ta metoda ma zwracać shooting board a nie board
        return opponent_board
    def print_board_numbers(self, board):
        '''
        Function printing board for first time to better understanding of coordinates
        :param board:
        :type board:
        '''
        counter = 0
        for s in board:
            # print(type(s))
            if isinstance(s, int) and s < 10:
                print("  ", s, "", end='')
            elif isinstance(s, str):
                print("   O ", end='')
            else:
                print(" ", s, "", end='')
            counter = counter + 1
            if counter == 5:
                counter = 0
                print(" ")
class Board(ShootingBoard):
    def __init__(self, *ai):
        super(Board, self).__init__()
        if ai:
            self.get_random_ships()
        else:
            self.get_ships_from_input()

    def get_ships_from_input(self):
        '''
        Function getting player ships from input
        '''
        placed_ships = 0
        while placed_ships < 3:
            self.print_board_numbers(self.board)
            beg = input("Podaj początkową współrzędną statku ")
            v_or_h = input("Wybierz położenie statku, poziomo - wpisz h, pionowo wpisz v")
            ship = Ship(3, int(beg), v_or_h)
            if self.place_ship_on_board(ship):
                placed_ships += 1
        self.print_board_numbers(self.board)

    def get_random_ships(self):
        '''
         Function is genarating random localized ships for AI
        '''
        placed_ships = 0
        numbers = [i for i in range(1, 26)]
        rotation = ['v', 'h']
        while placed_ships < 3:
            #self.print_board_numbers(self.board)
            beg = random.choice(numbers)
            numbers.remove(beg)
            v_or_h = random.choice(rotation)
            ship = Ship(3, int(beg), v_or_h)
            if self.place_ship_on_board(ship):
                placed_ships += 1
       # self.print_board_numbers(self.board)
        print("All AI ships are on board")
    def are_coordinates_free(self, board, size, begin, h_v):
        '''
         Function for checking  if coordinates no board are not occupied
        :param board:
        :type board:
        :param size:
        :type size:
        :param begin:
        :type begin:
        :param h_v:
        :type h_v:
        :return: statement1 and statement2 and statement3
        :rtype: boolean
        '''
        if h_v == 'h':
            middle = begin + 1
            ending = begin + 1 + 1
        if h_v == 'v':
            middle = begin + 5
            ending = begin + 5 + 5
        statement1 = middle in board
        statement2 = begin in board
        statement3 = ending in board
        return statement1 and statement2 and statement3
    def place_ship_on_board(self, ship):
        '''
        Function for placing ships on board
        :param ship:
        :type ship:
        :return: True
        :rtype: boolean
        '''
        if ship.begining in self.board:
            start = self.board.index(ship.begining)
            # print(self.board.index(ship.begining))
            if ship.h_or_v == 'h':
                if start % 5 < ship.ship_size and self.are_coordinates_free(self.board, ship.ship_size, ship.begining,
                                                                            ship.h_or_v):
                    self.board[start] = 0
                    for i in range(ship.ship_size):
                        self.board[start + (i)] = 0
                    return True
            elif ship.h_or_v == 'v' and self.are_coordinates_free(self.board, ship.ship_size, ship.begining,
                                                                  ship.h_or_v):
                if start + (5 * (ship.ship_size - 1)) - 1 < len(self.board):
                    # self.board[start] = 'o'
                    for c in range(ship.ship_size):
                        self.board[(start) + 5 * c] = 0
                    return True
    def ships_left(self):
        '''
        Function checking how many ships are left on the board
        :return: board.count
        :rtype: int
        '''
        return self.board.count(0)
class SpaghettiShips(TwoPlayersGame):
    def __init__(self, players):
        self.players = players
        self.nplayer = 1  # player 1 starts
        self.ai_board = Board(ai)
        self.human_board = Board()
        self.boards = [self.human_board, self.ai_board]
        self.human_shooting_board = ShootingBoard()
        self.ai_shooting_board = ShootingBoard()
        self.shooting_boards = [self.human_shooting_board, self.ai_shooting_board]
    def show(self):
        '''
         Function printing player's  board and his shooting board
        '''
        if self.nplayer == 1:
            print("Your ships board: ")
            self.boards[0].print_anonimized_board()
            print("Your shooting board: ")
            self.shooting_boards[0].print_anonimized_board()
    def possible_moves(self):
        '''
        Function getting possible moves
        :return:
        :rtype:
        '''
        board = self.shooting_boards[self.nplayer-1]
        if board.hunt_mode and self.nplayer == 2:
            return board.best_moves(board.last_shoot)
        elif self.nplayer == 2:
            moves = self.shooting_boards[self.nplayer - 1].get_possible_moves()
            moves = random.sample(moves, len(moves))
            return moves
        else :
            return  self.shooting_boards[self.nplayer - 1].get_possible_moves()
    def make_move(self, move):
        '''
        Function making moves of both players (human and AI)
        :param move:
        :type move:
        '''
        if self.nplayer == 1:
            self.ai_board.setBoard(self.human_shooting_board.make_shot(move, self.ai_board))
        if self.nplayer == 2:
            self.human_board.setBoard(self.ai_shooting_board.make_shot(move, self.human_board))

    def lose(self):
        return self.boards[self.nplayer-1].ships_left() <= 0
    def is_over(self):
        return self.lose()
    def win(self):
        condition = self.boards[self.nopponent - 1].ships_left() <= 0 and self.boards[self.nplayer - 1].ships_left() > 0
        return condition
    def scoring(self):
        return 20 if self.win() else 0  # For the AI


## TO DO ##
# def possible_moves(self): return [self.hunt, self.target]
#
# def make_move(self, move): self.pile -= int(move)  # remove bones.
#
# def win(self): return self.opponent.board  # opponent took the last bone ?
#
# def is_over(self): return self.win()  # Game stops when someone wins.
#
# def scoring(self): return 100 if self.win() else 0  # For the AI
### MAYBY USABLE MAYBY NOT
# def hunt(self):
#     guess = random.randint(0, 99)
#     if guess in self.opponent.board:
#         return guess
#
# def randomly_locate_ships(board):
#     random.randint(0, 100)
#
# def ships_elements_left(list):
#     return -1 in list


# Start a match (and store the history of moves when it ends)
ai = Negamax(5)
game = SpaghettiShips([Human_Player(), AI_Player(ai)])
history = game.play()
