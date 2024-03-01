import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str):
    print(f'Find by {tag}')
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str):
    print(f'Find by {author}')
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result

def main():
    """
    Функція працює у безкінечному циклі поки користувач не введе 'exit'
    Приймає у себе команду для пошуку через ":". доступні команди: name, tag, tags
    у випадку tags - усі теги, які необхідно знайти розділяються комою.
    """
    while True:
        user_input = input('>>> ').lower()
        if user_input.lower() == 'exit':
            exit(0)
        elif user_input.lower().startswith('name') or user_input.lower().startswith('tag'):
            try:
                command, value = user_input.split(":")
                if command == 'name':
                    author = value.strip()
                    author_quotes = find_by_author(author)
                    if author_quotes:
                        print(author_quotes)
                    else:
                        print(f'Author with name "{author}" is not present in the DB')
                elif command == 'tag':
                    tag = value
                    tag_res = find_by_tag(tag)
                    if tag_res:
                        print(tag_res)
                    else:
                        print(f'The search value {value} is not present in DB')
                elif command == 'tags':
                    tags = value.split(',')
                    tags = [tag.strip() for tag in tags]
                    matching_quotes = []
                    for tag in tags:
                        if tag:
                            matching_quotes.extend(find_by_tag(tag))
                    if len(matching_quotes) > 0:
                        print(matching_quotes)
                    else:
                        print(f'The search value "{tag}" is not present in DB')
                else:
                    continue
            except ValueError:
                print('Use ":" between command and text which you want to find without spaces and separated by coma')
                continue
        else:
            print(f'Command "{user_input}" is not a right command')


if __name__ == '__main__':
    main()





    # print(find_by_tag('l'))
    # print(find_by_tag('l'))
    # print(find_by_author('Ei'))
    # print(find_by_author('Ei'))
    # quotes = Quote.objects().all()
    # print([e.to_json() for e in quotes])
