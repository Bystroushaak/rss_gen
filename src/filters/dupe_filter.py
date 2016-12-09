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


# Functions & classes =========================================================
# in 2.7, there is no context manager for shelve :S
@contextmanager
def shelver(fn):
    db = shelve.open(fn)
    yield db
    db.close()


class DupeFilter(object):
    dupe_key = "dupes"

    def __init__(self, fn=None):
        self.fn = fn
        self.dupes = set()
        self.protected = {}

        self.protected_time = 30 * 60  # 30m

    def in_dupes(self, item):
        if item in self.dupes:
            return True

        return self._update_protected(item)

    def _update_protected(self, item):
        if item not in self.protected:
            self.protected[item] = time.time() + self.protected_time
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
            new_df = DupeFilter(fn=fn)
            df = db.get(DupeFilter.dupe_key, new_df)
            new_df.__dict__.update(df.__dict__)

            return new_df

    def save_dupes(self, fn=None):
        if not self.fn and not fn:
            raise IOError("Filename has to be set!")

        if not fn:
            fn = self.fn

        with shelver(fn) as db:
            db[DupeFilter.dupe_key] = self
