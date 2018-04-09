'''  BoxWorldWindow to test/demo graph (path) search.

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au
Please don't share without permission.

See readme.txt for details.

'''

from graphics import egi
import pyglet
from pyglet import window, clock
from pyglet.window import key
from pyglet.gl import *
from pyglet.text import Label

from box_world import BoxWorld, search_modes, cfg

class BoxWorldWindow(pyglet.window.Window):

    # Mouse mode indicates what the mouse "click" should do...
    mouse_modes = {
        key._1: 'clear',
        key._2: 'mud',
        key._3: 'water',
        key._4: 'wall',
        key._5: 'start',
        key._6: 'target',
    }
    mouse_mode = 'wall'

    # search mode cycles through the search algorithm used by box_world
    search_mode = 0

    def __init__(self, filename, **kwargs):
        kwargs.update({
            'width': 500,
            'height': 500,
            'vsync':True,
            'resizable':True,
        })
        super(BoxWorldWindow, self).__init__(**kwargs)

        self.searching = False;

        # create a pyglet window and set glOptions
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # needed so that graphs.egi knows where to draw
        egi.InitWithPyglet(self)
        egi.text_color(name='BLACK')

        glClearColor(0.9, 0.9, 0.9, 1.0) # Grey

        #create a world for graph searching
        #filename = kwargs['filename'] #"boxworld2.txt"
        #filename = 'map2.txt'
        self.world = BoxWorld.FromFile(filename, self.get_size())
        self.world.reset_navgraph()

        # prep the fps display and some labels
        self.fps_display = clock.ClockDisplay()
        clBlack = (0,0,0, 255)
        self.labels = {
            'mouse':  Label('', x=5, y=self.height-20, color=clBlack),
            'search': Label('', x=120, y=self.height-20, color=clBlack),
            'status': Label('', x=300, y=self.height-20, color=clBlack),
        }
        self._update_label()

        # add the extra event handlers we need
        self.add_handers()

        # search limit
        self.limit = 0 # unlimited.

    def _update_label(self, key=None, text='---'):
        if key == 'mouse' or key is None:
            self.labels['mouse'].text = 'Kind: '+self.mouse_mode
        if key == 'search' or key is None:
            self.labels['search'].text = 'Search: '+ search_modes[self.search_mode]
        if key == 'status' or key is None:
            self.labels['status'].text = 'Status: '+ text

    def add_handers(self):

        @self.event
        def on_resize(cx, cy):
            self.world.resize(cx, cy-25)
            # reposition the labels.
            for key, label in list(self.labels.items()):
                label.y = cy-20

        @self.event
        def on_mouse_press(x, y, button, modifiers):
            if button == 1: # left
                box = self.world.get_box_by_pos(x,y)
                if box:
                    if self.mouse_mode == 'start':
                        self.world.set_start(box.node.idx)
                    elif self.mouse_mode == 'target':
                        self.world.set_target(box.node.idx)
                    else:
                        box.set_kind(self.mouse_mode)
                    self.world.reset_navgraph()
                    self.plan_path()
                    self._update_label('status','graph changed')


        @self.event
        def on_key_press(symbol, modifiers):

            if symbol == key.Q:
                if self.searching:
                    return
                else:
                    self.searching = True

                    print("Do search to position (A*)")
                    self.world.set_target(110)
                    self.search_mode = 3
                    self.plan_path()
                    self._update_label('search')
            elif symbol == key.W:
                if self.searching:
                    return
                else:
                    self.searching = True

                    print("Do search for item (Dijkstra)")
                    self.world.set_target(79)
                    self.search_mode = 2
                    self.plan_path()
                    self._update_label('search')

            elif symbol == key.R:
                print("reset")
                self.searching = False

                self.world.path = None
                self.world.agent = None

    def plan_path(self):
        self.world.plan_path(search_modes[self.search_mode], self.limit)
        self._update_label('status', 'path planned')
        print(self.world.path.report(verbose=3))

    def on_draw(self):
        self.clear()
        self.world.draw()
        if self.fps_display:
            self.fps_display.draw()
        for key, label in list(self.labels.items()):
            label.draw()



#==============================================================================

if __name__ == '__main__':
    import sys

    filename = "map2.txt"
    window = BoxWorldWindow(filename)
    pyglet.app.run()

