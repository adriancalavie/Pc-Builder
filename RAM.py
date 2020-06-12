from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from panda3d.core import CollisionBox, CollisionNode, CollisionSphere, Point3, TextNode, Vec3
from direct.interval.IntervalGlobal import *


class Ram(DirectObject):

    def __init__(self, count):
        super().__init__()

        self.oPos = Point3(60+count*20, 30, -27)
        self.oHpr = Vec3(90, 0, 0)
        self.motherPos = Point3(18.8+count*3.375, 30.5, -20)
        self.motherHpr = Vec3(90, 90, 0)

        self.actor = Actor("Models/RAM.obj")
        self.actor.setPos(self.oPos)
        self.actor.setHpr(self.oHpr)
        self.inPlace=False
        self.actor.setScale(33, 33, 25)
        self.actor.node().setPythonTag('pickable', str(2+count))

        tag = TextNode("RAM"+str(count))
        self.actor.attachNewNode(tag)

        self.cnode = self.actor.attachNewNode(
            CollisionNode('cnode_RAM'+str(count)))
        self.cnode.node().addSolid(CollisionBox(Point3(0, 0.085, -0.035), 0.73, 0.25, 0.07))
        self.cnode.reparentTo(self.actor)
        # self.cnode.show()

