import numpy as np
class Environment:
    def __init__(self):
        self.board = np.array([[0,0,0],[0,0,0],[0,0,0]])
        self.mock_board = np.array([[0,0,0],[0,0,0],[0,0,0]])               #เอาไว้check win
        self.reverse_board = np.array([[0,0,0],[0,0,0],[0,0,0]]) 
        self.x = "x"
        self.o = "o"
        self.winner = 0
        self.ended = False
        
        self.x_big = 2
        self.x_medium = 2
        self.x_small = 2
        self.o_big = 2
        self.o_medium = 2
        self.o_small = 2

        self.can_move = []
        self.moveable = []

    
    def reverse(self):
        board = []
        count = 0
        for i in range(3):
            for j in range(3):
                board.append(self.board[i][j])
        reverse_board = board[::-1]
        for i in range(3):
            for j in range(3):
                self.reverse_board[i][j] = reverse_board[count]
                count += 1
        return reverse_board
        
    def get_state(self):                                
        k = 0
        h = 0
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    v = 0
                elif self.board[i, j] == 1:
                    v = 1
                elif self.board[i, j] == 2:
                    v = 2
                elif self.board[i, j] == 3:
                    v = 3
                elif self.board[i, j] == 4:
                    v = 4
                elif self.board[i, j] == 5:
                    v = 5
                elif self.board[i, j] == 6:
                    v = 6
                elif self.board[i, j] == 7:
                    v = 7
                elif self.board[i, j] == 8:
                    v = 8
                elif self.board[i, j] == 9:
                    v = 9
                elif self.board[i, j] == 10:
                    v = 10
                elif self.board[i, j] == 11:
                    v = 11
                elif self.board[i, j] == 12:
                    v = 12
                elif self.board[i, j] == 13:
                    v = 13
                elif self.board[i, j] == 14:
                    v = 14
                elif self.board[i, j] == 15:
                    v = 15
                elif self.board[i, j] == 16:
                    v = 16
                elif self.board[i, j] == 17:
                    v = 17
                elif self.board[i, j] == 18:
                    v = 18
                elif self.board[i, j] == 19:
                    v = 19
                elif self.board[i, j] == 20:
                    v = 20
                elif self.board[i, j] == 21:
                    v = 21
                elif self.board[i, j] == 22:
                    v = 22
                elif self.board[i, j] == 23:
                    v = 23
                elif self.board[i, j] == 24:
                    v = 24
                elif self.board[i, j] == 25:
                    v = 25
                elif self.board[i, j] == 26:
                    v = 26


                h += (27**k) * v
                k += 1

        return h      # ได้เลขฐาน10

    def small_impossible(self):
        check = 0
        for i in range(3):
            for j in range(3):
                if self.priority(1,i,j) == False:
                    check += 1
        if check == 9 and self.x_big == 0 and self.x_medium == 0:
            return True
        elif check == 9 and self.o_big == 0 and self.o_medium == 0:
            return True
        else:
            return False

                    
        
    def check_big(self,symbol):
        if symbol == "x":
            if self.x_big == 0:
                return False
            return True
        elif symbol == "o":
            if self.o_big == 0:
                return False
            return True
        else:
            raise Exception("Something Wrong With check_big")
    
    def check_medium(self,symbol):
        if symbol == "x":
            if self.x_medium == 0:
                return False
            return True
        elif symbol == "o":
            if self.o_medium == 0:
                return False
            return True
        else:
            raise Exception("Something Wrong With check_medium")
    
    def check_small(self,symbol):
        if symbol == "x":
            if self.x_small == 0:
                return False
            return True
        elif symbol == "o":
            if self.o_small == 0:
                return False
            return True
        else:
            raise Exception("Something Wrong With check_small")
    
    def check_take(self,symbol): #มันดูแค่ว่ามีหมากเหลือไหม แต่มันจะเหลือกรณีที่ มีหมากเหลือ แต่ลงไม่ได้อยู่ดีอยู่ด้วย 
        if symbol == "x":
            if self.check_big("x") == False and self.check_medium("x") == False and self.check_small("x") == False:
                return False
            else:
                return True
        elif symbol == "o":
            if self.check_big("o") == False and self.check_medium("o") == False and self.check_small("o") == False:
                return False
            else:
                return True
        else:
            raise Exception("Something Wrong With check_take")
    
    
    def get_reward(self, symbol):
        if not self.is_game_over():
            return 0
        if symbol == "x":
            return 1 if self.winner == 1 else 0
        elif symbol == "o":
            return 1 if self.winner == 2 else 0
        else:
            raise Exception("Symbol is Wrong")


    

    def check_size_top_object_on_board(self,row,column):
        checking = self.board[row][column]
        if checking == 0:
            return ""
        elif checking == 1:
            return "Small"
        elif checking == 2:
            return "Medium"
        elif checking == 3:
            return "Big"
        elif checking == 4:
            return "Small"
        elif checking == 5:
            return "Medium"
        elif checking == 6:
            return "Big"
        elif checking == 7:
            return "Medium"
        elif checking == 8:
            return "Big"
        elif checking == 9:
            return "Medium"
        elif checking == 10:
            return "Big"
        elif checking == 11:
            return "Medium"
        elif checking == 12:
            return "Big"
        elif checking == 13:
            return "Medium"
        elif checking == 14:
            return "Big"
        elif checking == 15:
            return "Big"
        elif checking == 16:
            return "Big"
        elif checking == 17:
            return "Big"
        elif checking == 18:
            return "Big"
        elif checking == 19:
            return "Big"
        elif checking == 20:
            return "Big"
        elif checking == 21:
            return "Big"
        elif checking == 22:
            return "Big"
        elif checking == 23:
            return "Big"
        elif checking == 24:
            return "Big"
        elif checking == 25:
            return "Big"
        elif checking == 26:
            return "Big"
        else:
            raise Exception("Something Wrong With check_size_top_object_on_board")
    
    def check_object_on_board(self,row,column):
        checking = self.board[row][column]
        if checking == 0:
            return ""
        elif checking == 1:
            return "X_Small"
        elif checking == 2:
            return "X_Medium"
        elif checking == 3:
            return "X_Big"
        elif checking == 4:
            return "O_Small"
        elif checking == 5:
            return "O_Medium"
        elif checking == 6:
            return "O_Big"
        elif checking == 7:
            return "X_Small_X_Medium"
        elif checking == 8:
            return "X_Small_X_Big"
        elif checking == 9:
            return "X_Small_O_Medium"
        elif checking == 10:
            return "X_Small_O_Big"
        elif checking == 11:
            return "O_Small_X_Medium"
        elif checking == 12:
            return "O_Small_X_Big"
        elif checking == 13:
            return "O_Small_O_Medium"
        elif checking == 14:
            return "O_Small_O_Big"
        elif checking == 15:
            return "X_Medium_X_Big"
        elif checking == 16:
            return "X_Medium_O_Big"
        elif checking == 17:
            return "O_Medium_X_Big"
        elif checking == 18:
            return "O_Medium_O_Big"
        elif checking == 19:
            return "X_Small_X_Medium_X_Big"
        elif checking == 20:
            return "X_Small_X_Medium_O_Big"
        elif checking == 21:
            return "X_Small_O_Medium_X_Big"
        elif checking == 22:
            return "X_Small_O_Medium_O_Big"
        elif checking == 23:
            return "O_Small_X_Medium_X_Big"
        elif checking == 24:
            return "O_Small_X_Medium_O_Big"
        elif checking == 25:
            return "O_Small_O_Medium_X_Big"
        elif checking == 26:
            return "O_Small_O_Medium_O_Big"
        else:
            raise Exception("Something Wrong With check_object_on_board")
    
    def convert_Text_to_Number(self,text):
        if text == "":
            return 0
        elif text == "X_Small":
            return 1
        elif text == "X_Medium":
            return 2
        elif text == "X_Big":
            return 3
        elif text == "O_Small":
            return 4
        elif text == "O_Medium":
            return 5
        elif text == "O_Big":
            return 6
        elif text == "X_Small_X_Medium":
            return 7
        elif text == "X_Small_X_Big":
            return 8
        elif text == "X_Small_O_Medium":
            return 9
        elif text == "X_Small_O_Big":
            return 10
        elif text == "O_Small_X_Medium":
            return 11
        elif text == "O_Small_X_Big":
            return 12
        elif text == "O_Small_O_Medium":
            return 13
        elif text == "O_Small_O_Big":
            return 14
        elif text == "X_Medium_X_Big":
            return 15
        elif text == "X_Medium_O_Big":
            return 16
        elif text == "O_Medium_X_Big":
            return 17
        elif text == "O_Medium_O_Big":
            return 18
        elif text == "X_Small_X_Medium_X_Big":
            return 19
        elif text == "X_Small_X_Medium_O_Big":
            return 20
        elif text == "X_Small_O_Medium_X_Big":
            return 21
        elif text == "X_Small_O_Medium_O_Big":
            return 22
        elif text == "O_Small_X_Medium_X_Big":
            return 23
        elif text == "O_Small_X_Medium_O_Big":
            return 24
        elif text == "O_Small_O_Medium_X_Big":
            return 25
        elif text == "O_Small_O_Medium_O_Big":
            return 26
        else:
            raise Exception("Something Wrong With check_object_on_board")
    
    def add_object(self,symbol,object_size,row,column):
        new_symbol = symbol.upper()
        board = self.check_object_on_board(row,column)
        if board == "":
            board_added = new_symbol+"_"+object_size
            return board_added
        board_added = board+"_"+new_symbol+"_"+object_size
        if len(board_added.split("_")) > 6:
            raise Exception("Something Wrong With add_object")
        return board_added
    
    def remove_object(self,row,column):
        board = self.check_object_on_board(row,column)
        if board == "":
            raise Exception("Something Wrong With remove_object")
        splited_board = board.split("_")
        splited_board.pop()
        splited_board.pop()
        value_on_board = ""
        if len(splited_board) == 4:
            for i in range(3):
                value_on_board += splited_board[i]+"_"
            value_on_board += splited_board[3]
        elif len(splited_board) == 2:
            value_on_board = splited_board[0]+"_"+splited_board[1]

        return value_on_board
    
        

    def priority(self,object_size,row,column):                      #เช็คว่าหมากในช่องนั้นใหญ่กว่า object size ไหม
        size_top = self.check_size_top_object_on_board(row,column)
        if size_top == "":
            board_size = 0
        elif size_top == "Big":
            board_size = 3
        elif size_top == "Medium":
            board_size = 2
        else:
            board_size = 1
            
        if object_size <= board_size:
            return False
        else:
            return True

    def moveable_priority(self,row,column):                         #เช็คว่า หมากที่หยิบมา จากช่อง row,column นั้นสามารถขยับไปช่องไหนได้บ้าง
        self.moveable = []
        size_top = self.check_size_top_object_on_board(row,column)
        if size_top == "":
            board_size = 0
        elif size_top == "Big":
            board_size = 3
        elif size_top == "Medium":
            board_size = 2
        else:
            board_size = 1

        for i in range(3):
            for j in range(3):
                if self.priority(board_size,i,j) == True:
                    self.moveable.append([i,j])

        if self.moveable != []:
            return True
        else:
            return False
                



    def convert_value_number_to_top_symbol(self,number): # https://docs.google.com/document/d/1d5Vb0XwCJ8eMddU_6yUxJVcWmDIGqUWwZfYjJGAAT3U/edit
        # x = 1 , o = 2
        if number>=0 and number < 27:
            if number == 0:
                return 0
            elif number == 1:
                return 1
            elif number == 2:
                return 1
            elif number == 3:
                return 1
            elif number == 4:
                return 2
            elif number == 5:
                return 2
            elif number == 6:
                return 2
            elif number == 7:
                return 1
            elif number == 8:
                return 1
            elif number == 9:
                return 2
            elif number == 10:
                return 2
            elif number == 11:
                return 1
            elif number == 12:
                return 1
            elif number == 13:
                return 2
            elif number == 14:
                return 2
            elif number == 15:
                return 1
            elif number == 16:
                return 2
            elif number == 17:
                return 1
            elif number == 18:
                return 2
            elif number == 19:
                return 1
            elif number == 20:
                return 2
            elif number == 21:
                return 1
            elif number == 22:
                return 2
            elif number == 23:
                return 1
            elif number == 24:
                return 2
            elif number == 25:
                return 1
            elif number == 26:
                return 2
        else:
            raise Exception("Something Wrong With convert_value_number_to_top_symbol")
    
    def build_mock_board(self):
        for row in range(3):
            for column in range(3):
                value = self.board[row][column]
                self.mock_board[row][column]=self.convert_value_number_to_top_symbol(value)

    def check_move(self,symbol):
        self.build_mock_board()
        if symbol == "x":
            self.can_move = []
            for i in range(3):
                for j in range(3):
                    if self.mock_board[i][j] == 1:
                        self.can_move.append([i,j])

            if len(self.can_move) == 0:
                return False
            elif len(self.can_move) > 9:
                raise Exception("can_move Wrong cause value > 9")
            else:
                return True

        elif symbol == "o":
            self.can_move = []
            for i in range(3):
                for j in range(3):
                    if self.mock_board[i][j] == 2:
                        self.can_move.append([i,j])
                        
            if len(self.can_move) == 0:
                return False
            elif len(self.can_move) > 9:
                raise Exception("can_move Wrong cause value > 9")
            else:
                return True

        else:
            raise Exception("Something Wrong With check_move")

    def is_game_over(self):
        self.build_mock_board()
        for row in range(3):
            if self.mock_board[row][0]== self.mock_board[row][1] == self.mock_board[row][2] != 0:
                self.winner = self.mock_board[row][0]
                self.ended = True
                return True

        for column in range(3):
            if self.mock_board[0][column]== self.mock_board[1][column] == self.mock_board[2][column] != 0:
                self.winner = self.mock_board[0][column]
                self.ended = True
                return True

        if self.mock_board[0][0] == self.mock_board[1][1] == self.mock_board[2][2] != 0:
            self.winner = self.mock_board[0][0]
            self.ended = True
            return True

        elif self.mock_board[0][2] == self.mock_board[1][1] == self.mock_board[2][0] != 0:
            self.winner = self.mock_board[0][2]
            self.ended = True
            return True
        else:
            self.winner = 0
            self.ended = False
            return False
            
    # def is_game_over(self):
    #     rotated_board = np.rot90(self.board,3)
    #     for row in self.board:  #เช็คแนวนอน
    #         if row[0]==row[1]==row[2]:
    #             if row[0] != 0:
    #                 self.winner = row[0]
    #                 self.ended = True
    #                 return True
    #     for row in rotated_board: #เช็คแนวตั้ง
    #         if row[0]==row[1]==row[2]:
    #             if row[0] != 0:
    #                 self.winner = row[0]
    #                 self.ended = True
    #                 return True
    #     if self.board[0,0]==self.board[1,1]==self.board[2,2]: #เช็คแนวทแยงจากซ้ายบน
    #         if self.board[1,1] != 0:
    #             self.winner = self.board[1,1]
    #             self.ended = True
    #             return True
    #     if rotated_board[0,0]==rotated_board[1,1]==rotated_board[2,2]: #เช็คแนวทแยงจากขวาบน
    #         if rotated_board[1,1] != 0:
    #             self.winner = self.board[1,1]
    #             self.ended = True
    #             return True

    #     # Check if draw
    #     if np.min(self.board) != 0:
    #         self.winner = None
    #         self.ended = True
    #         return True

    #     # Game is not over
    #     self.winner = None
    #     self.ended = False
    #     return False


    
    def print_board(self):                      
        print('============ Board ============')
        for i in range(3):
            print('-------------')
            for j in range(3):
                print('| ', end='')
                print(self.board[i, j], end='')
            print('|')
        print('-------------')
    
    def place(self,player,row,column): # รอ priority จาก ฝั่งเกม
        self.board[row][column] = player

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = 0
                self.mock_board[i][j] = 0
    
    def rotate_board(self):
        rotated_board = np.rot90(self.board,np.random.choice(4))
        self.board = rotated_board

def convert_base10_to_base27 (decimal):
    conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
                        5: '5', 6: '6', 7: '7',
                        8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
                        13: 'D', 14: 'E', 15: 'F', 16 : 'G' , 17 : 'H',
                        18 : 'I', 19 : 'J', 20 : 'K', 21 : 'L', 22 : 'M',
                        23 : 'N', 24 : 'O', 25 : 'P', 26 : 'Q'}
    base27 = ''
    while(decimal > 0):
            remainder = decimal % 27
            base27  = conversion_table[remainder] + base27 
            decimal = decimal // 27

    while len(base27) < 9:
        base27 = "0" + base27
    
    return base27 

# a = Environment()

# a.print_board()
# print("State Decimal is : ",a.get_state())
# base27 = convert_base10_to_base27(a.get_state())
# re = ""
# for i in str(base27):
#     re = i+re
# print("State Base 27 is : ",re)
# a.moveable_priority(1,1)
# print("Object from Position (1,1) Can Move to : ",a.moveable)


