#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from progressbar import Bar, ETA, Percentage, ProgressBar


class Pbar(ProgressBar):
    def __init__(self,init_text, maxval):
        super(Pbar, self).__init__(widgets=[
            init_text,
            Percentage(),
            ' ',
            Bar(marker='#', left='[', right=']'),
            ' ',
            ETA()],
            maxval=maxval
        )
        self.start()

    def plus_one(self):
        self.update(self.currval+1)
