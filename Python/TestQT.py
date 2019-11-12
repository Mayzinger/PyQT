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



root = TreeItem("\\\\_DWH\\\\10_DWH\\\\BIS\\\\CREDIT",('CREDIT','FOLDER'))
def getListFolder(root,folderList):
    pass

df = pd.read_csv('data.txt', delimiter='|')
folderList = [list(x) for x in df.values if x[4]=='FOLDER']
jobList = [list(x) for x in df.values if x[4]!='FOLDER']
for folder in folderList:
    if folder[1]==1:
        root.appendChild (TreeItem(folder[3]+'\\\\'+folder[2],(folder[2],'FOLDER')))
    else:
        child = root.findChildren(folder[3])
        if child!=None:
            child.appendChild (TreeItem(folder[3]+'\\\\'+folder[2],(folder[2],'FOLDER')))

print(folder,file)
