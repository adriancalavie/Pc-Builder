from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from panda3d.core import CollisionBox, CollisionNode, Point3


class MOTHERBOARD(DirectObject):

    actor = Actor("Models/MOTHERBOARD")
    actor.setPos(0, 0, -40)
    actor.setScale(0.5)
