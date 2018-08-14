import json
import logging

import jieba
from gensim.corpora import Dictionary

ARTICLE_ID = 'article_id'
ARTICLE_TITLE = 'article_title'
ARTICLE_CONTENT = 'article_content'
QUESTIONS = 'questions'
QUESTION = 'question'
QUESTIONS_ID = 'questions_id'
ANSWER = 'answer'

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def jieba_tokenize(text: str) -> list:
    """use jieba module to tokenize word

    Arguments:
        text {str} -- raw text
    """

    text = str_q2b(text)
    tokens = list(jieba.cut(text, cut_all=False))
    tokens = [w for w in tokens if w != ' ']
    return tokens


def build_dictionary(file_path: str) -> Dictionary:
    """build token2id dictionary by the data in file_path

    Arguments:
        file_path {str} -- path for data file
    """
    data = None
    with open(file_path, mode='r', encoding='utf-8') as fp:
        data = json.load(fp)

    # init dictionary
    dictionary = Dictionary()

    for article in data:
        # extract article text
        article_title = article[ARTICLE_TITLE]
        article_content = article[ARTICLE_CONTENT]

        # get token from text
        segment1 = jieba_tokenize(article_title)
        segment2 = jieba_tokenize(article_content)

        dictionary.add_documents([segment1, segment2])

        for questions_obj in article[QUESTIONS]:
            # extract question text
            question = questions_obj[QUESTION]
            answer = questions_obj[ANSWER]

            # get token from text
            segment1 = jieba_tokenize(question)
            segment2 = jieba_tokenize(answer)

            dictionary.add_documents([segment1, segment2])

    # return result
    return dictionary


def str_q2b(ustring: str) -> str:
    """convert full string to half string

    Arguments:
        string {str} -- unicode string
    """
    ret_str = ''
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:
            inside_code = 32
        elif inside_code >= 65281 and inside_code <= 65374:
            inside_code -= 65248

        ret_str += chr(inside_code)
    return ret_str


if __name__ == '__main__':
    dictionary = build_dictionary('./data/question.json')
    dictionary.save('./data/jieba.dict')
