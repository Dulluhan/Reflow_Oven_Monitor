
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import sys, time, math, serial
from matplotlib._png import read_png
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, \
     AnnotationBbox
from matplotlib.cbook import get_sample_data



xsize=400
pause = True


def data_gen():
    t = data_gen.t
    while (True):
       if pause: 
	       t+=1
	       val=math.sin(t*2.0*3.1415/50.0)
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
axpause = plt.axes([0.7, 0.05, 0.1, 0.075]) #button position "a seperature plot"
bpause = Button(axpause,'Pause',color = u'0.85', hovercolor = u'0.95') #create button 
bpause.on_clicked(onclick) #set action on click
fig.canvas.mpl_connect('pause_event',onclick) #add global event
ax.plot([0,90,180,210,240,340],[20,150,210,235,240,20])
            

# Important: Although blit=True makes graphing faster, we need blit=False to prevent
# spurious lines to appear when resizing the stripchart.
ax.plot ()
ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=100, repeat=False)

plt.show()


