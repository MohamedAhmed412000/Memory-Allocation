from tkinter import *
from tkinter import ttk
from random import randint
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt                 # This is to add graph to gui
import matplotlib.patches as patches            # This is to add text on graph
##########################################################################
#global variables
FrameNo = 0     #To navigate between frames
HoleNo = 0      #To get num of holes
SegmentNo = 0
lstReal = []
lstAddress = []
Start = 1
End = 29
ind = []
CurProcess = 0
HoleUsed = 0
Message = ""
#########################################################################
#Global variables to algorithm
flgDeallocate = 0                               # Deallocate
DeallocatedProcess = ""
ProcessNo = 1                                   #n is no of processes
MemorySize = 0                                  #size is memory size
NumHoles = 0
lstHoleBase = []               #[1000, 1200, 1300, 1500, 1700]  #hstart is number of starting adreeses holes
lstHoleLimit = []              #[100, 100, 100,  150, 200]      #hsize is number of size of holes
lstSegments = []               #[2, 2, 3, 2, 3] #lstSegments is a list have the number of segment for each process
lstSegName = [[]]                #lstSegsize  is a list of lists with number of the processes  #[[30, 20], [20, 20], [10, 20, 30], [20, 40], [10, 10, 10]]
lstSegSize = [[]]
lstSegAddress = []             #segaddresses  is a list of lists with number of the processes #it must have number of n empty lists inside the list
lstOldSize = []
lstOldAddress = []
##########################################################################
#Functions
#Functions To hide
def hide(widget):
    widget.place(y=1000)
def hideAll():
    hide(firstFrame)
    hide(holesFrame)
    hide(processFrame)
    hide(allocationFrame)
def Get_Allocation_Type():
    #Do Nothing
    exit()

#Function to input data
def initial():
    hideAll()
    get_status()
    firstFrame.place(x=10, y=0, width=480, height=95)

#Get Holes Data
def get_unit(*args):
    if UnitType.get() == "Bytes":
        return "B"
    elif UnitType.get() == "KBytes":
        return "KB"
    else:
        return "MB"
def get_primary_data():
    global MemorySize, NumHoles, UnitType, units
    if entMemSize.get() == "":
        MemorySize = randint(100, 500)
        entMemSize.insert(0, str(MemorySize))
    else:
        MemorySize = int(entMemSize.get())
    if entNoHoles.get() == "":
        NumHoles = randint(3, 7)
        entNoHoles.insert(4, str(NumHoles))
    else:
        NumHoles = int(entNoHoles.get())
    if UnitType.get() == units[0]:
        UnitType.set(units[2])
    entMemSize.configure(state=['disabled'])
    entNoHoles.configure(state=['disabled'])
    btnNoHoles.configure(state=['disabled'])
    holesFrame.place(x=10, y=100, width=480, height=115)
    hide(btnProcess)
    Units_menu.configure(state=['disabled'])
def Next():
    global NumHoles, HoleNo, lstHoleBase, lstHoleLimit
    if entHoleBase.get() == "":
        lstHoleBase.append(randint(0, MemorySize))
    else:
        lstHoleBase.append(int(entHoleBase.get()))
    if entHoleLimit.get() == "":
        lstHoleLimit.append(randint(0, int(MemorySize / NumHoles)))
    else:
        lstHoleLimit.append(int(entHoleLimit.get()))
    entHoleBase.delete(0, 'end')
    entHoleLimit.delete(0, 'end')
    HoleNo = HoleNo + 1
    HoleNumber.set("Hole Num. " + str(HoleNo))
    lblHole.configure(text=HoleNumber.get())
    if len(lstHoleBase) == NumHoles:
        entHoleBase.configure(state=['disabled'])
        entHoleLimit.configure(state=['disabled'])
        hide(btnNext)
        btnProcess.place(x=360, y=60, width=90)
def get_process():
    btnProcess.configure(state=['disabled'])
    processFrame.place(x=10, y=222, width=480, height=180)
    lstSegAddress.append([])
    hide(lblSegment)
    hide(lblSegName)
    hide(entSegName)
    hide(lblSegSize)
    hide(entSegSize)
    hide(btnNewSegment)
    hide(btnNewProcess)
    hide(btnSubmit)

#Get Processes Data
def get_segment_data():
    global lstSegments, SegmentNo, ProcessNo
    if entNoSegment.get() == "":
        lstSegments.append(3)
    else:
        lstSegments.append(int(entNoSegment.get()))
    entNoSegment.delete(0, 'end')
    entNoSegment.insert(0, str(lstSegments[ProcessNo-1]))
    entNoSegment.configure(state=['disabled'])
    btnNoSegment.configure(state=['disabled'])
    SegmentNumber.set("Segment Num. " + str(SegmentNo))
    lblSegment.configure(text=SegmentNumber.get())
    lblSegment.place(x=40, y=60)
    lblSegName.place(x=40, y=85)
    entSegName.place(x=140, y=87, width=80)
    entSegName.configure(state=['!disabled'])
    lblSegSize.place(x=260, y=85)
    entSegSize.place(x=360, y=87, width=80)
    entSegSize.configure(state=['!disabled'])
    btnNewSegment.place(x=220, y=125, width=90)
    btnNewSegment.configure(state=['!disabled'])
def new_segment():
    global SegmentNo, lstSegments, lstSegName, lstSegSize, ProcessNo
    if entSegName.get() == "":
        lstSegName[ProcessNo-1].append("Segment " + str(SegmentNo))
    else:
        lstSegName[ProcessNo-1].append(entSegName.get())
    if entSegSize.get() == "":
        lstSegSize[ProcessNo-1].append(randint(1, 100))
    else:
        lstSegSize[ProcessNo-1].append(int(entSegSize.get()))
    SegmentNo = SegmentNo + 1
    SegmentNumber.set("Segment Num. " + str(SegmentNo))
    lblSegment.configure(text=SegmentNumber.get())
    entSegName.delete(0, 'end')
    entSegSize.delete(0, 'end')
    if SegmentNo == lstSegments[ProcessNo-1]:
        lstSegName.append([])
        lstSegSize.append([])
        entSegName.configure(state=['disabled'])
        entSegSize.configure(state=['disabled'])
        btnNewSegment.configure(state=['disabled'])
        btnSubmit.configure(state=['!disabled'])
        btnSubmit.place(x=330, y=125, width=120)
def submit_process():
    btnSubmit.configure(state=['disabled'])
    btnNewProcess.place(x=10, y=125, width=100)
    allocationFrame.place(x=10, y=410, width=480, height=60)
def new_process():
    global ProcessNo, SegmentNo
    ProcessNo = ProcessNo + 1
    lstSegAddress.append([])
    SegmentNo = 0
    hide(btnNewProcess)
    ProcessNumber.set("Process Num. " + str(ProcessNo-1))
    lblProcess.configure(text=ProcessNumber.get())
    entNoSegment.configure(state=['!disabled'])
    entNoSegment.delete(0, 'end')
    btnNoSegment.configure(state=['!disabled'])
    hide(allocationFrame)

#Get Allocation Type
def get_allocation_type(*args):
    global allocType, btnAllocate, btnNewProcess
    btnAllocate.place(x=335, y=5, width=100)
    btnNewProcess.configure(state=['disabled'])
    return allocType.get()
def allocate():
    global flgDeallocate, allocation_menu
    allocation_frame()
    old_processes()
    if get_allocation_type() == "First Fit":
        first_fit()     #First Fit
    elif get_allocation_type() == "Worst Fit":
        worst_fit()     #Worst Fit
    else:
        best_fit()      #Best Fit
    b = len(lstHoleLimit)
    flgDeallocate += 1
    for j in range(0, b):
        for i in range(0, b):
            if lstHoleLimit[i] <= 0:
                b = b - 1
                lstHoleLimit.pop(i)
                lstHoleBase.pop(i)
                break
    get_dprocesses_list()
    btnAllocate.configure(state=['disabled'])
    allocation_menu.configure(state=['disabled'])
    merge_holes()
    draw(0, 100, 1, 99)
    get_status()
def merge_holes():
    global lstHoleLimit, lstHoleBase
    l = len(lstHoleLimit)
    for i in range(0, l):
        for j in range(0, l):
            if lstHoleBase[j] == lstHoleLimit[i]+lstHoleBase[i]:
                lstHoleLimit[i] += lstHoleLimit[j]
                lstHoleLimit[j] = 0
    for k in range(0, l):
        for q in range(0, l):
            if lstHoleLimit[q] <= 0:
                lstHoleLimit.pop(q)
                lstHoleBase.pop(q)
                l = l - 1
                break

#get_real_Positions
def get_real_yposition(realstart, realend, virtualstart, virtualend, virtualnum):
    return realend - ((realend - realstart) * (virtualend - virtualnum) / (virtualend - virtualstart))
def draw(Begin, Finish, Start, End):
    global MemorySize, ProcessNo, lstReal, lstAddress, fig, ax
    ax.clear()
    rect.clear()
    lstAddress.clear()
    lstReal.clear()
    lstAllAddress = [lstOldAddress] + [lstHoleBase] + lstSegAddress
    ax.set_xlim(0, 30)
    ax.set_ylim(Begin, Finish)
    for i in range(0, len(lstAllAddress)):
        for j in range(0, len(lstAllAddress[i])):
            lstAddress.append(lstAllAddress[i][j])
            lstReal.append(get_real_yposition(Start, End, 0, MemorySize, lstAllAddress[i][j]))
    lstAddress.append(MemorySize)
    lstReal.append(End)
    ax.set_yticklabels(lstAddress)
    ax.set_yticks(lstReal)
    ax.set_xticks([5, 25])
    #gnt.grid(True)
    # Draw Old Process First
    for i in range(0, len(lstOldAddress)):
        rect.append(patches.Rectangle((5, get_real_yposition(Start, End, 0, MemorySize, lstOldAddress[i])), 20, get_real_yposition(Start, End, 0, MemorySize, lstOldSize[i])-Start, linewidth=1, edgecolor='black', facecolor='none'))
        ax.add_patch(rect[i])
        ax.text(15, get_real_yposition(Start, End, 0, MemorySize, (lstOldSize[i] + 2 * lstOldAddress[i]) / 2), ("OldProcess " + str(i)), horizontalalignment='center', verticalalignment='center', fontsize=get_font_size((get_real_yposition(Start, End, 0, MemorySize, lstOldSize[i])-Start)))
    # Draw Holes
    for j in range(0, len(lstHoleBase)):
        rect.append(patches.Rectangle((5, get_real_yposition(Start, End, 0, MemorySize, lstHoleBase[j])), 20, get_real_yposition(Start, End, 0, MemorySize, lstHoleLimit[j])-Start, linewidth=1, edgecolor='black', facecolor='none'))
        ax.add_patch(rect[len(lstOldAddress)+j])
        ax.text(15, get_real_yposition(Start, End, 0, MemorySize, (lstHoleLimit[j] + 2 * lstHoleBase[j]) / 2), "Hole " + str(j), horizontalalignment='center', verticalalignment='center', fontsize=get_font_size((get_real_yposition(Start, End, 0, MemorySize, lstHoleLimit[j])-Start)))
    # Draw Segments
    count = 0
    for h in range(0, ProcessNo):
        for k in range(0, len(lstSegAddress[h])):
            rect.append(patches.Rectangle((5, get_real_yposition(Start, End, 0, MemorySize, lstSegAddress[h][k])), 20, get_real_yposition(Start, End, 0, MemorySize, lstSegSize[h][k])-Start, linewidth=1, edgecolor='black', facecolor='none'))
            ax.add_patch(rect[len(lstOldAddress)+len(lstHoleBase)+count])
            count += 1
            ax.text(15, get_real_yposition(Start, End, 0, MemorySize, (lstSegSize[h][k] + 2 * lstSegAddress[h][k]) / 2), "P" + str(h) + ": " + lstSegName[h][k], horizontalalignment='center', verticalalignment='center', fontsize=get_font_size(get_real_yposition(Start, End, 0, MemorySize, lstSegSize[h][k])-Start))
    canvas.draw()
    canvas.get_tk_widget().place(x=0, y=0, width=470, height=450)
def get_font_size(y_diff):
    if 0 <= y_diff < 1:
        return 6
    elif 1 <= y_diff < 2:
        return 8
    elif 2 <= y_diff < 3:
        return 9
    elif 3 <= y_diff < 4:
        return 10
    elif 4 <= y_diff < 5:
        return 11
    else:
        return 14
########################################
"""modified"""
def old_processes():
    global MemorySize, lstHoleBase, lstHoleLimit, lstOldSize, lstOldAddress
    temp1 = lstHoleBase.copy()
    temp2 = lstHoleLimit.copy()
    if temp1[mini_index(temp1)] == 0:
        address = temp2[mini_index(temp1)]
    else:
        address = 0
    l = len(lstHoleBase)
    for i in range(0, l):
        m = mini_index(temp1)
        lstOldSize.append(temp1[m] - address)
        lstOldAddress.append(address)
        address = temp1[m]+temp2[m]
        temp1.remove(temp1[m])
        temp2.remove(temp2[m])
    if lstHoleBase[maxi_index(lstHoleBase)] + lstHoleLimit[maxi_index(lstHoleBase)] != MemorySize:
        index = maxi_index(lstHoleBase)
        lstOldAddress.append(lstHoleBase[index]+lstHoleLimit[index])
        lstOldSize.append(MemorySize-lstOldAddress[-1])
    b = len(lstOldAddress)
    for j in range(0, b):
        for i in range(0, b):
            if lstOldSize[i] <= 0:
                b = b - 1
                lstOldSize.pop(i)
                lstOldAddress.pop(i)
                break
def mini_index(a):
    min_index = a.index(min(a))
    return min_index
def maxi_index(a):
    max_index = a.index(max(a))
    return max_index
def search(a, arr):
    for i in range(0, len(arr)):
        if arr[i] == a:
            return i
    return -1
def minumum(num ,arr):
    arr1 = []
    for i in range(len(arr)):
        arr1.append([arr[i],i])
    arr1.sort()
    for i in range(len(arr)):
        if arr1[i][0] >= num:
            return arr1[i][1]
    return -1
def maximum(num,arr):
    arr1 = []
    for i in range(len(arr)):
        arr1.append([arr[i],i])
    arr1.sort(reverse=True)
    for i in range(len(arr)):
        if arr1[i][0] >= num:
            return arr1[i][1]
    return -1
#################################################################
#Allocation Algorithms
def first_fit():
    global ProcessNo, lstSegments, lstHoleLimit, lstSegSize, lstHoleBase,lstSegAddress, CurProcess, Message
    m = 0
    flag = 0
    while m < ProcessNo:
        l = lstSegments[m] #len(segsize[m])
        for j in range(0, l):  # first it will be 0 then it will be segsize[0]
            h = len(lstHoleLimit)
            flag = 0
            for i in range(0, h):
                if lstHoleLimit[i] >= lstSegSize[m][j]:
                    lstSegAddress[m].append(lstHoleBase[i])
                    lstHoleBase[i] = lstHoleBase[i] + lstSegSize[m][j]	#+1 was removed
                    lstHoleLimit[i] = lstHoleLimit[i] - lstSegSize[m][j]
                    flag = 1
                    break
            CurProcess += 1
            if flag == 0:
                Message = "Segment Num "+str(j)+" in Process Num "+str(m)+" can't fit in any hole"
                messagebox.showinfo(title="ERROR", message=Message)
                break
                break

        j = 0
        m = m + 1
def best_fit():
    global ProcessNo, lstSegments, lstHoleLimit, lstSegSize, lstHoleBase, lstSegAddress, CurProcess
    m = 0
    while m < ProcessNo:
        l = lstSegments[m]#len(segsize[m])
        CurProcess += 1
        for j in range(0, l):
            index = minumum(lstSegSize[m][j],lstHoleLimit)
            if index != -1:
                lstSegAddress[m].append(lstHoleBase[index])
                lstHoleBase[index] = lstHoleBase[index] + lstSegSize[m][j]	#+1 was removed
                lstHoleLimit[index] = lstHoleLimit[index] - lstSegSize[m][j]
            else:
                Message = "Segment Num " + str(j) + " in Process Num " + str(m) + " can't fit in any hole"
                messagebox.showinfo(title="ERROR", message=Message)
                break
                break
        j = 0
        m = m + 1
def worst_fit():
    global ProcessNo, lstSegments, lstHoleLimit, lstSegSize, lstHoleBase, lstSegAddress, CurProcess
    m = 0
    while m < ProcessNo:
        l = lstSegments[m] #len(segsize[m])
        CurProcess += 1
        for j in range(0, l):
            index = maximum(lstSegSize[m][j],lstHoleLimit)
            if index != -1:
                lstSegAddress[m].append(lstHoleBase[index])
                lstHoleBase[index] = lstHoleBase[index] + lstSegSize[m][j]	#+1 was removed
                lstHoleLimit[index] = lstHoleLimit[index] - lstSegSize[m][j]
            else:
                Message = "Segment Num " + str(j) + " in Process Num " + str(m) + " can't fit in any hole"
                messagebox.showinfo(title="ERROR", message=Message)
                break
                break
        j = 0
        m = m + 1
##########################################################################
#Deallocation Algorithms
def get_dprocesses_list():
    global flgDeallocate, Processes, lstOldAddress, lstSegAddress, Processes_menu, lblProcessDeallocate, Process
    if flgDeallocate == 1:
        for i in range(0, len(lstOldAddress)):
            Processes.append("OldProcess "+str(i))
        for i in range(0, len(lstSegAddress)):
            Processes.append("Process Num "+str(i))
        Processes_menu = ttk.OptionMenu(DeallocationFrame, Process, *Processes)
        Processes_menu.place(x=188, y=7)
        lblProcessDeallocate.place(x=10, y=10)
        Process.trace('w', get_dprocess)
def get_dprocess(*args):
    global Process, btnDeallocate
    btnDeallocate.place(x=320, y=5, width=140)
    return Process.get()
def deallocate(index):
    global ProcessNo, lstSegments, lstHoleLimit, lstSegSize, lstHoleBase, lstSegAddress
    temp1 = list(lstSegAddress) #segaddress.copy()
    temp2 = list(lstSegSize)#segsize.copy()
    for i in range(0, ProcessNo):
        if i == index:
            for j in range(0, len(lstSegSize[i])):
                lstHoleBase.append(temp1[i][j])
                lstHoleLimit.append(temp2[i][j])
            lstSegAddress.pop(i)
            lstSegSize.pop(i)
            lstSegments.pop(i)
            ProcessNo = ProcessNo - 1
def deallocate_old(index):
    global lstHoleLimit, lstHoleBase, lstOldAddress, lstOldSize
    for i in range(0, len(lstOldSize)):
        if i == index:
            lstHoleBase.append(lstOldAddress[i])
            lstHoleLimit.append(lstOldSize[i])
            lstOldAddress.pop(i)
            lstOldSize.pop(i)
def Deallocate_Process():
    global Process, lstOldAddress, btnDeallocate, Processes_menu, CurProcess
    index = search(get_dprocess(), Processes)
    if index != -1:
        if index <= len(lstOldAddress):
            deallocate_old(index-1)
        else:
            deallocate(index-len(lstOldAddress)-1)
        allocation_frame()
        merge_holes()
        CurProcess -= 1
        draw(0, 100, 1, 99)
        get_status()
        Processes_menu.configure(state=['disabled'])
        btnDeallocate.configure(state=['disabled'])
##########################################################################
#Status Data
def get_status():
    global lblCurrentProcess, lblHoleUsed, lblHoleAvailable, lblUsageMemory, lblMessage, CurProcess, HoleUsed, MemorySize, lstOldSize, lstSegSize, lstHoleLimit, Message
    lblCurrentProcess.place(x=10, y=20)
    lblHoleUsed.place(x=10, y=45)
    lblHoleAvailable.place(x=10, y=70)
    lblUsageMemory.place(x=10, y=95)
    lblMessage.place(x=10, y=120)
    valCurrentProcess = str(CurProcess) + " Processes"
    lblCPVal = ttk.Label(StatusFrame, text=valCurrentProcess, foreground="green")
    lblCPVal.place(x=170, y=20)
    HoleUsed = 0
    for i in range(0, len(lstSegSize)):
        HoleUsed += sum(lstSegSize[i])
    valHoleUsed = str(HoleUsed) + " " + get_unit()
    lblHUVal = ttk.Label(StatusFrame, text=valHoleUsed, foreground="red")
    lblHUVal.place(x=170, y=45)
    valHoleAvailable = str(sum(lstHoleLimit)) + " " + get_unit()
    lblHUVal = ttk.Label(StatusFrame, text=valHoleAvailable, foreground="green")
    lblHUVal.place(x=170, y=70)
    if MemorySize != 0:
        PercentageMemory = 100 - (sum(lstHoleLimit)/MemorySize)*100
    else:
        PercentageMemory = 0
    valUsageMemory = str(PercentageMemory) + " %"
    lblPMVal = ttk.Label(StatusFrame, text=valUsageMemory)
    if PercentageMemory > 50:
        lblPMVal.configure(foreground = "red")
    else:
        lblPMVal.configure(foreground="green")
    lblPMVal.place(x=185, y=95)
    if Message == "":
        if MemorySize != 0:
            lblMSGVal = ttk.Label(StatusFrame, text="Done (No Problem Occurs)", foreground="green")
            lblMSGVal.place(x=75, y=120)
    else:
        lblMSGVal = ttk.Label(StatusFrame, text=Message, foreground="red")
        Message = ""
        lblMSGVal.place(x=75, y=120)
##########################################################################
#Create GUI App
root = Tk()

#set size and the address
root.title("Memory Allocation GUI")
root.geometry("500x480")

#Add Menubar##########################################################
#functions for Navigating in Menubar
def allocation_frame():
    global FrameNo
    if FrameNo == 1:
        frmInput.place_forget()
    elif FrameNo == 3:
        frmStatus.place_forget()
    elif FrameNo == 4:
        frmDeallocation.place_forget()
    FrameNo = 2
    frmAllocation.place(x=0, y=0, width=600, height=600)
def deallocation_frame():
    global FrameNo
    if FrameNo == 1:
        frmInput.place_forget()
    elif FrameNo == 2:
        frmAllocation.place_forget()
    elif FrameNo == 3:
        frmStatus.place_forget()
    FrameNo = 4
    frmDeallocation.place(x=0, y=0, width=600, height=600)
def input_frame():
    global FrameNo
    if FrameNo == 2:
        frmAllocation.place_forget()
    elif FrameNo == 3:
        frmStatus.place_forget()
    elif FrameNo == 4:
        frmDeallocation.place_forget()
    FrameNo = 1
    frmInput.place(x=0, y=0, width=600, height=600)
def status_frame():
    global FrameNo
    if FrameNo == 1:
        frmInput.place_forget()
    elif FrameNo == 2:
        frmAllocation.place_forget()
    elif FrameNo == 4:
        frmDeallocation.place_forget()
    FrameNo = 3
    frmStatus.place(x=0, y=0, width=600, height=600)
####################################################################
MenuBar = Menu(root)
MenuBar.add_cascade(label="Input Data", command=input_frame)
MenuBar.add_cascade(label="Allocation", command=allocation_frame)
MenuBar.add_cascade(label="Status", command=status_frame)
MenuBar.add_cascade(label="Deallocation", command=deallocation_frame)
root.config(menu=MenuBar)
#####################################################################

#Frames
frmInput = Frame(root)
frmInput.place(x=0, y=0, width=600, height=600)
frmAllocation = Frame(root)
frmStatus = Frame(root)
frmDeallocation = Frame(root)

######################## Input_Frame ############################
#PrimaryFrame
firstFrame = ttk.LabelFrame(frmInput, text=" Primary Data ")
lblMemSize = ttk.Label(firstFrame, text="Memory Size :")
lblMemSize.place(x=10, y=10)
entMemSize = ttk.Entry(firstFrame)
entMemSize.place(x=95, y=12, width=100)
#lblUnitMemSize = ttk.Label(firstFrame, text="(in KBs)")
units = ["Custom Unit", "Bytes", "KBytes", "MBytes"]
UnitType = StringVar()
Units_menu = ttk.OptionMenu(firstFrame, UnitType, *units)
UnitType.trace('w', get_unit)
Units_menu.place(x=300, y=5)
#lblUnitMemSize.place(x=200, y=10)
lblNoHoles = ttk.Label(firstFrame, text="Number of Holes :")
lblNoHoles.place(x=10, y=40)
entNoHoles = ttk.Entry(firstFrame)
entNoHoles.place(x=120, y=42, width=100)
btnNoHoles = ttk.Button(firstFrame, text="Enter Holes Data")
btnNoHoles.config(command=lambda: get_primary_data())
btnNoHoles.place(x=300, y=40, width=150)

#Holes Data
holesFrame = ttk.LabelFrame(frmInput, text=" Holes Data ")
HoleNumber = StringVar()
HoleNumber.set("Hole Num. " + str(HoleNo))
lblHole = ttk.Label(holesFrame, text=HoleNumber.get())
lblHole.place(x=10, y=2)
lblHoleBase = ttk.Label(holesFrame, text="Hole Base Address :")
lblHoleBase.place(x=10, y=25)
entHoleBase = ttk.Entry(holesFrame)
entHoleBase.place(x=125, y=27, width=100)
lblHoleLimit = ttk.Label(holesFrame, text="Hole limit :")
lblHoleLimit.place(x=280, y=25)
entHoleLimit = ttk.Entry(holesFrame)
entHoleLimit.place(x=350, y=27, width=100)
btnNext = ttk.Button(holesFrame, text="Next Hole")
btnNext.config(command=Next)
btnNext.place(x=250, y=60, width=90)
btnProcess = ttk.Button(holesFrame, text="Submit Holes")
btnProcess.place(x=360, y=60, width=90)
btnProcess.config(command=get_process)

#Processes Data
processFrame = ttk.LabelFrame(frmInput, text=" Processes Data ")
processFrame.place(x=10, y=222, width=480, height=180)
ProcessNumber = StringVar()
ProcessNumber.set("Process Num. " + str(ProcessNo-1))
lblProcess = ttk.Label(processFrame, text=ProcessNumber.get())
lblProcess.place(x=10, y=5)
lblNoSegment = ttk.Label(processFrame, text="Number of Segments :")
lblNoSegment.place(x=10, y=30)
entNoSegment = ttk.Entry(processFrame)
entNoSegment.place(x=140, y=32, width=80)
btnNoSegment = ttk.Button(processFrame, text="Submit")
btnNoSegment.place(x=250, y=30, width=75)
btnNoSegment.configure(command=get_segment_data)
SegmentNumber = StringVar()
SegmentNumber.set("Segment Num. " + str(SegmentNo))
lblSegment = ttk.Label(processFrame, text=SegmentNumber.get())
lblSegment.place(x=40, y=60)
lblSegName = ttk.Label(processFrame, text="Segment Name :")
lblSegName.place(x=40, y=85)
entSegName = ttk.Entry(processFrame)
entSegName.place(x=140, y=87, width=80)
lblSegSize = ttk.Label(processFrame, text="Segment Size :")
lblSegSize.place(x=260, y=85)
entSegSize = ttk.Entry(processFrame)
entSegSize.place(x=360, y=87, width=80)
btnNewSegment = ttk.Button(processFrame, text="Next Segment")
btnNewSegment.place(x=220, y=125, width=90)
btnNewSegment.configure(command=new_segment)
btnSubmit = ttk.Button(processFrame, text="Submit Process")
btnSubmit.place(x=330, y=125, width=120)
btnSubmit.configure(command=submit_process)
btnNewProcess = ttk.Button(processFrame, text="New Process")
btnNewProcess.place(x=10, y=125, width=100)
btnNewProcess.configure(command=new_process)

#Allocation Type
allocationFrame = ttk.LabelFrame(frmInput, text=" Allocation Type ")
allocationFrame.place(x=10, y=410, width=480, height=60)
options = ["Allocation Type", "First Fit", "Best Fit", "Worst Fit"]
allocType = StringVar()
allocation_menu = ttk.OptionMenu(allocationFrame, allocType, *options)
allocType.trace('w', get_allocation_type)
allocation_menu.place(width=150, height=25, x=10, y=5)
btnAllocate =ttk.Button(allocationFrame, text="Allocate Process")
btnAllocate.configure(command=allocate)
##################################################################
#Draw Area Frame
DrawAreaFrame = ttk.LabelFrame(frmAllocation, text=" Draw Area ")
DrawAreaFrame.place(x=10, y=0, width=480, height=470)
#fig = Figure(figsize=(5,4), dpi=100)
#t = np.arange(0, 3, .01)
#fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
#canvas = FigureCanvasTkAgg(fig, master=DrawAreaFrame)
#canvas.draw()
#canvas.get_tk_widget().place(x=-20, y=-10)
#fig, gnt = plt.subplots()
fig = plt.figure()
ax = fig.add_subplot()
fig.subplots_adjust(top=0.986, right=0.986, left=0.138, bottom=0.095)  # to edit the positions of the plot borders
canvas = FigureCanvasTkAgg(fig, DrawAreaFrame)
toolbar = NavigationToolbar2Tk(canvas, DrawAreaFrame)
rect = []
toolbar.update()
#canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#fig, gnt = plt.subplots()
#canvas = FigureCanvasTkAgg(fig, DataAreaFrame)
#toolbar = NavigationToolbar2Tk(canvas, DataAreaFrame)
#def Draw():
#    global toolbar, canvas, fig, gnt
#canvas.draw()
#canvas.get_tk_widget().place(x=5, y=10, width=468, height=225)

##################################################################
#Status Frame
StatusFrame = ttk.LabelFrame(frmStatus, text=" Status ")
StatusFrame.place(x=10, y=0, width=480, height=470)
strCurrentProcess = StringVar()
strCurrentProcess.set("Current Process in Memory :")
strHoleUsed = StringVar()
strHoleUsed.set("Total Hole Size Used :")
strHoleAvailable = StringVar()
strHoleAvailable.set("Total Hole Size Available :")
strUsageMemory = StringVar()
strUsageMemory.set("Percentage Usage of Memory :")
strMessage = StringVar()
strMessage.set("Message :")
lblCurrentProcess = ttk.Label(StatusFrame, text=strCurrentProcess.get())
lblHoleUsed = ttk.Label(StatusFrame, text=strHoleUsed.get())
lblHoleAvailable = ttk.Label(StatusFrame, text=strHoleAvailable.get())
lblUsageMemory = ttk.Label(StatusFrame, text=strUsageMemory.get())
lblMessage = ttk.Label(StatusFrame, text=strMessage.get())
##################################################################
#Deallocation Frame
DeallocationFrame = ttk.LabelFrame(frmDeallocation, text=" Deallocation ")
DeallocationFrame.place(x=10, y=0, width=480, height=470)
lblProcessDeallocate = ttk.Label(DeallocationFrame, text="Choose Process to deallocate :")
Processes = ["Choose Process"]
Process = StringVar()
Processes_menu = ttk.OptionMenu(DeallocationFrame, Process, *Processes)
btnDeallocate = ttk.Button(DeallocationFrame, text="Deallocate Process")
btnDeallocate.configure(command=Deallocate_Process)
##################################################################
initial()
root.mainloop()