import json

with open("network.json", "r") as read_file:
    network = json.load(read_file)
    network = network['network']

for i in network:
    print(i['name'])
    for friend in i['friends']:
        print(friend['friendName'])
