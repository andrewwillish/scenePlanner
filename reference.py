#Registrar Sequence Manager UI
#Andrew Willis 2014

from PyQt4 import QtCore, QtGui, uic
import sys,mncRegistrarCore,datetime

class registrarSequence(QtGui.QMainWindow):
    def __init__(self,*args):
        QtGui.QMainWindow.__init__(self,*args)
        self.Main_Window=uic.loadUi('Z:/development/mncRegistrar/mncRegistrarSeqManagerQtUI.ui')
        self.Main_Window.show()
        self.Main_Window.setFixedSize(1364,790)

        #Additional==========================================================================
        self.Main_Window.filterCoordinatorQListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.Main_Window.filterSupervisorQListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.Main_Window.filterDepartmentQListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.Main_Window.filterProjectQListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.Main_Window.filterStatusQListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.Main_Window.filterLayCplxQListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.Main_Window.filterArtistQListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.Main_Window.filterAssigneeQListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        self.Main_Window.registerTitleQLineEdit.setEnabled(1)

        self.Main_Window.registerIndividualAssignmentQPushButton.clicked.connect(self.registerSingle)
        self.Main_Window.assignmentManagemerQTableWidget.itemSelectionChanged.connect(self.populateUpdateAssignment)
        self.Main_Window.updateCommitUpdateQPushButton.clicked.connect(self.updateAssignment)
        self.Main_Window.updateCommitDeadlineQPushButton.clicked.connect(self.updateDeadline)
        self.Main_Window.updateClearDeadlineQPushButton.clicked.connect(lambda*args:self.updateDeadline(clear=True))
        self.Main_Window.updateCommitUpdateQPushButton.setEnabled(0)
        self.Main_Window.updateClearDeadlineQPushButton.setEnabled(0)
        self.Main_Window.updateCommitDeadlineQPushButton.setEnabled(0)

        self.Main_Window.filterIdMaxQSpinBox.valueChanged.connect(self.populateTable)
        self.Main_Window.filterIdMinQSpinBox.valueChanged.connect(self.populateTable)
        self.Main_Window.filterTitleQLineEdit.textChanged.connect(self.populateTable)
        self.Main_Window.filterFrameFromQSpinBox.valueChanged.connect(self.populateTable)
        self.Main_Window.filterFrameToQSpinBox.valueChanged.connect(self.populateTable)
        self.Main_Window.filterBidHourFromQSpinBox.valueChanged.connect(self.populateTable)
        self.Main_Window.filterBidHourToQSpinBox.valueChanged.connect(self.populateTable)

        self.refresh()
        return

    def dateProcessor(self,data,encrypt=None):
        #mode ENCRYPT ex.06/06/2013>20130606 DECRYPT ex.20130606>06/06/2013
        result=None
        if encrypt==False:
            result=data.replace('-','')
            if result.find(' ')!=-1:result=result[:result.find(' ')]
        elif encrypt==True:
            result=data[:4]+'-'+data[4:6]+'-'+data[6:8]
        return result

    def updateDeadline(self,clear=False):
        #get selected row
        selectedRow=self.Main_Window.assignmentManagemerQTableWidget.selectedItems()
        rowGrouped=[]
        temp=[]

        for base in range(len(selectedRow)/15):
            cnt=0
            for chk in range(15):
                temp.append(str(selectedRow[base+cnt].text()))
                cnt+=len(selectedRow)/15
            rowGrouped.append(temp)
            temp=[]

        if clear==False:
            for chk in rowGrouped:
                deadLineDate=str(self.Main_Window.updateDeadlineQDateEdit.text())
                deadLineDate=deadLineDate.replace('/','-')+' 00:00:00'
                if deadLineDate=='2000-1-1 00:00:00': deadLineDate='None'
                mncRegistrarCore.updateSeqRecord(id=chk[0],deadline=deadLineDate)
        else:
            for chk in rowGrouped:mncRegistrarCore.updateSeqRecord(id=chk[0],deadline='None')
        self.populateTable()
        return

    def updateAssignment(self):
        #get selected row
        selectedRow=self.Main_Window.assignmentManagemerQTableWidget.selectedItems()
        rowGrouped=[]
        temp=[]

        for base in range(len(selectedRow)/15):
            cnt=0
            for chk in range(15):
                temp.append(str(selectedRow[base+cnt].text()))
                cnt+=len(selectedRow)/15
            rowGrouped.append(temp)
            temp=[]

        for chk in rowGrouped:
            #get data
            department=str(self.Main_Window.updateDepartmentQComboBox.currentText())
            bidHour=str(self.Main_Window.updateBidHourQSpinBox.text())
            status=str(self.Main_Window.updateStatusQComboBox.currentText())
            artist=str(self.Main_Window.updateArtistQComboBox.currentText())
            coordinator=str(self.Main_Window.updateCoordinatorQComboBox.currentText())
            supervisor=str(self.Main_Window.updateSupervisorQComboBox.currentText())
            complexity=str(self.Main_Window.updateLayCplxQComboBox.currentText())

            mncRegistrarCore.updateSeqRecord(id=chk[0],\
                                             department=department,\
                                             bidHour=bidHour,\
                                             status=status,\
                                             artist=artist,\
                                             coord=coordinator,\
                                             supervisor=supervisor,\
                                             complexity=complexity)
        self.populateTable()
        return

    def populateUpdateAssignment(self):
        selectedRow=self.Main_Window.assignmentManagemerQTableWidget.selectedItems()
        totalSelected=int(len(selectedRow)/14)
        tempLis=[]

        if totalSelected>1:
            self.Main_Window.updateIdQLineEdit.setText('<multiple record>')
            self.Main_Window.updateTitleQLineEdit.setText('<multiple record>')
            self.Main_Window.updateProjectQLineEdit.setText('<multiple record>')
            self.Main_Window.updateAssigneeQLineEdit.setText('<multiple record>')
            self.Main_Window.updateRegisteredDateQLineEdit.setText('<multiple record>')

            self.Main_Window.updateDepartmentQComboBox.setCurrentIndex(0)
            self.Main_Window.updateBidHourQSpinBox.setValue(0)
            self.Main_Window.updateStatusQComboBox.setCurrentIndex(0)
            self.Main_Window.updateArtistQComboBox.setCurrentIndex(0)
            self.Main_Window.updateCoordinatorQComboBox.setCurrentIndex(0)
            self.Main_Window.updateSupervisorQComboBox.setCurrentIndex(0)
            self.Main_Window.updateLayCplxQComboBox.setCurrentIndex(0)
            self.Main_Window.updateDeadlineQDateEdit.setDateTime(QtCore.QDateTime(2000,01,01,0,0,0))
            self.Main_Window.updateBidHourQSpinBox.clear()
            self.Main_Window.updateCommitUpdateQPushButton.setEnabled(1)
            self.Main_Window.updateClearDeadlineQPushButton.setEnabled(1)
            self.Main_Window.updateCommitDeadlineQPushButton.setEnabled(1)
        elif totalSelected==0:
            self.Main_Window.updateIdQLineEdit.setText('')
            self.Main_Window.updateTitleQLineEdit.setText('')
            self.Main_Window.updateProjectQLineEdit.setText('')
            self.Main_Window.updateAssigneeQLineEdit.setText('')
            self.Main_Window.updateRegisteredDateQLineEdit.setText('')

            self.Main_Window.updateDepartmentQComboBox.setCurrentIndex(0)
            self.Main_Window.updateBidHourQSpinBox.setValue(0)
            self.Main_Window.updateStatusQComboBox.setCurrentIndex(0)
            self.Main_Window.updateArtistQComboBox.setCurrentIndex(0)
            self.Main_Window.updateCoordinatorQComboBox.setCurrentIndex(0)
            self.Main_Window.updateSupervisorQComboBox.setCurrentIndex(0)
            self.Main_Window.updateLayCplxQComboBox.setCurrentIndex(0)
            self.Main_Window.updateDeadlineQDateEdit.setDateTime(QtCore.QDateTime(2000,01,01,0,0,0))
            self.Main_Window.updateBidHourQSpinBox.clear()
            self.Main_Window.updateCommitUpdateQPushButton.setEnabled(0)
            self.Main_Window.updateClearDeadlineQPushButton.setEnabled(0)
            self.Main_Window.updateCommitDeadlineQPushButton.setEnabled(0)
        else:
            for chk in selectedRow:
                tempLis.append(str(chk.text()))
            self.Main_Window.updateIdQLineEdit.setText(tempLis[0])
            self.Main_Window.updateTitleQLineEdit.setText(tempLis[1])
            self.Main_Window.updateProjectQLineEdit.setText(tempLis[4])
            self.Main_Window.updateAssigneeQLineEdit.setText(tempLis[9])
            self.Main_Window.updateRegisteredDateQLineEdit.setText(tempLis[12])
            self.Main_Window.updateCommitUpdateQPushButton.setEnabled(1)
            self.Main_Window.updateClearDeadlineQPushButton.setEnabled(1)
            self.Main_Window.updateCommitDeadlineQPushButton.setEnabled(1)

            if str(tempLis[3])<>'':
                allStatus=[self.Main_Window.updateDepartmentQComboBox.itemText(ct) for ct in range(self.Main_Window.updateDepartmentQComboBox.count())]
                cnt=0
                for chk in allStatus:
                    if str(chk)==str(tempLis[3]):
                        self.Main_Window.updateDepartmentQComboBox.setCurrentIndex(cnt)
                    cnt+=1

            self.Main_Window.updateBidHourQSpinBox.setValue(int(tempLis[5]))

            if str(tempLis[6])<>'None':
                allStatus=[self.Main_Window.updateStatusQComboBox.itemText(ct) for ct in range(self.Main_Window.updateStatusQComboBox.count())]
                cnt=0
                for chk in allStatus:
                    if str(chk)==str(tempLis[6]):
                        self.Main_Window.updateStatusQComboBox.setCurrentIndex(cnt)
                    cnt+=1

            if str(tempLis[7])<>'None':
                allStatus=[self.Main_Window.updateArtistQComboBox.itemText(ct) for ct in range(self.Main_Window.updateArtistQComboBox.count())]
                cnt=0
                for chk in allStatus:
                    if str(chk)==str(tempLis[7]):
                        self.Main_Window.updateArtistQComboBox.setCurrentIndex(cnt)
                    cnt+=1

            if str(tempLis[9])<>'None':
                allStatus=[self.Main_Window.updateCoordinatorQComboBox.itemText(ct) for ct in range(self.Main_Window.updateCoordinatorQComboBox.count())]
                cnt=0
                for chk in allStatus:
                    if str(chk)==str(tempLis[9]):
                        self.Main_Window.updateCoordinatorQComboBox.setCurrentIndex(cnt)
                    cnt+=1

            if str(tempLis[10])<>'None':
                allStatus=[self.Main_Window.updateSupervisorQComboBox.itemText(ct) for ct in range(self.Main_Window.updateSupervisorQComboBox.count())]
                cnt=0
                for chk in allStatus:
                    if str(chk)==str(tempLis[10]):
                        self.Main_Window.updateSupervisorQComboBox.setCurrentIndex(cnt)
                    cnt+=1

            if str(tempLis[11])<>'':
                allStatus=[self.Main_Window.updateLayCplxQComboBox.itemText(ct) for ct in range(self.Main_Window.updateLayCplxQComboBox.count())]
                cnt=0
                for chk in allStatus:
                    if str(chk)==str(tempLis[11]):
                        self.Main_Window.updateLayCplxQComboBox.setCurrentIndex(cnt)
                    cnt+=1
            else:
                self.Main_Window.updateLayCplxQComboBox.setCurrentIndex(0)

            #Populate date now
            if tempLis[13]!='None':
                tempDate=tempLis[13][:tempLis[13].find(' ')].split('-')
                self.Main_Window.updateDeadlineQDateEdit.setDateTime(QtCore.QDateTime(int(tempDate[0]), int(tempDate[1]), int(tempDate[2]),0, 0, 0))
            else:
                self.Main_Window.updateDeadlineQDateEdit.setDateTime(QtCore.QDateTime(2000,01,01,0,0,0))
        return

    def refresh(self):
        self.populateMenu()
        self.populateTable()
        return

    def populateMenu(self):
        #clearing
        self.Main_Window.registerBidHourQComboBox.clear()

        #populate department
        self.Main_Window.registerDepartmentQComboBox.clear()
        self.Main_Window.filterDepartmentQListWidget.clear()
        self.Main_Window.updateDepartmentQComboBox.clear()
        self.Main_Window.registerDepartmentQComboBox.addItems(['']+mncRegistrarCore.listDepartment())
        self.Main_Window.filterDepartmentQListWidget.addItems(mncRegistrarCore.listDepartment())
        self.Main_Window.updateDepartmentQComboBox.addItems(['']+mncRegistrarCore.listDepartment())

        #populate project
        self.Main_Window.registerProjectQComboBox.clear()
        self.Main_Window.filterProjectQListWidget.clear()
        self.Main_Window.registerProjectQComboBox.addItems(['']+mncRegistrarCore.listProject())
        self.Main_Window.filterProjectQListWidget.addItems(mncRegistrarCore.listProject())

        #populate Status
        self.Main_Window.filterStatusQListWidget.clear()
        self.Main_Window.updateStatusQComboBox.clear()
        self.Main_Window.filterStatusQListWidget.addItems(mncRegistrarCore.listStatus())
        self.Main_Window.updateStatusQComboBox.addItems(['']+mncRegistrarCore.listStatus())

        #populate user
        self.Main_Window.filterArtistQListWidget.clear()
        self.Main_Window.filterAssigneeQListWidget.clear()
        self.Main_Window.filterCoordinatorQListWidget.clear()
        self.Main_Window.filterSupervisorQListWidget.clear()
        self.Main_Window.updateArtistQComboBox.clear()
        self.Main_Window.updateCoordinatorQComboBox.clear()
        self.Main_Window.updateSupervisorQComboBox.clear()

        tempLis=[]
        for chk in mncRegistrarCore.listUserTable():tempLis.append(chk[1])

        self.Main_Window.filterArtistQListWidget.addItems(tempLis)
        self.Main_Window.filterAssigneeQListWidget.addItems(tempLis)
        self.Main_Window.filterCoordinatorQListWidget.addItems(tempLis)
        self.Main_Window.filterSupervisorQListWidget.addItems(tempLis)
        self.Main_Window.updateArtistQComboBox.addItems(['']+tempLis)
        self.Main_Window.updateCoordinatorQComboBox.addItems(['']+tempLis)
        self.Main_Window.updateSupervisorQComboBox.addItems(['']+tempLis)

        #populate complexity
        self.Main_Window.filterLayCplxQListWidget.clear()
        self.Main_Window.updateLayCplxQComboBox.clear()
        self.Main_Window.registerLayCplxQComboBox.clear()
        self.Main_Window.filterLayCplxQListWidget.addItems(mncRegistrarCore.listComplex())
        self.Main_Window.updateLayCplxQComboBox.addItems(['']+mncRegistrarCore.listComplex())
        self.Main_Window.registerLayCplxQComboBox.addItems(['']+mncRegistrarCore.listComplex())

        #clean rest of field
        self.Main_Window.registerTitleQLineEdit.clear()
        return

    def registerSingle(self):
        #get data
        newTitle=str(self.Main_Window.registerTitleQLineEdit.text())
        newDepartment=str(self.Main_Window.registerDepartmentQComboBox.currentText())
        newProject=str(self.Main_Window.registerProjectQComboBox.currentText())
        newBidHour=str(self.Main_Window.registerBidHourQComboBox.text())
        newComplex=str(self.Main_Window.registerLayCplxQComboBox.currentText())

        if newTitle=='' or newDepartment=='' or newProject=='' or newBidHour=='' or newComplex=='':
            QtGui.QMessageBox.warning(None, 'Error', 'Incomplete credential!',QtGui.QMessageBox.Ok)
        else:
            mncRegistrarCore.registerSingleSequence(title=newTitle,\
                                                    department=newDepartment,\
                                                    project=newProject,\
                                                    bidhour=newBidHour,\
                                                    complex=newComplex)
        self.refresh()
        return

    #populate table is not edited
    #filtration will be coded here
    def populateTable(self):
        global recordLis
        #get all recorded data
        recordLis=mncRegistrarCore.listSequenceTable()

        #fetch filter data
        idMin=self.Main_Window.filterIdMinQSpinBox.value()
        idMax=self.Main_Window.filterIdMaxQSpinBox.value()
        title=str(self.Main_Window.filterTitleQLineEdit.text())
        frameMin=str(self.Main_Window.filterFrameFromQSpinBox.value())
        frameMax=str(self.Main_Window.filterFrameToQSpinBox.value())
        bidMin=self.Main_Window.filterBidHourFromQSpinBox.value()
        bidMax=self.Main_Window.filterBidHourToQSpinBox.value()
        regDateMin=str(self.Main_Window.filterRegDateFromQSpinBox.text())
        regDateMax=str(self.Main_Window.filterRegDateToQSpinBox.text())
        dedDateMin=str(self.Main_Window.filterDedDateFromQSpinBox.text())
        dedDateMax=str(self.Main_Window.filterDedDateToQSpinBox.text())
        selectedDept=str(self.Main_Window.filterDepartmentQListWidget.selectedItems())
        selectedProj=str(self.Main_Window.filterProjectQListWidget.selectedItems())
        selectedStat=str(self.Main_Window.filterStatusQListWidget.selectedItems())
        selectedComp=str(self.Main_Window.filterLayCplxQListWidget.selectedItems())
        selectedArtist=str(self.Main_Window.filterArtistQListWidget.selectedItems())
        selectedAssign=str(self.Main_Window.filterAssigneeQListWidget.selectedItems())
        selectedCoord=str(self.Main_Window.filterCoordinatorQListWidget.selectedItems())
        selectedSuper=str(self.Main_Window.filterSupervisorQListWidget.selectedItems())

        #filtering fetched data
        allAsset=recordLis
        tempLis=[]
        writeLis=allAsset

        #filter idmin
        if idMin!=0:
            for check in writeLis:
                if check[0]>=idMin:
                    tempLis.append(check)
            writeLis=tempLis
            tempLis=[]

        #filter idmax
        if idMax!=0:
            for check in writeLis:
                if check[0]<=idMax:
                    tempLis.append(check)
            writeLis=tempLis
            tempLis=[]

        #filter title
        if title!='':
            for check in writeLis:
                if check[1].find(title)!=-1:
                    tempLis.append(check)
            writeLis=tempLis
            tempLis=[]

        #filter frameMin
        if frameMin!=0:
            for check in writeLis:
                if check[2]>=frameMin or check[2]==None:
                    tempLis.append(check)
            writeLis=tempLis
            tempLis=[]

        #filter frameMax
        if frameMax!=0:
            for check in writeLis:
                if check[2]<=frameMax or check[2]==None:
                    tempLis.append(check)
            writeLis=tempLis
            tempLis=[]

        #filter bidMin
        if bidMin!=0:
            for check in writeLis:
                if int(check[5])>=bidMin or check[5]==None:
                    tempLis.append(check)
            writeLis=tempLis
            tempLis=[]

        #filter bidMax
        if bidMax!=0:
            for check in writeLis:
                if int(check[5])<=bidMax or check[5]==None:
                    tempLis.append(check)
            writeLis=tempLis
            tempLis=[]

        #filter regDateMin
        if regDateMin!=0:
            if int(self.dateProcessor(regDateMin,encrypt=False)) != 20000101:
                for check in writeLis:
                    if int(self.dateProcessor(check[12],encrypt=False))>=int(self.dateProcessor(regDateMin,encrypt=False)) or check[12]==None:
                        tempLis.append(check)
                writeLis=tempLis
                tempLis=[]

        #filter regDateMax
        if regDateMax!=0:
            if int(self.dateProcessor(regDateMax,encrypt=False))!=20000101:
                for check in writeLis:
                    if int(self.dateProcessor(check[12],encrypt=False))<=int(self.dateProcessor(regDateMax,encrypt=False)) or check[12]==None:
                        tempLis.append(check)
                writeLis=tempLis
                tempLis=[]

        print writeLis

        #clearing table
        self.Main_Window.assignmentManagemerQTableWidget.setRowCount(0)
        self.Main_Window.assignmentManagemerQTableWidget.setRowCount(len(writeLis))

        #populating table
        cnt=0
        #(1, u'tester', u'0', u'AST', u'KIKO', u'0', None, None, None, None, None, u'A', u'2014-10-29 08:54:51', u'2014-10-29 08:54:51', u'2014-10-29 08:54:51', u'2014-10-29 08:54:51')
        for chk in recordLis:
            #determine color code
            colorRule=mncRegistrarCore.getColorCodeRule()
            statusColor=colorRule[0]
            preLateColor=colorRule[1]

            for color in statusColor:
                if color.find(chk[6])!=-1:
                    color=color[color.find(':')+1:]
                    color=color.split(',')
                    colorCode=QtGui.QColor(int(color[0]),int(color[1]),int(color[2]))
                else:
                    colorCode=QtGui.QColor(124,124,124)

            #Current date
            date=datetime.datetime.now()
            year=str(date.year)
            month=str(date.month)
            day=str(date.day)

            if len(month)==1:
                month='0'+month
            if len(day)==1:
                day='0'+day
            todayDate=int(year+month+day)

            #pre-late date
            s = "3 days ago"
            parsed_s = [s.split()[:2]]
            time_dict = dict((fmt,float(amount)) for amount,fmt in parsed_s)
            dt = datetime.timedelta(**time_dict)
            preLateDate =str(datetime.datetime.now() - dt)

            preLateDate=preLateDate[:preLateDate.find(' ')].replace('-','')

            if chk[14]!=None:
                #Assignment date
                deadlineDate=chk[14][:chk[14].find(' ')].replace('-','')
                if int(preLateDate)<int(deadlineDate) and int(todayDate)>int(deadlineDate):
                    preLateColors=preLateColor[0][preLateColor[0].find(':')+1:]
                    preLateColors=preLateColors.split(',')
                    fontColorCode=QtGui.QColor(int(preLateColors[0]),int(preLateColors[1]),int(preLateColors[2]))

                #Late
                elif int(todayDate)>int(deadlineDate):
                    lateColor=preLateColor[1][preLateColor[1].find(':')+1:]
                    lateColor=lateColor.split(',')
                    fontColorCode=QtGui.QColor(int(lateColor[0]),int(lateColor[1]),int(lateColor[2]))

                else:
                    #Standard system color
                    fontColorCode=QtGui.QColor(0,0,0)
            else:
                fontColorCode=QtGui.QColor(0,0,0)

            #writing to table
            item=QtGui.QTableWidgetItem(str(chk[0]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,0,item)

            item=QtGui.QTableWidgetItem(str(chk[1]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,1,item)

            item=QtGui.QTableWidgetItem(str(chk[2]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,2,item)

            item=QtGui.QTableWidgetItem(str(chk[3]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,3,item)

            item=QtGui.QTableWidgetItem(str(chk[4]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,4,item)

            item=QtGui.QTableWidgetItem(str(chk[5]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,5,item)

            item=QtGui.QTableWidgetItem(str(chk[6]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,6,item)

            item=QtGui.QTableWidgetItem(str(chk[7]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,7,item)

            item=QtGui.QTableWidgetItem(str(chk[8]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,8,item)

            item=QtGui.QTableWidgetItem(str(chk[9]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,9,item)

            item=QtGui.QTableWidgetItem(str(chk[10]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,10,item)

            item=QtGui.QTableWidgetItem(str(chk[11]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,11,item)

            item=QtGui.QTableWidgetItem(str(chk[12]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,12,item)

            item=QtGui.QTableWidgetItem(str(chk[13]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,13,item)

            item=QtGui.QTableWidgetItem(str(chk[14]))
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,14,item)

            item=QtGui.QTableWidgetItem(str(chk[15]))
            print str(chk[15])
            item.setBackground(colorCode)
            item.setTextColor(fontColorCode)
            self.Main_Window.assignmentManagemerQTableWidget.setItem(cnt,15,item)
            cnt+=1
        self.Main_Window.assignmentManagemerQTableWidget.resizeColumnsToContents()
        return

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = registrarSequence()
    sys.exit(app.exec_())