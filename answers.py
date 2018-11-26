from tinydb import TinyDB, Query, where
import csv

db = TinyDB('qna.json')
questions = set([line['question'] for line in db])
print('questions %s' %questions)

def get_answer(question):
    return "random answer. not even random. go fuck yourself %s" % question


def update_from_csv(csv_file):
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        print('header: %s' % header)
        for i, row in enumerate(reader):
            User = Query()
            print('row %d: question: %s, answers %s' % (i, row[1], row[2]))
            #p = db.search(User.question == row[1], User.answer == row[2])
            #print(p)
            db.insert({'question': row[1], 'answer': row[2]})

def print_db():
    for a in db:
        print(a)

if __name__ == '__main__':
#    print_db()
    update_from_csv('rsp.csv')