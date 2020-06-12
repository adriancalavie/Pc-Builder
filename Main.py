from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText, TextNode
from panda3d.core import AmbientLight, DirectionalLight, LVector3, LightAttrib
import sys
import tkinter as tk
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.interval.MetaInterval import Parallel, Sequence
from direct.interval.FunctionInterval import Wait
from direct.gui.OnscreenImage import OnscreenImage
from direct.task import Task

from RAM import Ram
from MOTHERBOARD import MOTHERBOARD
from CPU import Processor
from SSD import Ssd
from GPU import VideoCard
from FAN import Cooler

loadPrcFile("Config/conf.prc")

SENSITIVITY = 1


CPU = Processor()
RAM1 = Ram(0)
RAM2 = Ram(1)
RAM3 = Ram(2)
RAM4 = Ram(3)
SSD = Ssd()
GPU = VideoCard()
FAN = Cooler()


def PointAtZ(z, point, vec):
    return point + vec * ((z - point.getZ()) / vec.getZ())


class Msg(DirectObject):
    def __init__(self):
        self.accept("escape", self.endgame)

    def endgame(self):
        sys.exit(0)


def pickup(obj, hpr_dest=Vec3(0, 0, 0)):
    print('picking ' + obj.getName())
    time = 1
    inv = obj.posHprInterval(time, Point3(
        obj.getX(), obj.getY(), obj.getZ()+50), hpr_dest)
    return inv


def move(obj, destination, hpr_dest=Vec3(0, 0, 0), pickfirst=True):
    time = 1
    go = obj.posHprInterval(time, destination, hpr_dest)
    if pickfirst:
        pick = pickup(obj, hpr_dest)
        action = Sequence(pick, Wait(0.3), go)
        action.start()
    else:
        go.start()


class Game(ShowBase):
    def __init__(self):
        super().__init__()

        self.disableMouse()

        self.camera.setPosHpr(0, -150, 150, 0, -45, 0)
        self.camLens.setFov(85)
        self.scene = self.loader.loadModel("Models/ROOM4.obj")
        self.scene.setScale(30)
        self.scene.setPos(0, -210, -201)
        self.scene.reparentTo(self.render)

        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor((0.6, 0.6, 0.6, 1))
        ambientLightNP = self.scene.attachNewNode(ambientLight)
        self.scene.setLight(ambientLightNP)

        dlight = DirectionalLight('dlight')
        dlight.setColorTemperature(7000)
        dlnp = self.scene.attachNewNode(dlight)
        dlnp.setHpr(354, 266, 0)
        self.scene.setLight(dlnp)

        # fonts
        airstrike = self.loader.loadFont("airstrike.ttf")
        googlesans = self.loader.loadFont("GoogleSans-Regular.ttf")

        # texts
        self.error_cpu_not_on = OnscreenText(text='The CPU is not placed\nConsider putting it before the Fan', fg=(
            1, 1, 1, 1), shadow=(0, 0, 0, 1), align=TextNode.ALeft, pos=(-1.7, 0.8), bg=(0, 0, 0, 0.2))
        self.error_cpu_not_on.setFont(googlesans)
        self.error_cpu_not_on.hide()

        self.error_fan_on = OnscreenText(text='The Fan is placed on the socket\nConsider removing the Fan first', fg=(
            1, 0, 0, 1), shadow=(0, 0, 0, 1), align=TextNode.ALeft, pos=(-1.7, 0.8), bg=(0, 0, 0, 0.2))
        self.error_fan_on.setFont(googlesans)
        self.error_fan_on.hide()

        self.fullBoard = OnscreenText(text='Congratulations!\nAll the pieces are in place', fg=(
            8, 249, 0, 1), shadow=(0, 0, 0, 1), align=TextNode.ACenter, shadowOffset=(0.1,0.1), scale=0.15, pos=(0, 0.65))
        self.fullBoard.setFont(airstrike)
        self.fullBoard.hide()

        self.instructions = OnscreenText(text='right-click \t\t select\nleft-click \t\t move to place\n(while selected) X \t move back\nesc \t\t exit', fg=(
            1, 1, 1, 1), shadow=(0, 0, 0, 1), align=TextNode.ALeft, pos=(-1.7, -0.7), bg=(0, 0, 0, 0.2))
        self.instructions.setFont(googlesans)
        # self.instructions.hide()
        # images
        self.CPU_info = OnscreenImage("CPU_INFO.png", pos=(
            2.88, 0, 0), scale=(0.45, 1, 1.0125))

        self.RAM1_info = OnscreenImage(
            "RAM_INFO.png", pos=(
                2.88, 0, 0), scale=(0.45, 1, 1.0125))
        self.RAM2_info = OnscreenImage(
            "RAM_INFO.png", pos=(
                2.88, 0, 0), scale=(0.45, 1, 1.0125))
        self.RAM3_info = OnscreenImage(
            "RAM_INFO.png", pos=(
                2.88, 0, 0), scale=(0.45, 1, 1.0125))
        self.RAM4_info = OnscreenImage(
            "RAM_INFO.png", pos=(
                2.88, 0, 0), scale=(0.45, 1, 1.0125))

        self.GPU_info = OnscreenImage(
            "GPU_INFO.png", pos=(
                2.88, 0, 0), scale=(0.45, 1, 1.0125))

        self.SSD_info = OnscreenImage(
            "SSD_INFO.png", pos=(
                2.88, 0, 0), scale=(0.45, 1, 1.0125))

        self.FAN_info = OnscreenImage("FAN_INFO.png", pos=(
            2.88, 0, 0), scale=(0.45, 1, 1.0125))

        self.MOTHERBOARD_info = OnscreenImage("MOTHERBOARD_INFO.png", pos=(
            2.88, 0, 0), scale=(0.45, 1, 1.0125))

        self.CPU_info.reparentTo(self.aspect2d)
        self.RAM1_info.reparentTo(self.aspect2d)
        self.RAM2_info.reparentTo(self.aspect2d)
        self.RAM3_info.reparentTo(self.aspect2d)
        self.RAM4_info.reparentTo(self.aspect2d)
        self.GPU_info.reparentTo(self.aspect2d)
        self.SSD_info.reparentTo(self.aspect2d)
        self.FAN_info.reparentTo(self.aspect2d)
        self.MOTHERBOARD_info.reparentTo(self.aspect2d)
        # models
        MOTHERBOARD.actor.reparentTo(self.render)
        MOTHERBOARD.actor.reparentTo(self.render)

        CPU.actor.reparentTo(self.render)
        RAM1.actor.reparentTo(self.render)
        RAM2.actor.reparentTo(self.render)
        RAM3.actor.reparentTo(self.render)
        RAM4.actor.reparentTo(self.render)
        SSD.actor.reparentTo(self.render)
        GPU.actor.reparentTo(self.render)
        FAN.actor.reparentTo(self.render)

        self.pieces = []
        self.pieces.append(CPU)
        self.pieces.append(RAM1)
        self.pieces.append(RAM2)
        self.pieces.append(RAM3)
        self.pieces.append(RAM4)
        self.pieces.append(SSD)
        self.pieces.append(GPU)
        self.pieces.append(FAN)

        self.data = {
            CPU.actor: self.CPU_info,
            RAM1.actor: self.RAM1_info,
            RAM2.actor: self.RAM2_info,
            RAM3.actor: self.RAM3_info,
            RAM4.actor: self.RAM4_info,
            GPU.actor: self.GPU_info,
            SSD.actor: self.SSD_info,
            FAN.actor: self.FAN_info
        }
        self.placed = {
            CPU.actor: False,
            RAM1.actor: False,
            RAM2.actor: False,
            RAM3.actor: False,
            RAM4.actor: False,
            GPU.actor: False,
            SSD.actor: False,
            FAN.actor: False
        }

        CPU.actor.setLight(ambientLightNP)
        RAM1.actor.setLight(ambientLightNP)
        RAM2.actor.setLight(ambientLightNP)
        RAM3.actor.setLight(ambientLightNP)
        RAM4.actor.setLight(ambientLightNP)
        GPU.actor.setLight(ambientLightNP)
        # SSD.actor.setLight(ambientLightNP)
        FAN.actor.setLight(ambientLightNP)

        CPU.actor.setLight(dlnp)
        RAM1.actor.setLight(dlnp)
        RAM2.actor.setLight(dlnp)
        RAM3.actor.setLight(dlnp)
        RAM4.actor.setLight(dlnp)
        GPU.actor.setLight(dlnp)
        # SSD.actor.setLight(dlnp)
        FAN.actor.setLight(dlnp)
        m = Msg()
        # messenger.send('1', [self.camera])
        self.picker = CollisionTraverser()
        # self.picker.showCollisions(self.render)
        self.pq = CollisionHandlerQueue()

        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(BitMask32.bit(1))
        # CPU.actor.setCollideMask(BitMask32.bit(1))

        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.picker.addCollider(self.pickerNP, self.pq)

        self.accept("mouse1", self.mouseClick)
        self.accept("mouse3", self.rightClick)
        self.accept('mouse4', self.centerMotherboard)
        self.accept('mouse5', self.defaultCamera)
        self.accept('z', self.checkFull)

        self.taskMgr.add(self.checkFull, 'Check if full')

    def checkFull(self, task):
        if self.isFull():
            self.fullBoard.show()
        else:
            self.fullBoard.hide()
        return task.cont

    def mouseClick(self):
        # print('mouse click')
        # check if we have access to the mouse
        if self.mouseWatcherNode.hasMouse():

            # get the mouse position
            mpos = self.mouseWatcherNode.getMouse()

            # set the position of the ray based on the mouse position
            self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())
            self.picker.traverse(self.render)
            # if we have hit something sort the hits so that the closest is first and highlight the node
            if self.pq.getNumEntries() > 0:
                self.pq.sortEntries()
                pickedObj = self.pq.getEntry(0).getIntoNodePath()
                pickedObjx = self.pq.getEntry(0)
                # print('click on ' + pickedObj.getName())
                # print(self.getDestination(pickedObj.getParent()))
                # print(self.getRotation(pickedObj.getParent()))
                self.fade()
                self.defaultCamera()
                if pickedObj.getParent().getKey() == CPU.actor.getKey() and self.placed[FAN.actor] == True:
                    self.error_fan_on.show()
                else:
                    self.error_fan_on.hide()
                    move(pickedObj.getParent(), self.getDestination(
                        pickedObj.getParent(), False), self.getRotation(pickedObj.getParent(), False), True)
                    if pickedObj.getParent().getKey() == CPU.actor.getKey():
                        FAN.ProcessorOn = True
                    self.placed[pickedObj.getParent()] = True
                if pickedObj.getParent().getKey() == FAN.actor.getKey() and not FAN.ProcessorOn:
                    self.error_cpu_not_on.show()
                else:
                    self.error_cpu_not_on.hide()

    def getDestination(self, object, goHome):
        # print('checking destination for ' + object.getName())
        for i in self.pieces:
            if i.actor.getKey() == object.getKey():
                if goHome:
                    i.inPlace = False
                    return i.oPos
                else:
                    i.inPlace = True
                    return i.motherPos

    def getRotation(self, object, goHome):
        # print('checking rotation for ' + object.getName())
        for i in self.pieces:
            if i.actor.getKey() == object.getKey():
                if goHome:
                    i.inPlace = False
                    return i.oHpr
                else:
                    i.inPlace = True
                    return i.motherHpr

    def rightClick(self):
        if self.mouseWatcherNode.hasMouse():

            # get the mouse position
            mpos = self.mouseWatcherNode.getMouse()

            # set the position of the ray based on the mouse position
            self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())
            self.picker.traverse(self.render)
            # if we have hit something sort the hits so that the closest is first and highlight the node
            if self.pq.getNumEntries() > 0:
                self.pq.sortEntries()
                pickedObj = self.pq.getEntry(0).getIntoNodePath()
                pickedObjx = self.pq.getEntry(0)
                # print('right click on ' + pickedObj.getName())

                self.accept('x', self.goBack, [pickedObj.getParent()])

                self.accept('w-repeat', self.pitch,
                            [pickedObj.getParent(), True])
                self.accept('w', self.pitch,
                            [pickedObj.getParent(), True])
                self.accept('s-repeat', self.pitch,
                            [pickedObj.getParent(), False])
                self.accept('s', self.pitch,
                            [pickedObj.getParent(), False])
                self.accept('a-repeat', self.heading,
                            [pickedObj.getParent(), False])
                self.accept('a', self.heading,
                            [pickedObj.getParent(), False])
                self.accept('d-repeat', self.heading,
                            [pickedObj.getParent(), True])
                self.accept('d', self.heading,
                            [pickedObj.getParent(), True])
                self.info_out(self.data[pickedObj.getParent()])
                self.fade(pickedObj.getParent())
                self.centerCamera(pickedObj.getParent())
                self.defaultPositioning(pickedObj.getParent())
            else:
                self.defaultCamera()
                self.defaultPositioning()
                self.fade()

    def goBack(self, object):
        self.defaultCamera()
        # self.fade()
        move(object,
             self.getDestination(object, True),
             self.getRotation(object, True), True)
        if object.getKey() == CPU.actor.getKey():
            FAN.ProcessorOn = False
        self.placed[object] = False

    def defaultPositioning(self, object=MOTHERBOARD.actor):
        for i in self.pieces:
            if i.actor.getKey() == CPU.actor.getKey() and i.actor.getKey() != object.getKey():
                if not CPU.inPlace:
                    move(i.actor, CPU.oPos, CPU.oHpr, False)
                else:
                    move(i.actor, CPU.motherPos, CPU.motherHpr, False)

            elif i.actor.getKey() == RAM1.actor.getKey() and i.actor.getKey() != object.getKey():
                if not RAM1.inPlace:
                    move(i.actor, RAM1.oPos, RAM1.oHpr, False)
                else:
                    move(i.actor, RAM1.motherPos, RAM1.motherHpr, False)

            elif i.actor.getKey() == RAM2.actor.getKey() and i.actor.getKey() != object.getKey():
                if not RAM2.inPlace:
                    move(i.actor, RAM2.oPos, RAM2.oHpr, False)
                else:
                    move(i.actor, RAM2.motherPos, RAM2.motherHpr, False)

            elif i.actor.getKey() == RAM3.actor.getKey() and i.actor.getKey() != object.getKey():
                if not RAM3.inPlace:
                    move(i.actor, RAM3.oPos, RAM3.oHpr, False)
                else:
                    move(i.actor, RAM3.motherPos, RAM3.motherHpr, False)
            elif i.actor.getKey() == RAM4.actor.getKey() and i.actor.getKey() != object.getKey():
                if not RAM4.inPlace:
                    move(i.actor, RAM4.oPos, RAM4.oHpr, False)
                else:
                    move(i.actor, RAM4.motherPos, RAM4.motherHpr, False)
            elif i.actor.getKey() == SSD.actor.getKey() and i.actor.getKey() != object.getKey():
                if not SSD.inPlace:
                    move(i.actor, SSD.oPos, SSD.oHpr, False)
                else:
                    move(i.actor, SSD.motherPos, SSD.motherHpr, False)
            elif i.actor.getKey() == GPU.actor.getKey() and i.actor.getKey() != object.getKey():
                if not GPU.inPlace:
                    move(i.actor, GPU.oPos, GPU.oHpr, False)
                else:
                    move(i.actor, GPU.motherPos, GPU.motherHpr, False)
            elif i.actor.getKey() == FAN.actor.getKey() and i.actor.getKey() != object.getKey():
                if not FAN.inPlace:
                    move(i.actor, FAN.oPos, FAN.oHpr, False)
                else:
                    move(i.actor, FAN.motherPos, FAN.motherHpr, False)

    def heading(self, obj, positive):
        # print('heading for ' + obj.getName() + ' ' + str(positive))
        if positive:
            obj.setH(obj.getH() + 5*SENSITIVITY)
        else:
            obj.setH(obj.getH() - 5*SENSITIVITY)
        if obj.getH() == 360:
            obj.setH(0)

    def pitch(self, obj, positive):
        # print('pitch for ' + obj.getName() + ' ' + str(positive))
        if positive:
            obj.setP(obj.getP() + 5*SENSITIVITY)
        else:
            obj.setP(obj.getP() - 5*SENSITIVITY)
        if obj.getP() == 360:
            obj.setP(0)

    def centerCamera(self, object):
        pick = pickup(object)
        inv = self.camera.posHprInterval(
            1, Point3(object.getX()+20, object.getY()-55, object.getZ()+90), Vec3(0, -30, 0))
        action = Parallel(pick, inv)
        action.start()

    def defaultCamera(self):
        inv = self.camera.posHprInterval(
            1, Point3(0, -150, 150), Vec3(0, -45, 0))
        fadeOut = self.MOTHERBOARD_info.posInterval(1, Point3(2.88, 0, 0))
        action = Parallel(inv, fadeOut)
        action.start()

    def centerMotherboard(self):
        self.info_out(self.MOTHERBOARD_info)
        inv = self.camera.posHprInterval(
            1, Point3(MOTHERBOARD.actor.getX(), MOTHERBOARD.actor.getY()-130, MOTHERBOARD.actor.getZ()+100), Vec3(0, -30, 0))
        inv.start()

    def info_out(self, object):
        fadeIn = object.posInterval(1, Point3(1.33, 0, 0))
        fadeIn.start()

    def fade(self, object=MOTHERBOARD.actor):
        for i in self.data:
            if i != object:
                fadeOut = self.data[i].posInterval(1, Point3(2.88, 0, 0))
                fadeOut.start()
        fadeOut = self.MOTHERBOARD_info.posInterval(1, Point3(2.88, 0, 0))
        fadeOut.start()

    def isFull(self):
        for i in self.placed.values():
            if i == False:
                return False
        return True


game = Game()
game.run()
