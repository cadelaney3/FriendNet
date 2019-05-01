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
from collections import Counter
import numpy as np

with open("network.json", "r") as read_file:
    network = json.load(read_file)
    network = network['network']

class FriendNet:
    def __init__(self, network):
        self.network = network['network']
    
    def userGraph(self):
        graph = []
        isAFriend = False
        # k1 is an index, v1 is the value at that index
        for k1, v1 in enumerate(self.network):
            row = []
            for k2, v2 in enumerate(self.network):
                # graph distance is 0 for person to themself
                if k1 == k2:
                    row.append(0)
                else:
                    # iterate thru the friends v1
                    for v1_friend in v1['friends']:
                        # check to see if v2 is in the list of v1's friends
                        if v2['name'] == v1_friend['friendName']:
                            row.append(v1_friend['strength'])
                            isAFriend = True
                    # if v2 not in v1's friends list, connection is 0
                    if isAFriend == False:
                        row.append(0)
                isAFriend = False
            graph.append(row)
        
        return graph

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

    def printPath(self, P, j, endPath):
        if P[j] == -1:
            for k, v in enumerate(self.network):
                if k == j:
                    endPath.append(v['name'])
                    break
            return
        self.printPath(P, P[j], endPath)
        for k, v in enumerate(self.network):
            if k == j:
                endPath.append(v['name'])
                break
        return endPath

    def minD(self, D, num_v, inN):
        minimum = math.inf
        min_i = -1
        for v in range(0, num_v):
            if D[v] < minimum and v not in inN:
                minimum = D[v]
                min_i = v 
        
        return min_i

    def bestFriendChain(self, user1, user2):
        graph = self.userGraph()

        for i in range(len(graph)):
            for j in range(len(graph[i])):
                graph[i][j] = abs(graph[i][j] - 10)
                if graph[i][j] == 0:
                    graph[i][j] = 1

        src = None
        dest = None
        for k, v in enumerate(self.network):
            if user1 == v['name']:
                src = k
            if user2 == v['name']:
                dest = k

        if src == None:
            print("User1 does not exist")
            return False
        if dest == None:
            print("User2 does not exist")
            return False

        N = []
        D = [math.inf] * len(graph)
        path = [-1] * len(graph)
        inN = [-1] * len(graph)
        inN[src] = src
        N.append(src)
        
        for v in range(0, len(graph)):
            if graph[src][v] != 0:
                D[v] = graph[src][v]
            else:
                D[v] = math.inf
        D[src] = 0

        for i in range(0, len(graph)):
            w = self.minD(D, len(graph), inN)
            N.append(w)
            inN[w] = w

            for v in range(0, len(graph)):
                if graph[w][v] > 0 and v not in N and D[v] > D[w] + graph[w][v]:
                    D[v] = D[w] + graph[w][v]
                    path[v] = w
        
        array = [user1]
        chain = self.printPath(path, dest, array)

        if chain != None:
            for i in range(len(chain)):
                if i != len(chain) - 1:
                    print("{} => ".format(chain[i]), end='')
                else:
                    print(chain[i])
        else:
            if graph[src][dest] == 0:
                print("There is no chain between {} and {}.".format(user1, user2))
                return False
            else:
                print(user1, " => ", user2)

        return True

    def knapsackItems(self):
        values = []
        for k, v in enumerate(self.network):
            values.append([v['intensity'], v['maintenance']])
        return values

    def f(self, i, j, items, F):
        if F[i][j] < 0:
            value = 0
            if j < items[i-1][0]:
                value = self.f(i-1, j, items, F)
            else:
                value = max(self.f(i-1, j, items, F), items[i-1][1]+self.f(i-1, j-items[i-1][0], items, F))

            F[i][j] = value
        return F[i][j]

    # this function based on https://beckernick.github.io/dynamic-programming-knapsack
    def getItemsUsed(self, F, items, W, num_items):
        items_taken = np.empty(num_items).astype(str)
        remaining_capacity = W
        for i in range(len(F)-1, 0, -1):
            if F[i][remaining_capacity] != F[i-1][remaining_capacity]:
                items_taken[i-1] = 'Chosen'
                weight = items[i-1][0]
                remaining_capacity = remaining_capacity - weight
            else:
                items_taken[i-1] = 'Not Chosen'
        return np.array(items)[np.where(items_taken == 'Chosen')[0], :]

    def bestParty(self, max_weight):
        items = self.knapsackItems()
        num_items = len(items)
        F = []
        for m in range(len(items)+1):
            if m == 0:
                F.append([0]*(max_weight+1))
            else:
                F.append([-1]*(max_weight+1))
                F[m][0] = 0
        self.f(len(F)-1, max_weight, items, F)

        items_used = self.getItemsUsed(F, items, max_weight, len(items)).tolist()

        print("Your perfect party includes: ", end='')
        for item in items_used:
            for k, v in enumerate(self.network):
                if item[0] == v['intensity'] and item[1] == v['maintenance']:
                   print(v['name'], " ", end='')
        print()


if __name__ == "__main__":
    
    with open("network.json", "r") as read_file:
        network = json.load(read_file)
        fnet = FriendNet(network)
        fnet.doF(20)
        #print(fnet.knapsckItems())
        #graph = fnet.userGraph()
        #dist = fnet.bestFriendChain("Chris", "Janene")
        # path = dist[2]
        # print("destination\t | \tlink")
        # print("-" * 30)
        # for k in range(0, len(graph)):
        #     print(k, "\t\t |  ", end="")
        #     fnet.printPath(path, k)
        #     print()

    '''
    while(True):
        print('\nWhat ya wanna do?')
        print('1. Check if user exist')
        print('2. Check connections between users')
        print('3. Find best friend chain between users')
        print('4. Throw the best party')
        print('5. Exit')
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
                users = input('What users? (separated by a space) ')
                users = users.split()
                user1 = users[0]
                user2 = users[1]
                fnet.bestFriendChain(user1, user2)
            elif(selection == 4):
                intensity = input('What type of party? [0 (mega chill)- 100 (riot)] ')
                maintenance = input(')
            elif(selection == 5):
                print('Bye! Ill miss you!')
                break
            else:
                print('ERROR')
        except Exception as e:
            print(e)
            print("Error: Bad input. Please enter an nonnegative integer value.")
            pass
    '''    
