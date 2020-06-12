from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from panda3d.core import CollisionBox, CollisionNode, CollisionSphere, Point3, TextNode, Vec3
from direct.interval.IntervalGlobal import *



class Ssd(DirectObject):
    oPos = Point3(-70, -35, -27.75)
    oHpr = Vec3(326, 0, 0)
    motherPos = Point3(-8, 4, -24)
    motherHpr = Vec3(0, 0, 0)


    def __init__(self):
        super().__init__()
        self.actor = Actor("Models/SSD")
        self.actor.setPos(self.oPos)
        self.actor.setHpr(self.oHpr)
        self.inPlace = False
        self.actor.setScale(2)
        self.actor.node().setPythonTag('pickable', '6')
        self.cnode = self.actor.attachNewNode(CollisionNode('cnode_SSD'))
        self.cnode.node().addSolid(CollisionBox(Point3(0, 0, 0.2), 7.2, 2.15, 0.2))
        # self.cnode.show()
        self.cnode.reparentTo(self.actor)
