import json


def get_data():
    with open('data/request-data.json') as f:
        q = json.load(f)
    with open('data/schema.sql') as f:
        s = f.read()
    with open('data/result.sql') as f:
        r = f.read()
    return q, s, r


if __name__ == '__main__':
    d = get_data()
    print(d[0])
    print(d[1])
    print(d[2])
