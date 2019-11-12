#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 20/Jan/16 22:42

"""
"""
default.txt
"""
"""
Getting Started				How to familiarize yourself with Qt Designer
    Launching Designer			Running the Qt Designer application
    The User Interface			How to interact with Qt Designer

Designing a Component			Creating a GUI for your application
    Creating a Dialog			How to create a dialog
    Composing the Dialog		Putting widgets into the dialog example
    Creating a Layout			Arranging widgets on a form
    Signal and Slot Connections		Making widget communicate with each other

Using a Component in Your Application	Generating code from forms
    The Direct Approach			Using a form without any adjustments
    The Single Inheritance Approach	Subclassing a form's base class
    The Multiple Inheritance Approach	Subclassing the form itself
    Automatic Connections		Connecting widgets using a naming scheme
        A Dialog Without Auto-Connect	How to connect widgets without a naming scheme
        A Dialog With Auto-Connect	Using automatic connections

Form Editing Mode			How to edit a form in Qt Designer
    Managing Forms			Loading and saving forms
    Editing a Form			Basic editing techniques
    The Property Editor			Changing widget properties
    The Object Inspector		Examining the hierarchy of objects on a form
    Layouts				Objects that arrange widgets on a form
        Applying and Breaking Layouts	Managing widgets in layouts
        Horizontal and Vertical Layouts	Standard row and column layouts
        The Grid Layout			Arranging widgets in a matrix
    Previewing Forms			Checking that the design works

Using Containers			How to group widgets together
    General Features			Common container features
    Frames				QFrame
    Group Boxes				QGroupBox
    Stacked Widgets			QStackedWidget
    Tab Widgets				QTabWidget
    Toolbox Widgets			QToolBox

Connection Editing Mode			Connecting widgets together with signals and slots
    Connecting Objects			Making connections in Qt Designer
    Editing Connections			Changing existing connections
"""

from PyQt5.QtCore import (QAbstractItemModel, QFileInfo, QItemSelectionModel,
        QModelIndex, Qt)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAbstractItemView, QApplication,
        QFileIconProvider, QListView, QSplitter, QTableView, QTreeView)
import pandas as pd


class TreeItem(object):
    def __init__(self,name, data, parent=None):
        self.name = name
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0
    def findChildren(self,nameChildren):
        if self.name == nameChildren:
            return self
        elif self.childCount()>0:
            for child in self.childItems:
                ch = child.findChildren(nameChildren)
                if ch != None:
                    return ch
        else:
            return None

class TreeModel(QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.iconProvider = QFileIconProvider()
        self.rootItem = TreeItem("1111",('2222','3333'))
        self.setupModelData(data, self.rootItem)

        print('Data')
    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if role == Qt.DecorationRole:
            if index.internalPointer().itemData != None and index.internalPointer().itemData[1]=='FOLDER':
                return self.iconProvider.icon(QFileIconProvider.Folder)
            return self.iconProvider.icon(QFileIconProvider.File)
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None



        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setupModelData(self, allList, parent):
        for itemList in allList:
            if itemList[1]==1 and itemList[4]=='FOLDER':
                self.appendItem(itemList,parent)
            else:
                child = parent.findChildren(itemList[3])
                if child!=None:
                    self.appendItem(itemList,child)

    def appendItem(self,item,object):
        if item[4]=='FOLDER':
            object.appendChild (TreeItem(item[3]+'\\\\'+item[2],(item[2],item[4]),object))
        else:
            object.appendChild (TreeItem(item[3],(item[2],item[4]),object))
            # if object.itemData != None:
            #     object.itemData = object.itemData+((item[2],item[4]))
            # else:
            #     object.itemData = (item[2],item[4])


if __name__ == '__main__':
    import sys

    df = pd.read_csv('data.txt', delimiter='|')
    folderList = [list(x) for x in df.values if x[4]=='FOLDER']
    jobList = [list(x) for x in df.values if x[4]!='FOLDER']
    allList = [list(x) for x in df.values]

    app = QApplication(sys.argv)

    # f = QFile('default.txt')
    # f.open(QIODevice.ReadOnly)
    model = TreeModel(allList)
    # f.close()

    view = QTreeView()
    view.setModel(model)
    view.setWindowTitle("Simple Tree Model")
    view.show()
    app.exec_()
