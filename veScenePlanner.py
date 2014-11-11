__author__ = 'andrew.willis'
#Scene Planner - VE Version
#Andrew Willis 2014

from PyQt4 import QtCore, QtGui, uic
import sys,os

#Determining root path
rootPathVar=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')

#declare instruction
epsInst=[]

class veScenePlanner(QtGui.QMainWindow):
    def __init__(self,*args):
        QtGui.QMainWindow.__init__(self,*args)
        self.Main_Window=uic.loadUi(rootPathVar+'/veScenePlannerUI.ui')
        self.Main_Window.show()
        self.Main_Window.setFixedSize(565,418)

        #Additional
        self.Main_Window.workspaceGroup.hide()
        self.Main_Window.actionSave_As.setEnabled(1)

        #connect other function
        self.Main_Window.scenePlannerTable.itemSelectionChanged.connect(self.populateEdit)

        #connect control function
        self.Main_Window.actionBlank_Episode.triggered.connect(lambda*args:self.new(blank=True))
        self.Main_Window.actionSave_As.triggered.connect(lambda*args:self.fileOperation(save=True))
        self.Main_Window.actionOpen.triggered.connect(lambda*args:self.fileOperation(save=False))
        self.Main_Window.actionGenerate_From_xml.triggered.connect(self.generateFromXML)

        #connect button function
        self.Main_Window.addShotButton.clicked.connect(self.addShot)
        self.Main_Window.updateShotButton.clicked.connect(self.editFile)
        self.Main_Window.moveUpButton.clicked.connect(lambda*args:self.moved(up=True))
        self.Main_Window.moveDownButton.clicked.connect(lambda*args:self.moved(up=False))
        self.Main_Window.deleteShotButton.clicked.connect(self.deleteShot)
        return

    def generateFromXML(self):

        return

    def deleteShot(self):
        global epsInst
        selected=self.Main_Window.scenePlannerTable.selectedItems()
        if selected!=[]:
            repVar=QtGui.QMessageBox.question(None,'Delete','Delete selected shot?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if repVar==16384:epsInst.remove([str(selected[0].text()),str(selected[1].text())])
        self.populator()
        return

    def moved(self,up=True):
        global epsInst
        selected=self.Main_Window.scenePlannerTable.selectedItems()
        if selected!=[]:
            if up==True:
                curIndex= epsInst.index([str(selected[0].text()),str(selected[1].text())])
                if curIndex!=0:
                    epsInst.insert(curIndex-1,epsInst.pop(curIndex))
                    self.populator()
                    self.Main_Window.scenePlannerTable.selectRow(curIndex-1)
            else:
                curIndex= epsInst.index([str(selected[0].text()),str(selected[1].text())])
                if curIndex!=len(epsInst):
                    epsInst.insert(curIndex+1,epsInst.pop(curIndex))
                    self.populator()
                    self.Main_Window.scenePlannerTable.selectRow(curIndex+1)
        return

    def populateEdit(self):
        selected=self.Main_Window.scenePlannerTable.selectedItems()
        if selected!=[]:
            self.Main_Window.editName.setText(selected[0].text())
            self.Main_Window.editFrame.setValue(int(selected[1].text()))
        else:
            self.Main_Window.editName.clear()
            self.Main_Window.editFrame.clear()
        return

    def editFile(self):
        global epsInst
        editName=str(self.Main_Window.editName.text())
        editFrame=str(self.Main_Window.editFrame.value())
        if editName=='' or editFrame=='':
            QtGui.QMessageBox.warning(None,'Error','Incomplete shot information',QtGui.QMessageBox.Ok)

        selected=self.Main_Window.scenePlannerTable.selectedItems()
        temp=[]
        for chk in epsInst:
            if not chk[0]==str(selected[0].text()):temp.append(chk)

        for chk in temp:
            if chk[0]==editName:
                QtGui.QMessageBox.warning(None,'Error','There is a shot with the same name detected.',QtGui.QMessageBox.Ok)
                raise StandardError, 'error : shot with same name detected'

        tempFinal=[]
        for chk in epsInst:
            tempFinal.append([editName,editFrame]) if chk[0]==str(selected[0].text()) else tempFinal.append(chk)

        epsInst=tempFinal

        self.Main_Window.editName.clear()
        self.Main_Window.editFrame.clear()
        self.windowTitleManager(edited=True)
        self.populator()
        return

    def fileOperation(self,save=True):
        global epsInst
        if save==True:
            fileLoc=str(QtGui.QFileDialog.getSaveFileName(None,'Save'))
            if not fileLoc.endswith('.ecf'):
                fileLoc=fileLoc+'.ecf'

            writeInst=''
            for chk in epsInst:
                writeInst=writeInst+chk[0]+':'+chk[1]+'\n'
            writer=open(fileLoc,'w')
            writer.write(writeInst)
            writer.close()
            self.windowTitleManager(edited=False,newTitle=fileLoc)
        else:
            fileLoc=str(QtGui.QFileDialog.getOpenFileName(None,'Open'))
            reader=open(fileLoc,'r')
            readInst=reader.readlines()
            reader.close()
            epsInst=[]
            for chk in readInst:
                chk=chk.replace('\n','')
                epsInst.append([chk[:chk.find(':')],chk[chk.find(':')+1:]])
            self.windowTitleManager(edited=False,newTitle=fileLoc)
            self.Main_Window.workspaceGroup.show()
            self.clearWorkspace()
            self.populator()
        return

    def windowTitleManager(self,edited=None,newTitle=None):
        if edited!=None:
            title=str(self.Main_Window.windowTitle())
            if edited==True:
                if not title.endswith('*'):self.Main_Window.setWindowTitle(title+'*')
            if edited==False:
                self.Main_Window.setWindowTitle(title.replace('*',''))
        if newTitle!=None:
            self.Main_Window.setWindowTitle(str(newTitle))
        self.Main_Window.workspaceGroup.hide();self.Main_Window.workspaceGroup.show()
        return

    def addShot(self,*args):
        newName=str(self.Main_Window.newName.text())
        newFrame=str(self.Main_Window.newFrame.value())

        if newName=='' or newFrame=='':
            QtGui.QMessageBox.warning(None,'Error','Incomplete shot information',QtGui.QMessageBox.Ok)

        hit=False
        for chk in epsInst: hit=True if chk[0]==newName else None

        if hit==True:
            QtGui.QMessageBox.warning(None,'Error','Shot with the same name detected!',QtGui.QMessageBox.Ok)
            raise StandardError, 'error : shot with the same neame detected'
        else:
            epsInst.append([newName,newFrame])
            self.populator()

        self.Main_Window.newName.clear()
        self.Main_Window.newFrame.clear()
        self.windowTitleManager(edited=True)
        return

    def getTableDate(self):
        rowSelected=self.Main_Window.scenePlannerTable.selectedItems()
        columnCount=int(self.Main_Window.scenePlannerTable.columnCount())
        rowGrouped=[];temp=[]

        for base in range(len(rowSelected)/columnCount):
            cnt=0
            for chk in range(columnCount):
                temp.append(str(rowSelected[base+cnt].text()))
                cnt+=len(rowSelected)/columnCount
            rowGrouped.append(temp)
            temp=[]
        return rowGrouped

    def populator(self):
        #populate table
        self.Main_Window.scenePlannerTable.setRowCount(0)
        self.Main_Window.scenePlannerTable.setRowCount(len(epsInst))
        cnt=0;flipFlop=False;frameCnt=0
        for chk in epsInst:
            if flipFlop==False:
                colorCode=QtGui.QColor(180,180,180)
                flipFlop=True
            else:
                colorCode=QtGui.QColor(200,200,200)
                flipFlop=True

            item=QtGui.QTableWidgetItem(str(chk[0]))
            item.setBackground(colorCode)
            self.Main_Window.scenePlannerTable.setItem(cnt,0,item)

            item=QtGui.QTableWidgetItem(str(chk[1]))
            frameCnt=frameCnt+int(chk[1])
            item.setBackground(colorCode)
            self.Main_Window.scenePlannerTable.setItem(cnt,1,item)
            cnt+=1
        self.Main_Window.scenePlannerTable.resizeColumnsToContents()

        #counter
        self.Main_Window.shotCountLCD.display(len(epsInst))
        self.Main_Window.frameCountLCD.display(frameCnt)
        return

    def new(self,blank=False):
        global epsInst
        if str(self.Main_Window.windowTitle()).endswith('*'):
            repVar=QtGui.QMessageBox.question(None,'Save','There is an unsaved file. Would you like to save it?',\
                                              QtGui.QMessageBox.Yes,QtGui.QMessageBox.No,QtGui.QMessageBox.Cancel)
            if repVar==16384:
                self.fileOperation(save=True)
            else:
                raise StandardError, 'error : cancelled by user'
        if blank==True:
            epsInst=[]
            self.clearWorkspace()
            self.Main_Window.workspaceGroup.show()
            self.Main_Window.setWindowTitle('Untitled*')
        return

    def clearWorkspace(self):
        self.Main_Window.scenePlannerTable.setRowCount(0)
        self.Main_Window.shotCountLCD.display(0)
        self.Main_Window.frameCountLCD.display(0)
        self.Main_Window.newName.clear()
        self.Main_Window.newFrame.clear()
        self.Main_Window.editName.clear()
        self.Main_Window.editFrame.clear()
        return

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = veScenePlanner()
    sys.exit(app.exec_())