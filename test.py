import re
# import pandas as pd
#
# data = {'1': ['pivo', 'pivo2'], '2': ['car', 'car2']}
# df = pd.DataFrame.from_dict(data)
#
# filename = 'new.csv'
# df.to_csv(filename)

# word = 'cars".'
# print(word[0:len(word) - 2])

text = 'he said: "apple/car, is on the table".'
print(re.split(' |/', text))
#':|"|.| '