from matplotlib.transforms import BlendedGenericTransform
from matplotlib import patches
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
plt.rcParams['mathtext.fontset'] = 'cm'
import numpy as np


def transform_coords(coords, HT):
    if len(coords) == 2:
        coords = np.append(coords,[0,1])
    elif len(coords) == 3:
        coords = np.append(coords,[1])

    tcoords = np.dot(HT,coords)
    return tcoords


mygray = '#808B96'
grid_dict = {'linestyle':'dashed',\
             'color':mygray, \
             'linewidth':1.0, \
             'zorder':0, \
            }


class transformed_coords_sketch(object):
    """Throughout this class, frame A will be the global frame and
    frame B will be the rotated and/or translated frame."""
    def draw_rotated_line(self, start_coords, end_coords, HT, **plot_kwargs):
        start_A = transform_coords(start_coords, HT)
        stop_A = transform_coords(end_coords, HT)
        x_vect = [start_A[0],stop_A[0]]
        y_vect = [start_A[1],stop_A[1]]
        self.ax.plot(x_vect, y_vect, **plot_kwargs)


    def place_rotated_text(self, x, y, text, HT):
        rotated = transform_coords([x,y], HT)
        x_A = rotated[0]
        y_A = rotated[1]
        self.ax.text(x_A, y_A, text, va='center', \
                     fontdict=self.fontdict, ha='center')


    def place_text_A(self, x, y, text):
        self.place_rotated_text(x, y, text, self.eye)


    def place_text_B(self, x, y, text):
        self.place_rotated_text(x, y, text, self.HT)

            
    def draw_rotated_arrow(self, start_coords, end_coords, HT):
        start_A = transform_coords(start_coords, HT)
        stop_A = transform_coords(end_coords, HT)
        dx_A = stop_A[0]-start_A[0]
        dy_A = stop_A[1]-start_A[1]

        self.ax.arrow(start_A[0], start_A[1], dx_A, dy_A, \
                      fc='k', ec='k', lw = self.lw, \
                      head_width=self.hw, head_length=self.hl, \
                      overhang = self.ohg, \
                      length_includes_head= True, clip_on = False)


    def draw_axis(self, HT, substr='A'):
        xlabel = '$X_{%s}$' % substr
        ylabel = '$Y_{%s}$' % substr
        self.draw_rotated_arrow((self.xmin,0), (self.xmax,0), HT)
        self.place_rotated_text(self.xmax+0.5, 0, xlabel, HT)
        self.draw_rotated_arrow((0,self.ymin), (0,self.ymax), HT)
        self.place_rotated_text(0, self.ymax+0.5, ylabel, HT)


    def draw_axis_A(self):
        self.draw_axis(self.eye)


    def draw_axis_B(self):
        self.draw_axis(self.HT, substr='B')


    def draw_xticks(self, HT, ticks=None, dy=0.1, **plot_kwargs):
        kwargs = {'color':'k',\
                  'linewidth':2}
        kwargs.update(plot_kwargs)

        if ticks is None:
            ticks = np.arange(0, self.xmax, 1)

        
        for tick in ticks:
            start_tick = [tick, dy]
            end_tick = [tick, -dy]
            self.draw_rotated_line(start_tick, end_tick, HT, **kwargs)


    def draw_A_xticks(self, ticks=None, dy=0.1, **plot_kwargs):
        self.draw_xticks(self.eye,ticks=ticks, dy=dy, **plot_kwargs)


    def draw_B_xticks(self, ticks=None, dy=0.1, **plot_kwargs):
        self.draw_xticks(self.HT, ticks=ticks, dy=dy, **plot_kwargs)
        

    def draw_yticks(self, HT, ticks=None, dx=0.1, **plot_kwargs):
        kwargs = {'color':'k',\
                  'linewidth':2}
        kwargs.update(plot_kwargs)

        if ticks is None:
            ticks = np.arange(0, self.ymax, 1)

        for tick in ticks:
            start_tick = [-dx, tick]
            end_tick = [dx, tick]
            self.draw_rotated_line(start_tick, end_tick, HT, **kwargs)


    def draw_A_yticks(self, ticks=None, dx=0.1, **plot_kwargs):
        self.draw_yticks(self.eye,ticks=ticks, dx=dx, **plot_kwargs)


    def draw_B_yticks(self, ticks=None, dx=0.1, **plot_kwargs):
        self.draw_yticks(self.HT, ticks=ticks, dx=dx, **plot_kwargs)



    def draw_rotated_vertical_gridlines(self, HT, xlist=None, \
                                        ymin=0, ymax=None, plot_kwargs=None):
        if plot_kwargs is None:
            plot_kwargs = grid_dict

        if ymax is None:
            ymax = self.ymax

        if xlist is None:
            xlist = np.arange(0,self.xmax,1)

        for x in xlist:
            self.draw_rotated_line([x,ymin], [x,ymax], HT, **plot_kwargs)


    def draw_A_vertical_gridlines(self, xlist=None, **kwargs):
        self.draw_rotated_vertical_gridlines(self.eye, xlist=xlist,
                                             **kwargs)


    def draw_B_vertical_gridlines(self, xlist=None, **kwargs):
            self.draw_rotated_vertical_gridlines(self.HT, xlist=xlist,
                                                 **kwargs)


    def draw_rotated_horizontal_gridlines(self, HT, ylist=None, xmin=0, xmax=None, \
                                          plot_kwargs=None):
        if plot_kwargs is None:
            plot_kwargs = grid_dict

        if xmax is None:
            xmax = self.xmax

        if ylist is None:
            ylist = np.arange(0,self.ymax,1)
        

        for y in ylist:
            self.draw_rotated_line([xmin,y], [xmax,y], HT, **plot_kwargs)


    def draw_A_horizontal_gridlines(self, ylist=None, **kwargs):
        self.draw_rotated_horizontal_gridlines(self.eye, ylist=ylist,
                                               **kwargs)


    def draw_B_horizontal_gridlines(self, ylist=None, **kwargs):
        self.draw_rotated_horizontal_gridlines(self.HT, ylist=ylist,
                                               **kwargs)


    def draw_rotated_circle(self, x, y, r, HT, color='k', alpha=1, \
                            zorder=100):
        center_B = [x,y,0]
        center_A = transform_coords(center_B, HT)
        rot_circle = Circle((center_A[0], center_A[1]), r, \
                            color=color, alpha=alpha, \
                            zorder=zorder)
        self.ax.add_patch(rot_circle)


    def draw_circle_A(self, x, y, r, **kwargs):
        self.draw_rotated_circle(x, y, r, self.eye, **kwargs)
        

    def draw_circle_B(self, x, y, r, **kwargs):
        self.draw_rotated_circle(x, y, r, self.HT, **kwargs)

        
    def set_arrow_lengths(self):
        self.hw = 1./30.*(self.ymax-self.ymin)
        self.hl = 1./20.*(self.xmax-self.xmin)
        self.lw = 2. # axis line width
        self.ohg = 0.3 # arrow overhang

        # compute matching arrowhead length and width
        #yhw = hw/(ymax-ymin)*(xmax-xmin)* height/width
        #yhl = hl/(xmax-xmin)*(ymax-ymin)* width/height


    def axis_off(self):
        self.ax.set_axis_off()
        
        
    def __init__(self, HT, ax, \
                 xmax=5, xmin=-0.5, ymax=5, ymin=-0.5, \
                 xlims=[-3,7], ylims=[-3,7], \
                 fontdict = {'size': 18, 'family':'serif'}, \
                 ):
                 self.HT = HT
                 self.eye = np.eye(4)
                 self.ax = ax
                 self.xmax = xmax
                 self.xmin = xmin
                 self.ymax = ymax
                 self.ymin = ymin
                 self.xlims = xlims
                 self.ylims = ylims
                 self.fontdict = fontdict
                 ax.set_xlim(self.xlims)
                 ax.set_ylim(self.ylims)
                 self.set_arrow_lengths()
