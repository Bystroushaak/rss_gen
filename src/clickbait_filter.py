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


# Main program ================================================================
if __name__ == '__main__':
    print read_examples("examples.txt")
