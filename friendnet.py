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

if __name__ == "__main__":

    with open("network.json", "r") as read_file:
        network = json.load(read_file)
        fnet = FriendNet(network)
    
    print(fnet.userExists("Molecule man"))
    