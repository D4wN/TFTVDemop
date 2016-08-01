from time import sleep

from tinkerforge.ip_connection import IPConnection

from bindings.brick_red import RED

# HOST = "192.168.0.67"
HOST = "localhost"
PORT = 4223
RED_UID = "3dfBkF"
#RED_UID = "37GByw"

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
    face = red.vision_module_start("downscale")
    # red.vision_numerical_parameter_set(face.id, "max-hue", 50) #max h    180
    # red.vision_numerical_parameter_set(face.id, "min-hue", 0) #min h
    # red.vision_numerical_parameter_set(face.id, "max-saturation", 255) #max s    255
    # red.vision_numerical_parameter_set(face.id, "min-saturation", 200) #min s
    # red.vision_numerical_parameter_set(face.id, "max-value", 255) #max v
    # red.vision_numerical_parameter_set(face.id, "min-value", 50) #min v

    snap = red.vision_module_start("snapshot")
    print gray, face, snap

    # scene = red.vision_scene_start(face.id)
    # # print "Scene Face add: " + str(red.vision_scene_add(scene.scene_id, face.id))
    # print "Scene Snap add: " + str(red.vision_scene_add(scene.scene_id, snap.id))


def end_demo():
    print "Ending Demo"
    #stop tv, destroy tv, destroy ipcon
    print "TinkerVisione RM Modules: " + str(red.vision_remove_all_modules())
    # print "TinkerVisione RM Scene  : " + str(red.vision_scene_remove(scene.scene_id))
    ipcon.disconnect()


def vision_callback(id, x, y, w, h, msg):
    # print "CB"
    # if id != snap.id:
    #     return

    global counter, end
    if counter == 10:
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

    print "Loop"
    while not end:
        sleep(1)

    end_demo()