import numpy as np
from Environment_coop_version9 import Environment
from Human_coop_version5 import Human
class Agent:
    def __init__(self, eps=0.1, lr=0.5):
        self.epsilon = eps
        self.learning_rate = lr
        self.state_hist = []
        self.winner_hist = []
        self.print_value_fn = False
        self.value_fn = []
        self.results = []

    def set_print_value_fn(self,v):
        self.print_value_fn = v

    def set_eps(self,v):
        self.epsilon = v

    def set_value_fn(self,value_fn):
        self.value_fn = value_fn # ตัวใหญ่มากมีทุก state [0.5,0.5,0,0,1] ขึ้นอยู่กับเป็น x หรือ o จะตรงกันข้ามกัน
    
    def set_symbol(self,symbol):
        self.symbol = symbol

    def update_winner_hist(self, s):
        self.winner_hist.append(s)

    def update_state_hist(self, s):
        self.state_hist.append(s)
    
    def reset_state_hist(self):
        self.state_hist = []

    def update_value_fn(self, env):
        reward = env.get_reward(self.symbol)
        
        for state in reversed(self.state_hist): 
            target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ว่ามีไหม บรรทัดนี้ target คือ index ของ state ใน value_fn
            if len(target) == 1: #ถ้ามีให้ update value function
                value = self.value_fn[target[0]][1] + self.learning_rate * (reward - self.value_fn[target[0]][1])

                state_in_value_fn = self.value_fn[target[0]][0]             #ต้องเอาstate ตัวหน้ามาเก็บไว้ในตัวแปรนี้ก่อน
                self.value_fn[target[0]] = (state_in_value_fn,value)        #เพื่อที่บรรทัดนี้จะได้ใส่คืนเพื่อ update เพราะว่า ต้องupdate ทั้ง2ค่าพร้อมกัน ไม่งั้นจะติดปัญหา 'tuple'        ดูจาก stream week 32 part 1

                reward = value
            elif len(target) == 0: #ถ้าไม่มีให้ initial ใหม่ และให้คะแนน โดยการ update value function
                self.get_hash_state_winner_ended(env,state)
                target = [i for i,x in enumerate(self.value_fn) if x[0]==state]     #เช็ค state ใน value_fn อีกทีว่ามีไหม แต่ต้องมีเท่านั้น
                if len(target) == 1:                                                #ถ้ามีก็คำนวน และ ให้คะแนน (update value function)
                    value = self.value_fn[target[0]][1] + self.learning_rate * (reward - self.value_fn[target[0]][1])
                    
                    state_in_value_fn = self.value_fn[target[0]][0]             #ต้องเอาstate ตัวหน้ามาเก็บไว้ในตัวแปรนี้ก่อน
                    self.value_fn[target[0]] = (state_in_value_fn,value)        #เพื่อที่บรรทัดนี้จะได้ใส่คืนเพื่อ update เพราะว่า ต้องupdate ทั้ง2ค่าพร้อมกัน ไม่งั้นจะติดปัญหา 'tuple'        ดูจาก stream week 32 part 1

                    reward = value
                else:                                                               # ต้องมีเท่านั้น ถ้าไม่มีแปลว่ามีบางอย่างผิดพลาด
                    raise Exception("Something Wrong With Get Hash")

            else:
                raise Exception("Something Wrong With Update Value Function")

        self.reset_state_hist()
    
    
    def take_action(self,env):
        # Epsilon Greedy
        rand = np.random.random()

        if rand < self.epsilon:                            # AI สุ่มช่องลงหมาก หรือ ย้ายหมาก แบบมั่วๆ         
            # Random action
            percent_90 = [0,1,1,1,1,1,1,1,1,1]                  #โอกาสที่จะสุ่ม action move โดยที่ยังหมากใหญ่และหมากกลางหมด 90 %
            percent_70 = [0,0,0,1,1,1,1,1,1,1]                  #โอกาส 70%
            take_tactic = [3,3,3,3,2,2,2,1,1,1]                           #โอกาสเลือกหมากใหญ่ กลาง เล็ก แบบ 40 30 30

            can_take = env.check_take(self.symbol)
            can_move = env.check_move(self.symbol)
            command = "waiting"
            picked_symbol = "waiting"

            possible_take = []
            if env.small_impossible() == True:
                command = "move"
            elif can_take == True and can_move == True:

                if env.check_big(self.symbol) == True and env.check_medium(self.symbol) == True and env.check_small(self.symbol) == True: #เหลือทั้งหมด  take 100%
                    command = "take"
                elif env.check_big(self.symbol) == False and env.check_medium(self.symbol) == True and env.check_small(self.symbol) == True: #เหลือกลาง เล็ก take 90%
                    percent = np.random.choice(len(percent_90)) #สุ่ม 90/10 %
                    if percent_90[percent] == 1:
                        command = "take"
                    else:
                        command = "move"
                elif env.check_big(self.symbol) == False and env.check_medium(self.symbol) == False and env.check_small(self.symbol) == True: #เหลือแต่ เล็ก take 10%
                    percent = np.random.choice(len(percent_90)) #สุ่ม 90/10 %
                    if percent_90[percent] == 0:
                        command = "take"
                    else:
                        command = "move"
                elif env.check_big(self.symbol) == False and env.check_medium(self.symbol) == True and env.check_small(self.symbol) == False:   #เหลือแต่กลาง take 70%
                    percent = np.random.choice(len(percent_70)) #สุ่ม 70/30 %
                    if percent_70[percent] == 1:
                        command = "take"
                    else:
                        command = "move"
                else: #หมากเล็กหมด เหลือ กลาง ใหญ่ take 100%  , หมากกลางหมด เหลือ เล็ก ใหญ่ take 100% , เหลือแต่ใหญ่ take 100%
                    command = "take"

            
            elif can_take == True and can_move == False:
                command = "take"
            
            elif can_take == False and can_move == True:
                command = "move"
            else:
                raise Exception("can't take and can't move it's impossible")

            #หลังจากเลือกได้แล้วว่าจะ Take หรือ Move ต้องมาเลือก หมาก หรือ ช่องที่จะลง
            if command == "take":
                while True:
                    idx = np.random.choice(len(take_tactic)) #สุ่ม หมากจาก แผน 433
                    if take_tactic[idx] == 3:
                        if env.check_big(self.symbol) == True:
                            picked_symbol = 3           #เลือกหมากใหญ่
                            size = "Big"
                            if self.symbol == "x":
                                env.x_big -= 1
                            elif self.symbol == "o":
                                env.o_big -= 1
                            else:
                                raise Exception("Something Wrong With Symbol")
                            break
                    elif take_tactic[idx] == 2:
                        if env.check_medium(self.symbol) == True:
                            picked_symbol = 2           #เลือกหมากกลาง
                            size = "Medium"
                            if self.symbol == "x":
                                env.x_medium -= 1
                            elif self.symbol == "o":
                                env.o_medium -= 1
                            else:
                                raise Exception("Something Wrong With Symbol")
                            break
                    else:
                        if env.check_small(self.symbol) == True:
                            picked_symbol = 1           #เลือกหมากเล็ก
                            size = "Small"
                            if self.symbol == "x":
                                env.x_small -= 1
                            elif self.symbol == "o":
                                env.o_small -= 1
                            else:
                                raise Exception("Something Wrong With Symbol")
                            
                            break
                #หลังจากได้หมากที่จะลงในกระดานแล้ว ให้สุ่มหาช่องที่จะลง
                possible_take = []
                for i in range(3):
                    for j in range(3):
                        priority = env.priority(picked_symbol,i,j)
                        if priority == True:
                            possible_take.append([i,j])
                
                idx = np.random.choice(len(possible_take)) # สุ่ม index จาก possible take
                take_position = possible_take[idx]  
                
                object_added = env.add_object(self.symbol,size,int(take_position[0]),int(take_position[1]))
                env.board[int(take_position[0])][int(take_position[1])] = env.convert_Text_to_Number(object_added)
            
            elif command == "move":
                env.check_move(self.symbol)     #หาพิกัดของฝั่งตัวเอง ว่ามีหมากไหนลงอยู่บ้าง เก็บไว้ใน env.can_move
                moveable = env.can_move         #เปลี่ยนมาเก็บใน moveable
                idx = np.random.choice(len(moveable)) # สุ่ม index จาก moveable
                move_position = moveable[idx]           #จะได้ตำแหน่งของหมากที่จะย้าย
                if env.moveable_priority(move_position[0],move_position[1]) == True:
                    idx = np.random.choice(len(env.moveable)) # สุ่ม index จาก env.moveable
                    target_position = env.moveable[idx]          #จะได้ตำแหน่งที่จะย้ายหมากไป
                    if move_position in moveable and target_position in env.moveable:
                        picked_symbol = env.check_size_top_object_on_board(move_position[0],move_position[1])   #หยิบหมากบนสุดของตำแหน่ง move_position
                        object_remove = env.remove_object(move_position[0],move_position[1])                    #ลดระดับ position
                        env.board[move_position[0]][move_position[1]] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position

                        if env.is_game_over() == True:                                                          #ถ้ามีผู้ชนะตอนที่ยกออก จะจบการทำงานทันที
                            return 0
                     
                        
                        
                        object_added = env.add_object(self.symbol,picked_symbol,target_position[0],target_position[1])  #เพิ่มระดับ target     
                                                                         
                        env.board[target_position[0]][target_position[1]] = env.convert_Text_to_Number(object_added)    #เพิ่มระดับ target

                
            
            else:
                raise Exception("Command is Wrong")


        else:                                               # AI เล่นแบบคิดเอง 
            can_take = env.check_take(self.symbol)          #check ว่าลงหมากได้ไหม
            can_move = env.check_move(self.symbol)          #check ว่าโยกหมากได้ไหม
            all_action = {}                                     #การกระทำทั้งที่สามารถทำได้ ใน state นั้นๆ
            best_value = -999
            if can_take == True and can_move == True:       #ถ้าทำได้ทั้งลงหมากและโยกหมาก
                #ลองลงหมากทุกขนาด ไปทุกช่องที่ลงได้
                if env.check_big(self.symbol) == True :
                    picked_symbol = 3
                    size = "Big"
                    for i in range(3):
                        for j in range(3):
                            priority = env.priority(picked_symbol,i,j)
                            if priority == True:
                                object_added = env.add_object(self.symbol,size,i,j)         #ทดลองลงหมากใหญ่ ในทุกตำแหน่งที่ลงได้
                                env.board[i][j] = env.convert_Text_to_Number(object_added)
                                state = env.get_state()
                                target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ว่ามีไหม บรรทัดนี้ target คือ index ของ state ใน value_fn
                                if len(target) == 1:                        #ถ้ามี state ใน value_fn
                                    state_value = self.value_fn[target[0]][1]
                                    all_action[(3,i,j)] = state_value
                                    if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                        best_value = state_value
                                        action = [3,i,j]
                                    object_remove = env.remove_object(i,j)                    #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                    env.board[i][j] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                elif len(target) == 0:                      #ถ้าไม่มี state ใน value_fn
                                    self.get_hash_state_winner_ended(env,state) #initial ใหม่
                                    target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ซึ่งต้องมีเท่านั้น
                                    if len(target) == 1:
                                        state_value = self.value_fn[target[0]][1]
                                        all_action[(3,i,j)] = state_value
                                        if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                            best_value = state_value
                                            action = [3,i,j]
                                        object_remove = env.remove_object(i,j)                    #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                        env.board[i][j] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                    else:
                                        raise Exception("Something Wrong With Hash in Take Action")
                                else:
                                    raise Exception("Something Wrong With Hash in Take Action")
                                

                          

                if env.check_medium(self.symbol) == True :
                    picked_symbol = 2
                    size = "Medium"
                    for i in range(3):
                        for j in range(3):
                            priority = env.priority(picked_symbol,i,j)
                            if priority == True:
                                object_added = env.add_object(self.symbol,size,i,j)         #ทดลองลงหมากกลาง ในทุกตำแหน่งที่ลงได้
                                env.board[i][j] = env.convert_Text_to_Number(object_added)
                                state = env.get_state()
                                target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ว่ามีไหม บรรทัดนี้ target คือ index ของ state ใน value_fn
                                if len(target) == 1:                        #ถ้ามี state ใน value_fn
                                    state_value = self.value_fn[target[0]][1]
                                    all_action[(2,i,j)] = state_value
                                    if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                        best_value = state_value
                                        action = [2,i,j]
                                    object_remove = env.remove_object(i,j)                    #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                    env.board[i][j] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                elif len(target) == 0:                      #ถ้าไม่มี state ใน value_fn
                                    self.get_hash_state_winner_ended(env,state) #initial ใหม่
                                    target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ซึ่งต้องมีเท่านั้น
                                    if len(target) == 1:
                                        state_value = self.value_fn[target[0]][1]
                                        all_action[(2,i,j)] = state_value
                                        if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                            best_value = state_value
                                            action = [2,i,j]
                                        object_remove = env.remove_object(i,j)                    #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                        env.board[i][j] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                    else:
                                        raise Exception("Something Wrong With Hash in Take Action")
                                else:
                                    raise Exception("Something Wrong With Hash in Take Action")
                                


                if env.check_small(self.symbol) == True :
                    picked_symbol = 1
                    size = "Small"
                    for i in range(3):
                        for j in range(3):
                            priority = env.priority(picked_symbol,i,j)
                            if priority == True:
                                object_added = env.add_object(self.symbol,size,i,j)         #ทดลองลงหมากเล็ก ในทุกตำแหน่งที่ลงได้
                                env.board[i][j] = env.convert_Text_to_Number(object_added)
                                state = env.get_state()
                                target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ว่ามีไหม บรรทัดนี้ target คือ index ของ state ใน value_fn
                                if len(target) == 1:                        #ถ้ามี state ใน value_fn
                                    state_value = self.value_fn[target[0]][1]
                                    all_action[(1,i,j)] = state_value
                                    if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                        best_value = state_value
                                        action = [1,i,j]
                                    object_remove = env.remove_object(i,j)                    #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                    env.board[i][j] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                elif len(target) == 0:                      #ถ้าไม่มี state ใน value_fn
                                    self.get_hash_state_winner_ended(env,state) #initial ใหม่
                                    target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ซึ่งต้องมีเท่านั้น
                                    if len(target) == 1:
                                        state_value = self.value_fn[target[0]][1]
                                        all_action[(1,i,j)] = state_value
                                        if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                            best_value = state_value
                                            action = [1,i,j]
                                        object_remove = env.remove_object(i,j)                    #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                        env.board[i][j] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                    else:
                                        raise Exception("Something Wrong With Hash in Take Action (Take Only)")
                                else:
                                    raise Exception("Something Wrong With Hash in Take Action (Take Only)")
                
                                

                            
                
                #ลองโยกหมากทั้งหมดที่โยกได้ ไปทุกช่องที่ไปได้           
                env.check_move(self.symbol)     #หาพิกัดของฝั่งตัวเอง ว่ามีหมากไหนลงอยู่บ้าง เก็บไว้ใน env.can_move
                moveable = env.can_move         #เปลี่ยนมาเก็บใน moveable
                for position in moveable:
                    if env.moveable_priority(position[0],position[1]) == True:  #ตำแหน่งที่เลือกมา สามารถ โยก ไป ตำแหน่งไหนได้บ้าง ในตัวแปร env.moveable
                        all_target = env.moveable                               # target = ตำแหน่งที่จะเอาไปวาง
                        for move_target in all_target:
                            size = env.check_size_top_object_on_board(position[0],position[1])  #หยิบหมากบนสุดของตำแหน่ง position
                            object_remove = env.remove_object(position[0],position[1])                    #ลดระดับ position
                            env.board[position[0]][position[1]] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position
                            if env.is_game_over() == True:                                                          #ถ้ามีผู้ชนะตอนที่ยกออก ให้ประมวลผลเลย
                                state = env.get_state()
                                target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ว่ามีไหม บรรทัดนี้ target คือ index ของ state ใน value_fn
                                if len(target) == 1:                        #ถ้ามี state ใน value_fn
                                    state_value = self.value_fn[target[0]][1]
                                    all_action[(position[0],position[1],move_target[0],move_target[1])] = state_value
                                    if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                        best_value = state_value
                                        action = [position[0],position[1],move_target[0],move_target[1]]
                                elif len(target) == 0:                      #ถ้าไม่มี state ใน value_fn
                                    self.get_hash_state_winner_ended(env,state) #initial ใหม่
                                    target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ซึ่งต้องมีเท่านั้น
                                    if len(target) == 1:
                                        state_value = self.value_fn[target[0]][1]
                                        all_action[(position[0],position[1],move_target[0],move_target[1])] = state_value
                                        if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                            best_value = state_value
                                            action = [position[0],position[1],move_target[0],move_target[1]]
                                    else:
                                        raise Exception("Something Wrong With Hash in Take Action (Move Only)")
                                else:
                                    raise Exception("Something Wrong With Hash in Take Action (Move Only)")
                                
                                object_added = env.add_object(self.symbol,size,position[0],position[1])  #เพิ่มระดับ position ที่ลดไป เพื่อคืนด่าเดิม                                    
                                env.board[position[0]][position[1]] = env.convert_Text_to_Number(object_added)    #เพิ่มระดับ position ที่ลดไป เพื่อคืนด่าเดิม  

                                
                            else:       #ถ้าไม่มีให้เอาหมากไปวางก่อน แล้วค่อยประมวลผล
                                object_added = env.add_object(self.symbol,size,move_target[0],move_target[1])  #เพิ่มระดับ move_target                                      
                                env.board[move_target[0]][move_target[1]] = env.convert_Text_to_Number(object_added)    #เพิ่มระดับ move_target
                                state = env.get_state()
                                target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ว่ามีไหม บรรทัดนี้ target คือ index ของ state ใน value_fn
                                if len(target) == 1:                        #ถ้ามี state ใน value_fn
                                    state_value = self.value_fn[target[0]][1]
                                    all_action[(position[0],position[1],move_target[0],move_target[1])] = state_value
                                    if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                        best_value = state_value
                                        action = [position[0],position[1],move_target[0],move_target[1]]
                                elif len(target) == 0:                      #ถ้าไม่มี state ใน value_fn
                                    self.get_hash_state_winner_ended(env,state) #initial ใหม่
                                    target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ซึ่งต้องมีเท่านั้น
                                    if len(target) == 1:
                                        state_value = self.value_fn[target[0]][1]
                                        all_action[(position[0],position[1],move_target[0],move_target[1])] = state_value
                                        if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                            best_value = state_value
                                            action = [position[0],position[1],move_target[0],move_target[1]]
                                    else:
                                        raise Exception("Something Wrong With Hash in Take Action (Move Only)")
                                else:
                                    raise Exception("Something Wrong With Hash in Take Action (Move Only)")
                                
                                object_added = env.add_object(self.symbol,size,position[0],position[1])  #เพิ่มระดับ position ที่ลดไป เพื่อคืนด่าเดิม                                    
                                env.board[position[0]][position[1]] = env.convert_Text_to_Number(object_added)    #เพิ่มระดับ position ที่ลดไป เพื่อคืนด่าเดิม     
                                object_remove = env.remove_object(move_target[0],move_target[1])                    #ลดระดับ move_target ที่เพิ่มมา เพื่อคืนค่าเดิม
                                env.board[move_target[0]][move_target[1]] = env.convert_Text_to_Number(object_remove)   #ลดระดับ move_target ที่เพิ่มมา เพื่อคืนค่าเดิม
                                    

            
            elif can_take == True and can_move == False:            #ถ้าลงหมากได้อย่างเดียว
                if env.check_big(self.symbol) == True :
                    picked_symbol = 3
                    size = "Big"
                    for i in range(3):
                        for j in range(3):
                            priority = env.priority(picked_symbol,i,j)
                            if priority == True:
                                object_added = env.add_object(self.symbol,size,i,j)         #ทดลองลงหมากใหญ่ ในทุกตำแหน่งที่ลงได้
                                env.board[i][j] = env.convert_Text_to_Number(object_added)
                                state = env.get_state()
                                target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ว่ามีไหม บรรทัดนี้ target คือ index ของ state ใน value_fn
                                if len(target) == 1:                        #ถ้ามี state ใน value_fn
                                    state_value = self.value_fn[target[0]][1]
                                    all_action[(3,i,j)] = state_value
                                    if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                        best_value = state_value
                                        action = [3,i,j]
                                    object_remove = env.remove_object(i,j)                    #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                    env.board[i][j] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                elif len(target) == 0:                      #ถ้าไม่มี state ใน value_fn
                                    self.get_hash_state_winner_ended(env,state) #initial ใหม่
                                    target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ซึ่งต้องมีเท่านั้น
                                    if len(target) == 1:
                                        state_value = self.value_fn[target[0]][1]
                                        all_action[(3,i,j)] = state_value
                                        if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                            best_value = state_value
                                            action = [3,i,j]
                                        object_remove = env.remove_object(i,j)                    #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                        env.board[i][j] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                    else:
                                        raise Exception("Something Wrong With Hash in Take Action")
                                else:
                                    raise Exception("Something Wrong With Hash in Take Action")
                                

                          

                if env.check_medium(self.symbol) == True :
                    picked_symbol = 2
                    size = "Medium"
                    for i in range(3):
                        for j in range(3):
                            priority = env.priority(picked_symbol,i,j)
                            if priority == True:
                                object_added = env.add_object(self.symbol,size,i,j)         #ทดลองลงหมากกลาง ในทุกตำแหน่งที่ลงได้
                                env.board[i][j] = env.convert_Text_to_Number(object_added)
                                state = env.get_state()
                                target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ว่ามีไหม บรรทัดนี้ target คือ index ของ state ใน value_fn
                                if len(target) == 1:                        #ถ้ามี state ใน value_fn
                                    state_value = self.value_fn[target[0]][1]
                                    all_action[(2,i,j)] = state_value
                                    if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                        best_value = state_value
                                        action = [2,i,j]
                                    object_remove = env.remove_object(i,j)                    #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                    env.board[i][j] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                elif len(target) == 0:                      #ถ้าไม่มี state ใน value_fn
                                    self.get_hash_state_winner_ended(env,state) #initial ใหม่
                                    target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ซึ่งต้องมีเท่านั้น
                                    if len(target) == 1:
                                        state_value = self.value_fn[target[0]][1]
                                        all_action[(2,i,j)] = state_value
                                        if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                            best_value = state_value
                                            action = [2,i,j]
                                        object_remove = env.remove_object(i,j)                    #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                        env.board[i][j] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                    else:
                                        raise Exception("Something Wrong With Hash in Take Action")
                                else:
                                    raise Exception("Something Wrong With Hash in Take Action")
                                

                      
                if env.check_small(self.symbol) == True :
                    picked_symbol = 1
                    size = "Small"
                    for i in range(3):
                        for j in range(3):
                            priority = env.priority(picked_symbol,i,j)
                            if priority == True:
                                object_added = env.add_object(self.symbol,size,i,j)         #ทดลองลงหมากเล็ก ในทุกตำแหน่งที่ลงได้
                                env.board[i][j] = env.convert_Text_to_Number(object_added)
                                state = env.get_state()
                                target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ว่ามีไหม บรรทัดนี้ target คือ index ของ state ใน value_fn
                                if len(target) == 1:                        #ถ้ามี state ใน value_fn
                                    state_value = self.value_fn[target[0]][1]
                                    all_action[(1,i,j)] = state_value
                                    if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                        best_value = state_value
                                        action = [1,i,j]
                                    object_remove = env.remove_object(i,j)                    #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                    env.board[i][j] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                elif len(target) == 0:                      #ถ้าไม่มี state ใน value_fn
                                    self.get_hash_state_winner_ended(env,state) #initial ใหม่
                                    target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ซึ่งต้องมีเท่านั้น
                                    if len(target) == 1:
                                        state_value = self.value_fn[target[0]][1]
                                        all_action[(1,i,j)] = state_value
                                        if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                            best_value = state_value
                                            action = [1,i,j]
                                        object_remove = env.remove_object(i,j)                    #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                        env.board[i][j] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position เพื่อคืนค่าให้เป็นเหมือนเดิม
                                    else:
                                        raise Exception("Something Wrong With Hash in Take Action (Take Only)")
                                else:
                                    raise Exception("Something Wrong With Hash in Take Action (Take Only)")
                                
                
            
            elif can_take == False and can_move == True:                #ถ้าโยกหมากได้อย่างเดียว
                env.check_move(self.symbol)     #หาพิกัดของฝั่งตัวเอง ว่ามีหมากไหนลงอยู่บ้าง เก็บไว้ใน env.can_move
                moveable = env.can_move         #เปลี่ยนมาเก็บใน moveable
                for position in moveable:
                    if env.moveable_priority(position[0],position[1]) == True:  #ตำแหน่งที่เลือกมา สามารถ โยก ไป ตำแหน่งไหนได้บ้าง ในตัวแปร env.moveable
                        all_target = env.moveable                               # target = ตำแหน่งที่จะเอาไปวาง
                        for move_target in all_target:
                            size = env.check_size_top_object_on_board(position[0],position[1])  #หยิบหมากบนสุดของตำแหน่ง position
                            object_remove = env.remove_object(position[0],position[1])                    #ลดระดับ position
                            env.board[position[0]][position[1]] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position
                            if env.is_game_over() == True:                                                          #ถ้ามีผู้ชนะตอนที่ยกออก ให้ประมวลผลเลย
                                state = env.get_state()
                                target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ว่ามีไหม บรรทัดนี้ target คือ index ของ state ใน value_fn
                                if len(target) == 1:                        #ถ้ามี state ใน value_fn
                                    state_value = self.value_fn[target[0]][1]
                                    all_action[(position[0],position[1],move_target[0],move_target[1])] = state_value
                                    if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                        best_value = state_value
                                        action = [position[0],position[1],move_target[0],move_target[1]]
                                elif len(target) == 0:                      #ถ้าไม่มี state ใน value_fn
                                    self.get_hash_state_winner_ended(env,state) #initial ใหม่
                                    target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ซึ่งต้องมีเท่านั้น
                                    if len(target) == 1:
                                        state_value = self.value_fn[target[0]][1]
                                        all_action[(position[0],position[1],move_target[0],move_target[1])] = state_value
                                        if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                            best_value = state_value
                                            action = [position[0],position[1],move_target[0],move_target[1]]
                                    else:
                                        raise Exception("Something Wrong With Hash in Take Action (Move Only)")
                                else:
                                    raise Exception("Something Wrong With Hash in Take Action (Move Only)")
                                
                                object_added = env.add_object(self.symbol,size,position[0],position[1])  #เพิ่มระดับ position ที่ลดไป เพื่อคืนด่าเดิม                                    
                                env.board[position[0]][position[1]] = env.convert_Text_to_Number(object_added)    #เพิ่มระดับ position ที่ลดไป เพื่อคืนด่าเดิม  

                                
                            else:       #ถ้าไม่มีให้เอาหมากไปวางก่อน แล้วค่อยประมวลผล
                                object_added = env.add_object(self.symbol,size,move_target[0],move_target[1])  #เพิ่มระดับ move_target                                      
                                env.board[move_target[0]][move_target[1]] = env.convert_Text_to_Number(object_added)    #เพิ่มระดับ move_target
                                state = env.get_state()
                                target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ว่ามีไหม บรรทัดนี้ target คือ index ของ state ใน value_fn
                                if len(target) == 1:                        #ถ้ามี state ใน value_fn
                                    state_value = self.value_fn[target[0]][1]
                                    all_action[(position[0],position[1],move_target[0],move_target[1])] = state_value
                                    if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                        best_value = state_value
                                        action = [position[0],position[1],move_target[0],move_target[1]]
                                elif len(target) == 0:                      #ถ้าไม่มี state ใน value_fn
                                    self.get_hash_state_winner_ended(env,state) #initial ใหม่
                                    target = [i for i,x in enumerate(self.value_fn) if x[0]==state]   #หา state ใน value_fn ซึ่งต้องมีเท่านั้น
                                    if len(target) == 1:
                                        state_value = self.value_fn[target[0]][1]
                                        all_action[(position[0],position[1],move_target[0],move_target[1])] = state_value
                                        if state_value > best_value:    #เก็บค่า value ของ state ที่ดีที่สุดไว้
                                            best_value = state_value
                                            action = [position[0],position[1],move_target[0],move_target[1]]
                                    else:
                                        raise Exception("Something Wrong With Hash in Take Action (Move Only)")
                                else:
                                    raise Exception("Something Wrong With Hash in Take Action (Move Only)")
                                
                                object_added = env.add_object(self.symbol,size,position[0],position[1])  #เพิ่มระดับ position ที่ลดไป เพื่อคืนด่าเดิม                                    
                                env.board[position[0]][position[1]] = env.convert_Text_to_Number(object_added)    #เพิ่มระดับ position ที่ลดไป เพื่อคืนด่าเดิม     
                                object_remove = env.remove_object(move_target[0],move_target[1])                    #ลดระดับ move_target ที่เพิ่มมา เพื่อคืนค่าเดิม
                                env.board[move_target[0]][move_target[1]] = env.convert_Text_to_Number(object_remove)   #ลดระดับ move_target ที่เพิ่มมา เพื่อคืนค่าเดิม                                                       
            else:
                raise Exception("can't take and can't move it's impossible")
            
            if self.print_value_fn:
                #ถ้าอยากทำให้มันเอาแค่ 5 อันดับ อันที่ดีที่สุดค่อยมาทำวันหลังนะจ๊ะ ตอนนี้เอาแบบแสดงทั้งหมดไปก่อน
                print("All action = "+str(len(all_action))+" action")
                for i in all_action:
                    if len(i) == 3:
                        if i[0] == 1:
                            print("Action is take Small to "+str(i[1])+","+str(i[2])+" Value is "+str(all_action[i]))
                        elif i[0] == 2:
                            print("Action is take Medium to "+str(i[1])+","+str(i[2])+" Value is "+str(all_action[i]))
                        elif i[0] == 3:
                            print("Action is take Big to "+str(i[1])+","+str(i[2])+" Value is "+str(all_action[i]))
                        else:
                            raise Exception("Something Wrong With all_action in Take Action")
                    elif len(i) == 4:
                        print("Move object from "+ str(i[0])+ ","+str(i[1])+" to "+str(i[2])+","+str(i[3])+" Value is "+str(all_action[i]))
                    else:
                        raise Exception("Something Wrong With all_action in Take Action")
            
            #หลักจากคิดทุกรูปแบบการเดินเสร็จแล้ว ให้นำ action ที่ดีที่สุด มาลงในกระดาน    
            
            if len(action) ==3: #ถ้าเป็น 3 หมายความว่า หยิบหมากมาลง (Take)
                if action[0] == 1:
                    size = "Small"
                    if self.symbol == "x":      #ลดหมาก
                        env.x_small -= 1
                    elif self.symbol == "o":
                        env.o_small -=1
                elif action[0] == 2:
                    size = "Medium"
                    if self.symbol == "x":      #ลดหมาก
                        env.x_medium -= 1
                    elif self.symbol == "o":
                        env.o_medium -=1
                elif action[0] == 3:
                    size = "Big"
                    if self.symbol == "x":      #ลดหมาก
                        env.x_big -= 1
                    elif self.symbol == "o":
                        env.o_big -=1
                else:
                    raise Exception("Something Wrong in Variable Action")
                
                object_added = env.add_object(self.symbol,size,action[1],action[2])                 #ลงหมากตามคำสั่งของ action               
                env.board[action[1]][action[2]] = env.convert_Text_to_Number(object_added)          #ลงหมากตามคำสั่งของ action   
            



            elif len(action) == 4: #ถ้าเป็น 4 หมายความว่า โยกหมากไปช่องอื่น (Move)
                picked_symbol = env.check_size_top_object_on_board(action[0],action[1])   #หยิบหมากบนสุดของตำแหน่ง move_position
                object_remove = env.remove_object(action[0],action[1])                    #ลดระดับ position
                env.board[action[0]][action[1]] = env.convert_Text_to_Number(object_remove)   #ลดระดับ position

                if env.is_game_over() == True:                                                          #ถ้ามีผู้ชนะตอนที่ยกออก จะจบการทำงานทันที
                    return 0
                
                object_added = env.add_object(self.symbol,picked_symbol,action[2],action[3])  #เพิ่มระดับ target                                                         
                env.board[action[2]][action[3]] = env.convert_Text_to_Number(object_added)    
            
            else:
                raise Exception("Something Wrong in Variable Action")

            return action
            
            

          
            # if self.print_value_fn:
            #     print('Value Function (Agent) :')
            #     for i in range(3):
            #         print('----------------------')
            #         for j in range(3):
            #             print('| ', end='')
            #             if env.is_empty(i, j):
            #                 print("%.2f " % pos2value[(i,j)], end="")
            #             else:
            #                 if env.board[i, j] == env.x:
            #                     print(' x   ', end='')
            #                 elif env.board[i, j] == env.o:
            #                     print(' o   ', end='')
            #                 else:
            #                     print('    ', end='')
            #         print('|')
            #     print('----------------------')
    
    def convert_base10_to_base27 (self,decimal):
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
    
    def initial(self,state):                        #search state ที่ต้องการ จาก result มาให้ราคา initial ของ state นั้นๆ แล้วเก็บใน value_fn
        target = [i for i,x in enumerate(self.results) if x[0]==state]
        if self.symbol == 'x':
            if self.results[target[0]][2]:
                if self.results[target[0]][1] == 1:
                    v = 1
                else:
                    v = 0
            else:
                v = 0.5
            
            self.value_fn.append((state,v))

            return self.value_fn

        elif self.symbol == 'o':
            if self.results[target[0]][2]:
                if self.results[target[0]][1] == 2:
                    v = 1
                else:
                    v = 0
            else:
                v = 0.5
            
            self.value_fn.append((state,v))

            return self.value_fn
        else:
            raise Exception("Symbol Is Wrong")
            

    def get_hash_state_winner_ended(self,env,state):           #เปรียบเสมือนการเอาไข่มาวางในแผงพร้อมใส่สรรพคุณของไข่ 
        base27 = self.convert_base10_to_base27(state)
        reverse_base27 = base27[::-1]
        count = 0
        for i in range(3):
            for j in range(3):
                if reverse_base27[count] == '0':
                    env.board[i][j] = 0
                elif reverse_base27[count] == '1':
                    env.board[i][j] = 1
                elif reverse_base27[count] == '2':
                    env.board[i][j] = 2
                elif reverse_base27[count] == '3':
                    env.board[i][j] = 3
                elif reverse_base27[count] == '4':
                    env.board[i][j] = 4
                elif reverse_base27[count] == '5':
                    env.board[i][j] = 5
                elif reverse_base27[count] == '6':
                    env.board[i][j] = 6
                elif reverse_base27[count] == '7':
                    env.board[i][j] = 7
                elif reverse_base27[count] == '8':
                    env.board[i][j] = 8
                elif reverse_base27[count] == '9':
                    env.board[i][j] = 9
                elif reverse_base27[count] == 'A':
                    env.board[i][j] = 10
                elif reverse_base27[count] == 'B':
                    env.board[i][j] = 11
                elif reverse_base27[count] == 'C':
                    env.board[i][j] = 12
                elif reverse_base27[count] == 'D':
                    env.board[i][j] = 13
                elif reverse_base27[count] == 'E':
                    env.board[i][j] = 14
                elif reverse_base27[count] == 'F':
                    env.board[i][j] = 15
                elif reverse_base27[count] == 'G':
                    env.board[i][j] = 16
                elif reverse_base27[count] == 'H':
                    env.board[i][j] = 17
                elif reverse_base27[count] == 'I':
                    env.board[i][j] = 18
                elif reverse_base27[count] == 'J':
                    env.board[i][j] = 19
                elif reverse_base27[count] == 'K':
                    env.board[i][j] = 20
                elif reverse_base27[count] == 'L':
                    env.board[i][j] = 21
                elif reverse_base27[count] == 'M':
                    env.board[i][j] = 22
                elif reverse_base27[count] == 'N':
                    env.board[i][j] = 23
                elif reverse_base27[count] == 'O':
                    env.board[i][j] = 24
                elif reverse_base27[count] == 'P':
                    env.board[i][j] = 25
                elif reverse_base27[count] == 'Q':
                    env.board[i][j] = 26
                count+=1
        get_state = env.get_state()
        ended = env.is_game_over()
        winner = env.winner
        self.results.append((get_state, winner, ended))

        self.initial(state)


        #env.board = np.array([[0,0,0],[0,0,0],[0,0,0]]) 

        return self.results

# env =Environment()
# np.random.seed(1)
# a= Agent()
# a.set_eps(0)
# a.set_symbol("x")
# a.set_print_value_fn(True)
# env.print_board()
# print(a.take_action(env))
# print(a.value_fn)
# print(a.results)


# b= Human()
# #b.set_eps(2)
# b.set_symbol("o")

# env =Environment()
# current_player = None  
# while not env.is_game_over():
# #for i in range(20):
#     env.print_board()
       
#     if current_player == a:
#         print("O Turn")
#         current_player = b
#     else:
#         print("X Turn")
#         current_player = a

#     current_player.take_action(env)
    
    
#     if env.is_game_over() == True:                                                    
#         env.print_board()
#         print(env.winner)
#         break
    
# print("Done")



# เอาไปรวมกับเกม
