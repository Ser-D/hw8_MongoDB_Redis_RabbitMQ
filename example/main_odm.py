import argparse

from mongoengine import connect, Document, StringField, IntField, ListField, DoesNotExist

connect(db='hw8',
        host='mongodb+srv://userhw8:<PASS>@atlascluster.dkms1wa.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster')

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


class Cat(Document):
    name = StringField(max_length=120, required=True)
    age = IntField(min_value=1, max_value=30)
    features = ListField(StringField(max_length=150))
    meta = {'collection': 'cats'}


def find():
    return Cat.objects.all()


def create(name, age, features):
    r = Cat(name=name, age=age, features=features)
    r.save()
    return r


def update(pk, name, age, features):
    cat = Cat.objects(id=pk).first()  # cat or None
    if cat:
        cat.update(name=name, age=age, features=features)
        cat.reload()
    return cat


def delete(pk):
    try:
        cat = Cat.objects.get(id=pk)  # cat or DoesNotExist
        cat.delete()
        return cat
    except DoesNotExist:
        return None


def main():
    match action:
        case 'create':
            r = create(name, age, features)
            print(r.to_mongo().to_dict())
        case "read":
            r = find()
            print([e.to_mongo().to_dict() for e in r])
        case 'update':
            r = update(pk, name, age, features)
            if r:
                print(r.to_mongo().to_dict())
        case 'delete':
            r = delete(pk)
            if r:
                print(r.to_mongo().to_dict())
        case _:
            print('unknown command')


if __name__ == '__main__':
    main()

# Example:
#  py .\example\main_odm.py --action read
# py .\example\main_odm.py --action create --name Bubu --age 2 --features "Лінивий" "Муркотить"
# py .\example\main_odm.py --action update --id 65e09e8f2f926712609821a3 --name Tom --age 3 --features "дає себе гладити" "Муркотить"
# py .\example\main_odm.py --action delete --id 65e09f212f926712609821a4
