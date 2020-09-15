# -*- coding: utf-8 -*-

import gendenshteyn10
import gendenshteyn11
import gendenshteyn7
import gendenshteyn8
import yakunin


class Tasks(object):
    def __init__(self):
        self.__TasksDict = {}
        for tasksGenerator in [
            gendenshteyn7.Gendenshteyn7(),
            gendenshteyn8.Gendenshteyn8(),
            gendenshteyn10.Gendenshteyn10(),
            gendenshteyn11.Gendenshteyn11(),
            yakunin.Yakunin(),
        ]:
            bookName = tasksGenerator.GetBookName()
            assert bookName not in self.__TasksDict
            self.__TasksDict[bookName] = {}
            for task in tasksGenerator():
                self.__TasksDict[bookName][task.Number] = task

    def GetTask(self, book, number):
        return self.__TasksDict[book][number]
