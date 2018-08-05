import pylisten

pick_one = pylisten.parser.PickTheBest('example_data/pickthebest.json')
data = pick_one.parse()

print(data)
