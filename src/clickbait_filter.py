#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Variables ===================================================================
# Functions & classes =========================================================
def read_examples(fn):
    with open(fn) as f:
        data = f.read()

    parsed = (
        line
        for line in data.splitlines()
        if line.strip()
    )

    positive = []
    negative = []
    whitespace = {" ", "\t"}

    for expression in parsed:
        if expression[0] in whitespace:
            negative.append(expression.strip())
        else:
            positive.append(expression)

    nt = namedtuple("TrainingSet", "positive negative")

    return nt(positive, negative)


class Classificators(object):
    @staticmethod
    def capitalize_score(sentence):
        cap_words = [
            word
            for word in sentence
            if word[0].isalnum() and word[0] == word[0].upper()
        ]
        return len(cap_words) / len(sentence)

    @staticmethod
    def has_number_at_beginning(sentence):
        number_words = [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "eleven",
            "twelve",
            "dozen",
            "thirteen",
            "fourteen",
            "fifteen",
            "sixteen",
            "seventeen",
            "eighteen",
            "nineteen",
            "twenty",
            "thirty",
            "forty",
            "fifty",
            "sixty",
            "seventy",
            "eighty",
        ]

        def test_word(word):
            if word.isdigit() and int(word) < 100:
                return True
            elif word.lower() in number_words:
                return True

            return False

        first = sentence[0]
        second = sentence[1]
        third = sentence[2]

        return test_word(first) or test_word(second) or test_word(third)

    @staticmethod
    def is_clickbaity(sentence):
        second_word_clickbaits = {
            "amazing",
            "bad",
            "best",
            "clues",
            "days",
            "engineering",
            "essential",
            "examples",
            "excellence",
            "excellent",
            "factor",
            "fantastic",
            "free",
            "funniest",
            "great",
            "habits",
            "languages",
            "mistakes",
            "most",
            "official",
            "open",
            "popular",
            "practices",
            "productivity",
            "questions",
            "reasons",
            "resolutions",
            "rules",
            "steps",
            "things",
            "tips",
            "typical",
            "use",
            "useful",
            "ways",
        }

        second_clickbait = False
        if len(sentence) > 1:
            second_clickbait = sentence[1] in second_word_clickbaits

        first_clickbait = False
        if sentence:
            first_clickbait = sentence[0] in {"top", "the", "my"}

        return first_clickbait or second_clickbait

    @staticmethod
    def contains_you(sentence):
        you_forms = {
            "you",
            "your",
            "yours",
        }

        matches = [
            word
            for word in sentence
            if word.lower() in you_forms
        ]

        return bool(matches)



# Main program ================================================================
if __name__ == '__main__':
    print read_examples("examples.txt")
