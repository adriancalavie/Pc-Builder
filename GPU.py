from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from panda3d.core import CollisionBox, CollisionNode, CollisionSphere, Point3, TextNode, Vec3
from direct.interval.IntervalGlobal import *



class VideoCard(DirectObject):
    oPos = Point3(-100, -5, -27.75)
    oHpr = Vec3(37, 0, 0)
    motherPos = Point3(-28, -24, -11)
    motherHpr = Vec3(0, 90, 0)

    def __init__(self):
        super().__init__()
        self.actor = Actor("Models/GPU")
        self.actor.setPos(self.oPos)
        self.actor.setHpr(self.oHpr)
        self.inPlace = False
        self.actor.setScale(0.3)
        self.actor.node().setPythonTag('pickable', '7')
        self.cnode = self.actor.attachNewNode(CollisionNode('cnode_GPU'))
        self.cnode.node().addSolid(CollisionBox(Point3(45, 10, 21.5), 120, 50, 20))
        # self.cnode.show()
        self.cnode.reparentTo(self.actor)
