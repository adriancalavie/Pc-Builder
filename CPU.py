from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from panda3d.core import CollisionBox, CollisionNode, CollisionSphere, Point3, TextNode, Vec3
from direct.interval.IntervalGlobal import *



class Processor(DirectObject):
    oPos = Point3(-80, 60, -27)
    oHpr = Vec3(300, 0, 0)
    motherPos = Point3(-1.5, 30, -25)
    motherHpr = Vec3(0, 0, 0)

    def __init__(self):
        super().__init__()
        self.actor = Actor("Models/CPU")
        self.actor.setPos(self.oPos)
        self.actor.setHpr(self.oHpr)
        self.actor.setScale(0.7)
        self.inPlace = False
        self.actor.node().setPythonTag('pickable', '1')
        self.cnode = self.actor.attachNewNode(CollisionNode('cnode_CPU'))
        self.cnode.node().addSolid(CollisionBox(Point3(0, 0, 0), 11, 11, 1))
        # self.cnode.show()
        self.cnode.reparentTo(self.actor)
