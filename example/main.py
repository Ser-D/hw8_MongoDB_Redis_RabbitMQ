import argparse
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId

uri = "mongodb+srv://userhw8:<PASS>@atlascluster.dkms1wa.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster"


client = MongoClient(uri)

db = client.hw8

parser = argparse.ArgumentParser(description='Server Cats')

parser.add_argument("--action", help="create, read, update, delete")
parser.add_argument('--id')
parser.add_argument('--name')
parser.add_argument('--age')
parser.add_argument('--features', nargs='+')

arg = vars(parser.parse_args())

action = arg.get("action")
pk = arg.get('id')
name = arg.get('name')
age = arg.get('age')
features = arg.get('features')


def find():
    return db.cats.find()


def create(name, age, features):
    db.cats.insert_one({
            'name': name,
            'age': age,
            'features': features,
        })


def update(pk, name, age, features):
    r = db.cats.update_one({'_id': ObjectId(pk)}, {
        "$set": {
            'name': name,
            'age': age,
            'features': features,
            }

        })


def delete(pk):
    return db.cats.delete_one({'_id': ObjectId(pk)})


def main():
    match action:
        case'create':
            r = create(name, age, features)
            print(r, 'mm')
        case "read":
            r = find()
            print([e for e in r])
        case 'update':
            r = update(pk, name, age, features)
            print(r)
        case 'delete':
            r = delete(pk)
            print(r)
        case _:
            print('unknown command')


if __name__ == '__main__':
    main()


# try:
#     db.cats.insert_many([
#         {
#             'name': 'Boris',
#             'age': 12,
#             'features': ['ходить в лоток', 'не дає себе гладити', 'сірий'],
#         },
#         {
#             'name': 'Murzik',
#             'age': 1,
#             'features': ['ходить в лоток', 'дає себе гладити', 'чорний'],
#         },
#     ])
#
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

