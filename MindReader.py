from pdbot import PDBot

give2 = 0
take1 = 1


alpha = 0.1            #learning rate
discount = 0.75         #discount factor

class MindReader(PDBot):
    def __init__(self):
        #initialise
        #tit-for-tat always starts with cooperation
        self.other_last_play = give2
        self.myplay = give2
        self.counter = 0                                # the numer of times init is called
        self.q = [[[0, 0], [0, 0]],[[0, 0], [0, 0]]]    # the Q function
                                                        # index x is my last play; index y is other's last play; index z is my next play

    # init is called every time a new game starts
    def init(self):
        self.counter += 1

        # reset the data if there is a new bot
        if self.counter > 5:
            self.counter = 0 
            self.other_last_play = give2
            self.myplay = give2
            self.q = [[[0, 0], [0, 0]],[[0, 0], [0, 0]]]

    #get_play is a function that takes no arguments
    #and returns one of the two strings "give 2" or "take 1" 
    #denoting the next play your agent will take in the game
    def get_play(self):
        # my current play is the last play
        self.my_last_play = self.myplay

        # choose the action with the highest Q[s, a]
        # the bot does tit for tat if the difference between two choices is too small
        if abs(self.q[self.my_last_play][self.other_last_play][take1] - self.q[self.my_last_play][self.other_last_play][give2]) < 0.01:
            self.myplay = self.other_last_play
        elif self.q[self.my_last_play][self.other_last_play][take1] < self.q[self.my_last_play][self.other_last_play][give2]:
            self.myplay = give2
        else:
            self.myplay = take1

        if (self.myplay == take1):
            return "take 1"
        else:
            return "give 2"


    #make_play is a function that takes a single string argument
    #that is either "give 2" or "take 1" denoting the opponent's
    #last play in the game    
    def make_play(self,opponent_play):
        # translate the opponent play to our representation
        if opponent_play == "give 2":
            oppoPlay = give2
        else:
            oppoPlay = take1

        # current status
        s = (self.my_last_play, self.other_last_play)

        # calculate the reward
        r = 0
        if self.myplay == take1:
            r += 1
        if oppoPlay == give2:
            r += 2

        #update the Q table
        self.q[s[0]][s[1]][self.myplay] = self.q[s[0]][s[1]][self.myplay] + alpha * (r + discount * findMaxExp((self.myplay, oppoPlay), self.q) - self.q[s[0]][s[1]][self.myplay])

        #store for next round
        self.other_last_play = oppoPlay

        

#return the highest expected reward
def findMaxExp(s, q):
    if q[s[0]][s[1]][0] >= q[s[0]][s[1]][1]:
        return q[s[0]][s[1]][0]
    else:
        return q[s[0]][s[1]][1]

        
    
