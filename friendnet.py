import json

with open("network.json", "r") as read_file:
    network = json.load(read_file)
    network = network['network']

# for i in network:
#     print(i['name'])
#     for friend in i['friends']:
#         print(friend['friendName'])

class FriendNet:
    def __init__(self, network):
        self.network = network['network']

    def userExists(self, username):
        for i in self.network:
            if username.lower() in i['name'].lower():
                return True
        return False

    def userConnection(self, user1, user2):
        if self.userExists(user1):
            for i in self.network:
                if user1.lower() == i['name'].lower():
                    for friend in i['friends']:
                        if user2.lower() == friend['friendName'].lower():
                            return friend['strength']
                    return -1
        else:
            return -1

if __name__ == "__main__":

    with open("network.json", "r") as read_file:
        network = json.load(read_file)
        fnet = FriendNet(network)
    while(True):
        print('What ya wanna do?')
        print('1. Check is user exist')
        print('2. Check connections between users')
        print('3. Exit')
        selection = input('> ')
        selection = int(selection)
        if(selection == 1):
            user = input('What user? ')
            print(fnet.userExists(user))
        elif(selection == 2):
            users = input('What users? (separated by a space)')
            users = users.split()
            user1 = users[0]
            user2 = users[1]
            #fnet.userConnection(user1, user2)
        elif(selection == 3):
            print('Bye! Ill miss you!')
            break
        else:
            print('ERROR')
