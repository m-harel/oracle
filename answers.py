from pyexcel_ods import get_data
from collections import Counter, OrderedDict
import json
import word_detector
import random

try:
    qna = json.load(open("qna.json", "r"))
except:
    qna = {}

def get_answer(question):
    if question in qna.keys():
        list_of_answers = [(ans_id, a) for ans_id, a in qna[question].items()]
        print('best answers - %s' % list_of_answers)
        return random.choice(list_of_answers)

    print('question: %s ' % question)
    question_rank = OrderedDict()
    for q in qna.keys():
        question_rank[q] = rate_questions(question, q)

    print('question rank:')
    print(question_rank)
    best_answers = get_the_best_n_answer_from_dict(question_rank, 10)
    print('best answers - %s' % best_answers)
    return random.choice(best_answers)


def get_the_best_n_answer_from_dict(question_rank, n):
    best_answers = []
    question_sorted_by_rank = sorted(question_rank.items(), key=lambda kv: kv[1])
    question_sorted_by_rank.reverse()
    print(question_sorted_by_rank)
    for question in question_sorted_by_rank:
        for ans_id, a in qna[question[0]].items():
            best_answers.append((ans_id, a))

        if len(best_answers) >= n:
            break

    return best_answers


def rate_questions(a, b):
    rank = 0
    b_words = b.split()
    for a_word in a.split():
        if a_word in b_words:
            rank += word_detector.words_dict[a_word]['rank']

    if b_words[0] == a.split()[0]:
        rank += 20

    return rank

def sanitize(phrase):
    phrase = "".join([c for c in phrase if c.isalpha() or c.isspace()])
    phrase = phrase.lower().strip()
    return phrase


def update_from_ods():
    data = get_data('rsp.ods')

    output = {}

    for i, line in enumerate(data["Form Responses 1"][1:]):
        if len(line) < 3:
            continue
        datetime = line[0]
        question = sanitize(line[1])
        answer = line[2]
        if question not in output.keys():
            output[question] = {}
        output[question][i] = answer

    print(output)
    json.dump(dict(output), open("qna.json", "w"))

def create_histogram():
    counter = Counter()
    print(qna.keys())
    i = 0
    for question in qna.keys():
        for word in question.split():
            counter[word] += 1
            i += 1

    print('counter size is %d' % len(counter))
    print(counter)
    counter_keys = list(counter.keys())
    counter_keys.sort()
    words_dict = json.load(open("words.json", "r"))
    words = words_dict.keys()
    i = 0
    for word in counter_keys:
        if word not in words:
            print(word)
            i+=1
    print(i)
    return counter_keys

def create_empty_word_dict(words):
    output = {}

    for word in words:
        output[word] = {'rank': 1, 'id': -1}

    print(output)
    json.dump(dict(output), open("words.json", "w"))

if __name__ == '__main__':
    #update_from_ods()
    #words = create_histogram()
    # create_empty_word_dict(words)
    print(get_answer('can an arab be a friend'))
