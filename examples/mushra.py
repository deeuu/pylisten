import pylisten

mushra = pylisten.parser.MUSHRA('example_data/mushra.json')
data = mushra.parse()

print(data)
