# -*- coding: utf-8 -*-

import problems.gendenshteyn10 as gendenshteyn10
import problems.gendenshteyn11 as gendenshteyn11
import problems.gendenshteyn7 as gendenshteyn7
import problems.gendenshteyn8 as gendenshteyn8
import problems.yakunin as yakunin


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
