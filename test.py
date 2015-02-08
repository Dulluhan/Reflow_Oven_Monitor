
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button,CheckButtons
import sys, time, math, serial
from matplotlib._png import read_png
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, \
     AnnotationBbox
from matplotlib.cbook import get_sample_data



xsize=400
pause = True
profiles = [[0,90,180,210,240,340],[20,150,210,235,240,20],
            [0,90,180,210,240,340],[20,150,180,208,180,20]]

def data_gen():
    t = data_gen.t
    while (True):
       if pause: 
	       t+=1
	       val=200*math.sin(t*2.0*3.1415/50.0)
       yield t, val

def run(data):
    # update the data
    t,y = data
    if (t>-1):
        xdata.append(t)
        ydata.append(y)
        if t>xsize: # Scroll to the left.
            ax.set_xlim(t-xsize, t)
        line.set_data(xdata, ydata)

    return line,

def on_close_figure(event):
    sys.exit(0)

def onclick(event):
    global pause
    pause = not pause
	#for pausing the graph when we need to 
def exit(event):
    mng.full_screen_toggle()
def func(label):
    if label == "SAC305": 
	p0.set_visible(not p0.get_visible())
	a0.set_visible(not a0.get_visible())
    elif label == "63Sn/37Pb": 
	p1.set_visible(not p1.get_visible())
	a1.set_visible(not a1.get_visible())
    plt.draw()	
 

data_gen.t = -1
fig = plt.figure()
fig.canvas.mpl_connect('close_event', on_close_figure)
ax = fig.add_subplot(111)
plt.subplots_adjust(bottom=0.2) #adjust margin on the bottom
plt.title('Inside Oven Temperature') #title
plt.ylabel('temperature') #y label
plt.xlabel('time') #x label 
line, = ax.plot([], [], lw=2)
ax.set_ylim(0, 300)
ax.set_xlim(0, xsize)
ax.grid()
xdata, ydata = [], []
##################BUTTONS#################
axpause = plt.axes([0.7, 0.05, 0.1, 0.075]) #button position "a seperature plot"
bpause = Button(axpause,'Pause',color = u'0.85', hovercolor = u'0.95') #create button 
bpause.on_clicked(onclick) #set action on click
fig.canvas.mpl_connect('pause_event',onclick) #add global event

axexit = plt.axes([0.48, 0.05, 0.2, 0.075]) #toggle button
bexit = Button(axexit,'Toggle Screen',color = u'0.85', hovercolor = u'0.95')
bexit.on_clicked(exit)
fig.canvas.mpl_connect('pause_event',exit)

#################CHECKBOXES################
cxck = plt.axes([0.2,0.05, 0.2, 0.075]) #check position 
check = CheckButtons(cxck,('SAC305','63Sn/37Pb'),(False,False)) #create check boxes



#################ITEMS TO TOGGLE WITH CHECKBOX#################
p0, = ax.plot(profiles[0],profiles[1], visible = False, lw= 2) #plot profiles 
a0 = ax.annotate(s="SAC305",xy=(273,166),xytext=(300,200),color = "green", arrowprops=dict(facecolor="green",shrink=0.01), visible = False ) 
p1, = ax.plot(profiles[2],profiles[3], visible = False, lw =2) #plot profiles http://goo.gl/RiW5l1
a1 = ax.annotate(s="63Sn/37Pb",xy=(261,145),xytext=(300,160),color = "red", arrowprops=dict(facecolor="red",shrink=0.01), visible = False  ) 


# Important: Although blit=True makes graphing faster, we need blit=False to prevent
# spurious lines to appear when resizing the stripchart.
ax.plot ()
ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=100, repeat=False)

check.on_clicked(func)
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
plt.show()


