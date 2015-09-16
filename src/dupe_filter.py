#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import time
import shelve
import os.path
from contextlib import contextmanager


# Variables ===================================================================
DUPE_KEY = "dupes"
PROTECTED_TIME = 60 * 60 * 10  # 10 hours


# Functions & classes =========================================================
# in 2.7, there is no context manager for shelve :S
@contextmanager
def shelver(fn):
    db = shelve.open(fn)
    yield db
    db.close()


class DupeFilter(object):
    def __init__(self, fn=None):
        self.fn = fn
        self.dupes = set()
        self.protected = {}

    def in_dupes(self, item):
        if item in self.dupes:
            return True

        return self._update_protected(item)

    def _update_protected(self, item):
        if item not in self.protected:
            self.protected[item] = time.time() + PROTECTED_TIME
            return False

        if self.protected[item] <= time.time():
            self.dupes.update([item])
            del self.protected[item]
            return True

        return False

    @staticmethod
    def load_dupes(fn):
        if not os.path.exists(fn):
            return DupeFilter(fn=fn)

        with shelver(fn) as db:
            return db.get(DUPE_KEY, DupeFilter(fn=fn))

    def save_dupes(self, fn=None):
        if not self.fn and not fn:
            raise IOError("Filename has to be set!")

        if not fn:
            fn = self.fn

        with shelver(fn) as db:
            db[DUPE_KEY] = self
