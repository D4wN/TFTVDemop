from time import sleep

from tinkerforge.ip_connection import IPConnection

from bindings.brick_red import RED

HOST = "localhost"
PORT = 4223
RED_UID = "3dfBkF"

counter = 0

gray = None
face = None
snap = None

scene = None
end = False


def tv_init():
    print "Init TinkerVision"
    global gray, face, snap, scene
    # gray = red.vision_module_start("grayfilter")
    face = red.vision_module_start("cascadeclassifier")
    snap = red.vision_module_start("snapshot")
    print gray, face, snap

    scene = red.vision_scene_start(gray.id)
    print scene
    print "Scene Face add: " + str(red.vision_scene_add(scene.scene_id, face.id))
    print "Scene Snap add: " + str(red.vision_scene_add(scene.scene_id, snap.id))


def end_demo():
    print "Ending Demo"
    #stop tv, destroy tv, destroy ipcon
    print "TinkerVisione RM Modules: " + str(red.vision_remove_all_modules())
    print "TinkerVisione RM Scene  : " + str(red.vision_scene_remove(scene.scene_id))
    ipcon.disconnect()


def vision_callback(id, x, y, w, h, msg):
    if id != snap.id:
        return

    global counter, end
    if counter == 5:
        end = True
        return
    print id, x, y, w, h, msg
    counter += 1


if __name__ == "__main__":
    print "TinkerVision FaceCount Demo"

    ipcon = IPConnection()
    red = RED(RED_UID, ipcon)
    ipcon.connect(HOST, PORT)

    tv_init()
    red.register_callback(RED.CALLBACK_VISION_MODULE, vision_callback)

    while not end:
        sleep(1)

    end_demo()