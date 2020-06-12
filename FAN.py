from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from panda3d.core import CollisionBox, CollisionNode, CollisionSphere, Point3, TextNode, Vec3
from direct.interval.IntervalGlobal import *


class Cooler(DirectObject):
    oPos = Point3(-115, 55, -27)
    oHpr = Vec3(325, 0, 0)
    motherPos = Point3(-1.5, 30, -24)
    motherHpr = Vec3(0, 0, 0)

    def __init__(self):
        super().__init__()
        self.actor = Actor("Models/FAN")
        self.actor.setPos(self.oPos)
        self.actor.setHpr(self.oHpr)
        self.actor.setScale(0.5)
        self.inPlace=False
        self.actor.node().setPythonTag('pickable', '8')
        self.cnode = self.actor.attachNewNode(CollisionNode('cnode_FAN'))
        self.cnode.node().addSolid(CollisionBox(Point3(-0.5, -0.5, 5), 18.5, 18.5, 7.5))
        # self.cnode.show()
        self.cnode.reparentTo(self.actor)
        self.ProcessorOn=False