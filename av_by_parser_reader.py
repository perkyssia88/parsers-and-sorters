import csv
import json

# read from csv
with open("av.csv", encoding="utf-8") as csv_data:
    reader = csv.reader(csv_data, delimiter=";")
    for row in reader:
        print(row)
        # for value in row:
        #     print(value)

# # read from json
# with open("av.json", encoding="utf-8") as f:
#     data = json.load(f)
#     for i in data:
#         print(data[i])
