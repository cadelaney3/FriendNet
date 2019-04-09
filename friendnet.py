# Authors: Tyler Tiedt, Carlos Vasquez Baur, Chris Delaney
# FriendNet
# Best Friend Chain Algorithm: Dijkstra's Algorithm
# Killer features:
#   1. use knapsack algorithm to determine who to invite
#      to a party so that there is a high friend value with
#      a capacity on overall personality intensity
#   2. use stable marriage algorithm to figure out who
#      dances with who at the party
#
# *Floyd's algorithm to find shortest path for all vertices


import json
import math

with open("network.json", "r") as read_file:
    network = json.load(read_file)
    network = network['network']

class FriendNet:
    def __init__(self, network):
        self.network = network['network']
    '''
    def userGraph(self):
        print(len(self.network))
        #for i in range(len(self.network)):
    '''

    def userExists(self, username):
        for i in self.network:
            if username.lower() in i['name'].lower():
                print("{} does exist".format(username))
                return True
        print("{} does not exist".format(username))
        return False

    def userConnection(self, user1, user2):
        if self.userExists(user1) and self.userExists(user2):
            for i in self.network:
                if user1.lower() == i['name'].lower():
                    for friend in i['friends']:
                        if user2.lower() == friend['friendName'].lower():
                            print("Connection between {} and {} is: {}".format(user1, user2, friend['strength']))
                            return True
                    print("No connection between {} and {}.".format(user1, user2))
                    return False
        else:
            print("One or both of the users do not exists or have their name mispelled. Try again.")
            return False

    #def bestFriendChain(self, user1, user2):


if __name__ == "__main__":
    
    with open("network.json", "r") as read_file:
        network = json.load(read_file)
        fnet = FriendNet(network)
        #fnet.userGraph()
    
    while(True):
        print('\nWhat ya wanna do?')
        print('1. Check is user exist')
        print('2. Check connections between users')
        print('3. Exit')
        try:
            selection = input('> ')
            selection = int(selection)
            if(selection == 1):
                user = input('What user? ')
                fnet.userExists(user)
            elif(selection == 2):
                users = input('What users? (separated by a space) ')
                users = users.split()
                user1 = users[0]
                user2 = users[1]
                fnet.userConnection(user1, user2)
            elif(selection == 3):
                print('Bye! Ill miss you!')
                break
            else:
                print('ERROR')
        except Exception as e:
            print("Error: please enter an nonnegative integer value.")
            pass
    
