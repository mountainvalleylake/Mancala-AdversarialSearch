import copy
W1,W2,W3,W4 = 1,1,2,3
#the board state of the GameBoard class
                  #will be updated with each move
#2 player game
# Goal, 4,4,4,4,4,4, X
# X   , 4,4,4,4,4,4, Goal
class GameBoard:
    def __init__(self, bucket_count):
        self.bucket_size = bucket_count + 2 #1 is for each player's goal
        self.player_1_i = 0
        self.player_1_j = 0 # board[0][0] = player_1_deposite
        self.player_2_i = 1 # board[1][7] = player_2_deposite
        self.player_2_j = bucket_count+1 #7
        self.parents_move_i = -1 #which move of parent results me
        self.parents_move_j = -1
        self.child_move_i = -1 #which move of mine results the best child
        self.child_move_j = -1
        self.board = [[],[]] #its board state
        self.cost = 0 #cost by parent's that move
        self.extra_turn = 0 #has this state gained any extra move
        self.captured = [0,0]#how many extras it has captured
    def Init_Board(self,stones): #parameter stones is stone in each bucket
        for i in range(0,2):
            for j in range(0,self.bucket_size):
                if ((i==self.player_1_i and j==self.player_1_j)or(i==self.player_2_i and j==self.player_2_j)):
                    self.board[i].append(0)
                elif((i==self.player_1_i and j==self.player_2_j) or(i==self.player_2_i and j==self.player_1_j)):
                    self.board[i].append('X')
                else:
                    self.board[i].append(stones)
    def Side_1_Count(self):
        count = 0
        for i in range(1,7):
            count += self.board[0][i]
        return count
    def Sweep(self,side):
        count = 0
        if side == 1:
            for i in range(1,7):
                count += self.board[0][i]
                self.board[0][i]=0
            self.board[self.player_1_i][self.player_1_j] += count
        if side == 2:
            for i in range(1,7):
                count += self.board[1][i]
                self.board[1][i]=0
            self.board[self.player_2_i][self.player_2_j] += count


    def Side_2_Count(self):
        count = 0
        for i in range(1,7):
            count += self.board[1][i]
        return count

    def Set_Move(self,i,j):
        self.move_i = i
        self.move_j = j

    def Print_Board(self):
        for i in range(0,2):
            print('Player ',i+1,':= ', self.board[i])

    def Set_Cost(self,given_cost):
        self.cost = given_cost
    def Get_Cost(self):
        return self.cost
    def Get_Cost_Heuristic1(self,player):
        if player == 1:
            self.cost = self.board[self.player_1_i][self.player_1_j] \
                   - self.board[self.player_2_i][self.player_2_j]
        else:
            self.cost = self.board[self.player_2_i][self.player_2_j] \
                   - self.board[self.player_1_i][self.player_1_j]

    def Get_Cost_Heuristic2(self,player):
        global W1,W2
        if player == 1:
            self.cost = W1* self.board[self.player_1_i][self.player_1_j] \
                   - W2* self.board[self.player_2_i][self.player_2_j]
        else:
            self.cost = W2* self.board[self.player_2_i][self.player_2_j] \
                   - W1* self.board[self.player_1_i][self.player_1_j]

    def Get_Cost_Heuristic3(self,player):
        global W1,W2,W3
        if player == 1:
            self.cost = W1* self.board[self.player_1_i][self.player_1_j] \
                   - W2* self.board[self.player_2_i][self.player_2_j]\
                   + W3* self.extra_turn
        else:
            self.cost = W2* self.board[self.player_2_i][self.player_2_j] \
                   - W1* self.board[self.player_1_i][self.player_1_j] \
                   + W3* self.extra_turn

    def Get_Cost_Heuristic4(self,player):
        global W1,W2,W3,W4
        if player == 1:
            self.cost = W1* self.board[self.player_1_i][self.player_1_j] \
                   - W2* self.board[self.player_2_i][self.player_2_j] \
                   + W3 * self.extra_turn + W4* (self.captured[0]-self.captured[1])
        else:
            self.cost = W2* self.board[self.player_2_i][self.player_2_j] \
                   - W1* self.board[self.player_1_i][self.player_1_j] \
                   + W3* self.extra_turn + W4* (self.captured[1]-self.captured[0])


def Decision(state,computer,human):
    player_turn = human
    initial = state
    move = initial
    p1 = computer
    p2 = human
    while(player_turn != -1):
        if(player_turn==1):
            if (move.Side_1_Count() == 0 and move.Side_2_Count() != 0):
                player_turn = 2
                continue
            elif (move.Side_2_Count() == 0 and move.Side_1_Count() != 0):
                player_turn = -1
                move.Sweep(1)
                move.Print_Board()
                break
            s = Maximize(initial,p1,p2,4,-9999,9999)
            move = Generate_Board(s,p1,s.child_move_i,s.child_move_j)
            print('Player ', player_turn, ' turn')
            move.Print_Board()
            print('Move is ',move.child_move_i,',',move.child_move_j)
            print('Extra turn ',move.extra_turn,' Captured ',move.captured)
            if move.extra_turn==1:
                player_turn = 1
                move.extra_turn = 0
            else:
                player_turn = 2
        elif(player_turn==2):
            if (move.Side_2_Count() == 0 and move.Side_1_Count() != 0):
                player_turn = 1
                continue
            elif (move.Side_1_Count() == 0 and move.Side_2_Count() != 0):
                player_turn = -1
                move.Sweep(2)
                move.Print_Board()
                break
            child_move_i = human - 1
            child_move_j = int(input("j index: "))
            move = Generate_Board(initial, p2, child_move_i, child_move_j)
            print('Player ', player_turn, ' turn')
            move.Print_Board()
            print('Move is ', child_move_i, ',', child_move_j)
            print('Extra turn ', move.extra_turn, ' Captured ', move.captured)
            if move.extra_turn == 1:
                player_turn = 2
                move.extra_turn = 0
            else:
                player_turn = 1
        initial = move
    if(initial.board[initial.player_1_i][initial.player_1_j] > initial.board[initial.player_2_i][initial.player_2_j]):
        winner = 1
        initial.Print_Board()
        print('Player 1 Wins')
    elif(initial.board[initial.player_1_i][initial.player_1_j] < initial.board[initial.player_2_i][initial.player_2_j]):
        winner = 2
        initial.Print_Board()
        print('Player 2 Wins')
    else:
        winner = 0
        initial.Print_Board()
        print('Draw')
    return winner

def Maximize(state,current_player,opposite_player,depth,alpha,beta):
    if depth == 0:
        state.Get_Cost_Heuristic4(current_player)
        return state
    depth -= 1
    #max = None
    return_child = []
    state.Set_Cost(-99999)
    max_child = Generate_Child(state,current_player)
    for child in max_child:
        child.Set_Cost(-9999) #which is inf
        return_child.append(Minimize(child,opposite_player,current_player,depth,alpha,beta))
    for child in return_child:
        if state.Get_Cost() <= child.Get_Cost():
            state.Set_Cost(child.Get_Cost())
            state.child_move_i = child.parents_move_i
            state.child_move_j = child.parents_move_j
            #max = copy.deepcopy(child)
        if state.Get_Cost() >= beta:
            break
        if state.Get_Cost() > alpha:
            alpha = state.Get_Cost()
    return_child.clear()
    max_child.clear()
    return state

def Minimize(state,current_player,opposite_player,depth,alpha,beta):
    if depth == 0:
        state.Get_Cost_Heuristic4(current_player)
        return state
    depth -= 1
    #min = None
    return_child = []
    state.Set_Cost(9999)
    min_child = Generate_Child(state,current_player)
    for child in min_child:
        child.Set_Cost(9999)
        return_child.append(Maximize(child,opposite_player,current_player,depth,alpha,beta))
    for child in return_child:
        if state.Get_Cost() >= child.Get_Cost():
            state.Set_Cost(child.Get_Cost())
            state.child_move_i = child.parents_move_i
            state.child_move_j = child.parents_move_j
            #min = copy.deepcopy(child)
        if state.Get_Cost() <= alpha:
            break
        if state.Get_Cost() < beta:
            beta = state.Get_Cost()
    return_child.clear()
    min_child.clear()
    return state

def Generate_Board(state,player,movei,movej):
    if player == 1:
        goal_i = 0
        goal_j = 0
        opp_i = 1
        opp_j = 7
    else:
        goal_i = 1
        goal_j = 7
        opp_i = 0
        opp_j = 0
    stones = state.board[movei][movej]
    next_i = movei
    next_j = movej
    if stones ==0:
        return state
    child = copy.deepcopy(state)
    child.board[next_i][next_j] = 0
    while stones > 0:
        if next_i == 0:
            if next_j > 0:
                next_j -= 1
            elif next_j == 0:  # (0,0)
                next_i = 1
                next_j = 1
        elif next_i == 1:
            if next_j < 7:
                next_j += 1
            elif next_j == 7:  # (1,7)
                next_i = 0
                next_j = 6
        if (next_i != opp_i or next_j != opp_j):
            child.board[next_i][next_j] += 1
            stones -= 1
            if stones == 0:  # where the last stone is going
                if (next_i == goal_i and next_j == goal_j):
                    # last stone in the goal post
                    child.extra_turn = 1
                    child.captured[goal_i] += 1
                elif (next_j != goal_j) and (child.board[next_i][next_j] == 1) and (next_i == goal_i):
                    # last stone in player's empty non-goal hole
                    child.captured[goal_i] = child.captured[goal_i] + child.board[next_i][next_j] + child.board[opp_i][next_j]
                    child.board[goal_i][goal_j] = child.board[goal_i][goal_j] + child.board[next_i][next_j] + \
                                                  child.board[opp_i][next_j]
                    child.board[next_i][next_j] = 0
                    child.board[opp_i][next_j] = 0
            else:
                if next_i == goal_i and next_j == goal_j:
                    child.captured[goal_i] += 1
    return child

def Generate_Child(state,player):
    q = []
    if player == 1:
        i = 0
        goal_i = 0
        goal_j = 0
        opp_i = 1
        opp_j = 7
    else:
        i = 1
        goal_i = 1
        goal_j = 7
        opp_i = 0
        opp_j = 0
    for j in range(1,7):
        stones = state.board[i][j]
        next_i = i
        next_j = j
        if stones == 0:
            continue
        child = copy.deepcopy(state)
        child.board[next_i][next_j] = 0
        child.parents_move_i = i
        child.parents_move_j = j
        while stones > 0:
            if next_i == 0:
                if next_j > 0:
                    next_j -= 1
                elif next_j == 0: #(0,0)
                    next_i = 1
                    next_j = 1
            elif next_i == 1:
                if next_j < 7:
                    next_j += 1
                elif next_j == 7: #(1,7)
                    next_i = 0
                    next_j = 6
            if (next_i!=opp_i or next_j!=opp_j):
                child.board[next_i][next_j] += 1
                stones -= 1
                if stones == 0: #where the last stone is going
                    if (next_i==goal_i and next_j==goal_j):
                       #last stone in the goal post
                        child.extra_turn = 1
                        child.captured[goal_i] += 1
                    elif (next_j != goal_j) and (child.board[next_i][next_j] == 1)and(next_i==goal_i):
                        #last stone in player's empty non-goal hole
                        child.captured[goal_i] = child.captured[goal_i] + child.board[next_i][next_j] + child.board[opp_i][next_j]
                        child.board[goal_i][goal_j] = child.board[goal_i][goal_j] + child.board[next_i][next_j] + child.board[opp_i][next_j]
                        child.board[next_i][next_j] = 0
                        child.board[opp_i][next_j] = 0
                else:
                    if next_i == goal_i and next_j == goal_j:
                        child.captured[goal_i] += 1
        #print(child.Print_Board())
        q.append(child)
    return q
def main():
    print('The Mancala Game\n')
    b = GameBoard(6)
    b.Init_Board(4)
    b.Print_Board()
    winner = Decision(b,1,2)
    '''winner1,winner2 = 0,0
    #player 1 has first turn
    for i in range(1,51):
        winner1 = Decision(b,1,2)
    for j in range(1,51):
        winner2 = Decision(b,2,1)
    print('Player 1 wins ',winner1/100,' times')
    print('Player 2 wins', winner2/200,' times')'''
if __name__ == '__main__':
    main()