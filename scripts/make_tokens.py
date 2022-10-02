import os
import re

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../outputs/img-samples/dream_log.txt')

def main():
    descriptions = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            descriptions.append(line.split('"')[1])

    token_list = []
    for description in descriptions:
        for token in re.split('\,|\.',description):
            token_list.append(token.strip())

    tokens = list(set(token_list))

    print(tokens)

if __name__ == "__main__":
    main()