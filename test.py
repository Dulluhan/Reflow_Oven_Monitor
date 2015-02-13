import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button,CheckButtons
import sys, time, math, serial, threading
from matplotlib._png import read_png
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, \
     AnnotationBbox
x=0
xsize=400
pause = True
profiles = [[0,90,180,210,240,340],[20,150,210,235,240,20],
            [0,90,180,210,240,340],[20,150,180,208,180,20]]

global showerror
showerror = False

ser = serial.Serial(
 port='COM4',
 baudrate=115200,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_TWO,
 bytesize=serial.EIGHTBITS
)
ser.isOpen()

def data_gen():
    global t
    t = data_gen.t
    while (True):
       if pause:
           if (ser.readline() > 25 ):
    	       t+=1
    	       val=ser.readline()
    	       #time.sleep(1)
    	       setvis (not l1.get_visible())
           elif (ser.readline() < 25):
               t = 0
       yield t, val


def run(data):
    t,y = data
    # update the data
    if (t>-1):
        xdata.append(t)
        ydata.append(y)
        if t>xsize: # Scroll to the left.
            ax.set_xlim(t-xsize, t)
        line.set_data(xdata, ydata)
        if t>350:
            global pause
            pause = not pause
    return line,

def on_close_figure(event):
    sys.exit(0)

def onclick(event):
    global pause
    pause = not pause
	#for pausing the graph when we need to

def exit(event):
    mng.full_screen_toggle()

def quit(event):
    sys.exit(0)

def func(label):
    if label == "SAC305":
	p0.set_visible(not p0.get_visible())
	a0.set_visible(not a0.get_visible())
    elif label == "63Sn/37Pb":
	p1.set_visible(not p1.get_visible())
	a1.set_visible(not a1.get_visible())
    plt.draw()

def show(event):
	l1.set_visible(not l1.get_visible())
	l2.set_visible(not l2.get_visible())
	plt.draw()

def setvis (condition):
       if (condition == True):
       		if (t > 90):
			e0.set_visible(True)
       		if (t > 180):
			e1.set_visible(True)
       		if (t > 210):
			e2.set_visible(True)
       		if (t > 240):
			e3.set_visible(True)
       else:
		e0.set_visible(False)
		e1.set_visible(False)
		e2.set_visible(False)
		e3.set_visible(False)
       plt.draw()

def label (event):
    	l3.set_visible(not l3.get_visible())
    	l4.set_visible(not l4.get_visible())
    	n0.set_visible(not n0.get_visible())
    	n1.set_visible(not n1.get_visible())
    	n2.set_visible(not n2.get_visible())
    	n3.set_visible(not n3.get_visible())
    	n4.set_visible(not n4.get_visible())
    	n5.set_visible(not n5.get_visible())
    	n6.set_visible(not n6.get_visible())
    	n7.set_visible(not n7.get_visible())
    	n8.set_visible(not n8.get_visible())
        plt.draw()

##################### INITIAL ###########################
data_gen.t = -1
fig = plt.figure()
fig.canvas.mpl_connect('close_event', on_close_figure)
ax = fig.add_subplot(111)
plt.subplots_adjust(bottom=0.2) #adjust margin on the bottom
plt.title('Inside Oven Temperature') #title
plt.ylabel('Temperature') #y label
plt.xlabel('Time') #x label
line, = ax.plot([], [], lw=2)
ax.set_ylim(0, 300)
ax.set_xlim(0, xsize)
ax.grid()
xdata, ydata = [], []

################## BUTTONS #################
axpause = plt.axes([0.67, 0.05, 0.05, 0.05]) #button position "a seperature plot"
bpause = Button(axpause,'Pause',color = u'0.85', hovercolor = u'0.95') #create button
bpause.on_clicked(onclick) #set action on click
fig.canvas.mpl_connect('pause_event',onclick) #add global event

axexit = plt.axes([0.73, 0.05, 0.08, 0.05]) #toggle button
bexit = Button(axexit,'Toggle Screen',color = u'0.85', hovercolor = u'0.95')
bexit.on_clicked(exit)
fig.canvas.mpl_connect('exit_event',exit)

axquit = plt.axes([0.82, 0.05, 0.05, 0.05])
bquit = Button(axquit,'Quit', color = '#F0B2B2', hovercolor = '#E06666')
bquit.on_clicked(quit)
fig.canvas.mpl_connect("quit_event",quit)

axshow = plt.axes([0.59,0.05,0.07,0.05])
bshow = Button(axshow,'Show Error', color = u'0.85', hovercolor = u'0.95')
bshow.on_clicked(show)
fig.canvas.mpl_connect("show_error",show)

axlabel = plt.axes ([0.51, 0.05, 0.07, 0.05])
blabel = Button(axlabel,'Label Cycle', color = u'0.85', hovercolor = u'0.95')
blabel.on_clicked(label)
fig.canvas.mpl_connect('label_cycle',label)

################# CHECKBOXES ################
cxck = plt.axes([0.2,0.05, 0.2, 0.075]) #check position
check = CheckButtons(cxck,('SAC305','63Sn/37Pb'),(False,False)) #create check boxes
#cxtg = plt.axes([0.1,0.05,0.2,0.075])
#tggle = CheckButtons(cxtg,('Show Error'),(False))

################# ITEMS TO TOGGLE WITH CHECKBOX #################
p0, = ax.plot(profiles[0],profiles[1], visible = False, lw= 2) #plot profiles
a0 = ax.annotate(s="SAC305",xy=(273,166),xytext=(300,200),color = "green", arrowprops=dict(facecolor="green",shrink=0.01), visible = False)
p1, = ax.plot(profiles[2],profiles[3], visible = False, lw =2) #plot profiles http://goo.gl/RiW5l1
a1 = ax.annotate(s="63Sn/37Pb",xy=(261,145),xytext=(300,160),color = "red", arrowprops=dict(facecolor="red",shrink=0.01), visible = False) #plot for sac305
#And my team needs to learn how to python

l1 = plt.annotate(s = "Error Off", xy = (1,1), xytext = (2.01,0.84), color = 'red', visible = True)
l2 = plt.annotate(s = "Error On", xy = (1,1), xytext = (2.01, 0.84), color = "green", visible = False)

l3 = plt.annotate(s = "Label Off", xy = (1,1), xytext = (1.61,0.84), color = "red", visible = True)
l4 = plt.annotate(s = "Label On", xy = (1,1), xytext = (1.61,0.84), color = "green", visible = False)

######################### CYCLE LABELS #############################
n0 = ax.annotate ( s = "Pre Heat Zone", xy =(0,5), xytext = (80,10), color = "black", visible = False)
n1 = ax.annotate (s = "Reflow Zone", xy = (180,5), xytext = (195, 10), color = "black", visible = False)
n2 = ax.annotate (s = "Cooling Zone", xy = (240,5), xytext = (280, 10),
color = "black", visible = False)

n3 = ax.annotate ('',xy=(0,5), xytext = (180,5), arrowprops = {'arrowstyle' : '<->'}, visible = False)
n4 = ax.annotate ('',xy=(180,5), xytext = (240,5), arrowprops = {'arrowstyle' : '<->'}, visible = False)
n5 = ax.annotate ('',xy=(240,5), xytext = (340,5), arrowprops = {'arrowstyle' : '<->'}, visible = False)

#[0,90,180,210,240,340]
n6 = ax.annotate ('',xy=(180,300), xytext = (180,0), arrowprops = {'arrowstyle' : '-'}, visible = False)
n7 = ax.annotate ('',xy=(240,300), xytext = (240,0), arrowprops = {'arrowstyle' : '-'}, visible = False)
n8 = ax.annotate ('',xy=(340,300), xytext = (340,0), arrowprops = {'arrowstyle' : '-'}, visible = False)

e0, = ax.plot([90],[100],'o',visible=False)
e1, = ax.plot([180],[110],'o',visible=False)
e2, = ax.plot([210],[120],'o',visible=False)
e3, = ax.plot([240],[130],'o',visible=False)

###################### MAIN ###################################
ax.plot ()
ani = animation.FuncAnimation(fig,  run, data_gen, blit=False, interval=100, repeat=False)

check.on_clicked(func)
#tggle.on_clicked(show)

mng = plt.get_current_fig_manager()
mng.full_screen_toggle()#Full Screen

plt.show()





#error when no signal
#auto stop after cooling
#make calculate error after cooling
