from pyexcel_ods import get_data
from collections import defaultdict
import json


def get_answer(question):
    return "random answer. not even random. go fuck yourself %s" % question


def sanitize(phrase):
    phrase = "".join([c for c in phrase if c.isalpha() or c.isspace()])
    phrase = phrase.lower().strip()
    return phrase


def update_from_ods(ods_file):

    data = get_data(ods_file)


    output = defaultdict(set)

    for line in data["Form Responses 1"][1:]:
        if len(line) < 3:
            continue
        datetime = line[0]
        question = sanitize(line[1])
        answer = line[2]

        output[question].add(answer)
    json.dump(dict(output), open("qna.json"))


def print_db():
    for a in db:
        print(a)


if __name__ == '__main__':
#    print_db()
    update_from_ods('rsp.ods')
