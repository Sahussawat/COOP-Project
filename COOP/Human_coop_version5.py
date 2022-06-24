class Human:
    def __init__(self):
        pass

    def set_value_fn(self, value_fn):
        pass

    def set_symbol(self, symbol):
        self.symbol = symbol

    def update_winner_hist(self, s):
        pass

    def update_state_hist(self, s):
        pass

    def reset_state_hist(self):
        pass

    def update_value_fn(self, env):
        pass

    def take_action(self, env):
        while True:
            can_take = env.check_take(self.symbol)
            can_move = env.check_move(self.symbol)
            command = "waiting"
            picked_symbol = "waiting"
            if env.small_impossible() == True:                          # กรณีที่ หมากเล็ก take มาแล้วลงช่องไหนไม่ได้เลย
                print("You can't Take because it's Small Impossible !!!!!")
                command = "move"                        
            elif can_take == True and can_move == True:
                while True:
                    take_or_move = input('Enter command take or move : ')
                    if take_or_move == "take":
                        command = "take"
                        break
                    elif take_or_move == "move":
                        command = "move"
                        break
            elif can_take == True and can_move == False:
                print("Your symbol not append on board")
                command = "take"
            elif can_take == False and can_move == True:
                print("All of your symbol are already on board")
                print("You can't take more but you can move from board")
                command = "move"
            else:
                raise Exception("can't take and can't move it's impossible")

            if command == "take":
                    if self.symbol == "x":
                        x_big = env.x_big
                        x_medium = env.x_medium
                        x_small = env.x_small
                        total = x_big+x_medium+x_small
                        print("you have "+str(total)+" symbol left")
                        
                        if x_big != 0:
                            print("X_Big = "+str(x_big))
                        if x_medium != 0:
                            print("X_Medium = "+str(x_medium))
                        if x_small != 0:
                            print("X_Small = "+str(x_small))
                        
                        while True:
                            size = input("Select your symbol size for take action (Big , Medium , Small ): ")
                            if size == "Big" and x_big != 0:
                                picked_symbol = "Big"
                                break
                            elif size == "Medium"  and x_medium != 0:
                                picked_symbol = "Medium"
                                break
                            elif size == "Small"  and x_small != 0 :
                                picked_symbol = "Small"
                                break
                           
                           
                    elif self.symbol == "o":
                        o_big = env.o_big
                        o_medium = env.o_medium
                        o_small = env.o_small
                        total = o_big + o_medium + o_small
                        print("you have "+str(total)+" symbol left")
                       
                        if o_big != 0:
                            print("O_Big = "+str(o_big))
                        if o_medium != 0:
                            print("O_Medium = "+str(o_medium))
                        if o_small != 0:
                            print("O_Small = "+str(o_small))
                        

                        while True:

                            size = input("Select your symbol size for take action (Big , Medium , Small ): ")
                            if size == "Big" and o_big != 0:
                                picked_symbol = "Big"
                                break
                            elif size == "Medium"  and o_medium != 0:
                                picked_symbol = "Medium"
                                break
                            elif size == "Small"  and o_small != 0 :
                                picked_symbol = "Small"
                                break
                                    
                    else:
                        raise Exception("Symbol is wrong should be 'x' or 'o' ")
                    


                    if picked_symbol == "Big" or picked_symbol == "Medium" or picked_symbol == "Small":                 
                        while True:
                            next_move = input('Select your coordinates i, j for place your symbol (e.g, 0,1 ): ')
                            position = next_move.split(',')
                            if len(position) == 2:
                                if position[0] == "0" or position[0] == "1" or position[0] == "2"  :
                                    if position[1] == "0" or position[1] == "1" or position[1] == "2" :
                                        if picked_symbol == "Big":
                                            object_size = 3
                                        elif picked_symbol == "Medium":
                                            object_size = 2
                                        else:
                                            object_size = 1
                                        priority = env.priority(object_size,int(position[0]),int(position[1]))
                                        if priority == True:
                                            object_added = env.add_object(self.symbol,picked_symbol,int(position[0]),int(position[1]))
                                            env.board[int(position[0])][int(position[1])] = env.convert_Text_to_Number(object_added)
                                            #env.print_board()
                                            if self.symbol == "x" and picked_symbol == "Big":
                                                env.x_big -= 1
                                            elif self.symbol == "x" and picked_symbol == "Medium":
                                                env.x_medium -= 1
                                            elif self.symbol == "x" and picked_symbol == "Small":
                                                env.x_small -= 1
                                            elif self.symbol == "o" and picked_symbol == "Big":
                                                env.o_big -= 1
                                            elif self.symbol == "o" and picked_symbol == "Medium":
                                                env.o_medium -= 1
                                            elif self.symbol == "o" and picked_symbol == "Small":
                                                env.o_small -= 1
                                            else:
                                                raise Exception("Something Wrong With self.symbol or picked_symbol")

                                            break

            elif command == "move":
                env.check_move(self.symbol)
                moveable = env.can_move
                print("You can Move from this coordinates : "+str(moveable))
                while True:
                    next_move = input('Select your coordinates i, j for Move your symbol : ')
                    position = next_move.split(',')                                                     #
                    if len(position) == 2:                                                              #
                        if position[0] == "0" or position[0] == "1" or position[0] == "2"  :            #>>>>>>4 บรรทัดนี้ เอาไว้ check ว่า user ใส่ 0,1,2 มาถูกต้องไหม
                            if position[1] == "0" or position[1] == "1" or position[1] == "2" :         #
                                int_position = []
                                int_position.append(int(position[0]))
                                int_position.append(int(position[1]))
                                if int_position in moveable:                                              #ถ้าตำแหน่งที่ใส่มามันไม่ถูกต้อง จะไม่ทำไรเลย และโดนไล่ไปใส่ตำแหน่งใหม่ ที่ while true
                                    if env.moveable_priority(int_position[0],int_position[1]) == True:          #ถ้าหมากที่จะ move มันโยกได้ ให้เลือกช่องที่จะโยกต่ออีกที
                                        while True:
                                            print("You can move to this coordinates : " + str(env.moveable))
                                            target_input = input("Select Your target : ")
                                            target = target_input.split(',')
                                            if len(target) ==2:                                                               
                                                if target[0] == "0" or target[0] == "1" or target[0] == "2"  :
                                                    if target[1] == "0" or target[1] == "1" or target[1] == "2" :
                                                        int_target = []
                                                        int_target.append(int(target[0]))
                                                        int_target.append(int(target[1]))
                                                        if int_target in env.moveable:
                                                            picked_symbol = env.check_size_top_object_on_board(int_position[0],int_position[1])   #หยิบหมากบนสุดของตำแหน่งที่จะโยก
                                                            object_remove = env.remove_object(int_position[0],int_position[1])                    #ลดระดับ position ที่จะโยก
                                                            env.board[int_position[0]][int_position[1]] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position ที่จะโยก
                                                            if env.is_game_over() == True:
                                                                break                                                
                                                           
                                                            object_added = env.add_object(self.symbol,picked_symbol,int_target[0],int_target[1])  #เพิ่มระดับ target                                                           
                                                            env.board[int_target[0]][int_target[1]] = env.convert_Text_to_Number(object_added)    #เพิ่มระดับ target
                                                                                                             
                                                            break
                                        break         
                                    else:                                                               #ถ้าหมากที่จะ Move มันไปไหนไม่ได้เลย จะไล่กลับไปเลือกหมากใหม่ และลบตำแหน่งของหมากเก่า
                                        env.can_move.remove([int_position[0],int_position[1]])
                                        moveable = env.can_move
                                        print("Your Object on Board can't move to other coordinates")
                                        print("You can Move from this coordinates : "+str(moveable))                                                                   

            break

# a= Human()
# b= Human()
# env =Environment()
# a.set_symbol("x")
# b.set_symbol("o")
# current_player = None   
# while not env.is_game_over():
#     env.print_board()
#     if current_player == a:
#         print("O Turn")
#         current_player = b
#     else:
#         print("X Turn")
#         current_player = a

#     current_player.take_action(env)
   
# env.print_board()
# print("Winner is : "+ str(env.winner))



