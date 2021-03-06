'''Autonomous Agent Movement: Seek, Arrive and Flee

Created for COS30002 AI for Games, Lab 05
By Clinton Woodward cwoodward@swin.edu.au

'''
from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *

from vector2d import Vector2D
from world import World
from agent import Agent, AGENT_MODES  # Agent with seek, arrive, flee and pursuit


def on_mouse_press(x, y, button, modifiers):
    if button == 1:  # left
        world.target = Vector2D(x, y)


def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused
    elif symbol in AGENT_MODES:
        for agent in world.agents:
            agent.mode = AGENT_MODES[symbol]
    ## LAB 05 TASK 2: Add agent by pressing a key
    elif symbol == KEY.NUM_ADD:
        world.agents.append(Agent(world,10,0.01))
    elif symbol == KEY.NUM_SUBTRACT:
        if len(world.agents) > 0:
            world.agents.pop()

    ## LAB 06 TASK 1: Reset all paths to new random ones
    elif symbol == KEY.R:
        for agent in world.agents:
            agent.randomise_path()

    #modify wander variables
    elif symbol == KEY.Z:
        for agent in world.agents:
            agent.modify_variables('radius', True)

    elif symbol == KEY.X:
        for agent in world.agents:
            agent.modify_variables('radius', False)

    elif symbol == KEY.C:
        for agent in world.agents:
            agent.modify_variables('dist', True)

    elif symbol == KEY.V:
        for agent in world.agents:
            agent.modify_variables('dist', False)

    elif symbol == KEY.B:
        for agent in world.agents:
            agent.modify_variables('jitter', True)

    elif symbol == KEY.N:
        for agent in world.agents:
            agent.modify_variables('jitter', False)

    # Toggle debug force line info on the agent
    elif symbol == KEY.I:
        for agent in world.agents:
            agent.show_info = not agent.show_info



def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy


if __name__ == '__main__':

    # create a pyglet window and set glOptions
    win = window.Window(width=500, height=500, vsync=True, resizable=True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = clock.ClockDisplay()
    # register key and mouse event handlers
    win.push_handlers(on_key_press)
    win.push_handlers(on_mouse_press)
    win.push_handlers(on_resize)

    # create a world for agents
    world = World(500, 500)
    # add one agent
    world.agents.append(Agent(world,10,0.01))
    # unpause the world ready for movement
    world.paused = False

    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # show nice FPS bottom right (default)
        delta = clock.tick()
        world.update(delta)
        world.render()
        fps_display.draw()
        # swap the double buffer
        win.flip()

