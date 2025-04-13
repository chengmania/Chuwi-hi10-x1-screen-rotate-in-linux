#!/usr/bin/env python3
import time
import subprocess

display = "DSI-1"

base = "/sys/bus/iio/devices/iio:device0/"
x_path = base + "in_accel_x_raw"
y_path = base + "in_accel_y_raw"

last_orientation = None

def read_axis(path):
    try:
        with open(path, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def rotate(direction):
    subprocess.call(["/usr/bin/kscreen-doctor", f"output.{display}.rotation.{direction}"])

# Rotation logic with labels FLIPPED to match your real orientation
while True:
    x = read_axis(x_path)
    y = read_axis(y_path)

    if abs(x) > abs(y):
        if x > 300:
            orientation = "normal"     # Was "inverted", flip to normal
        elif x < -300:
            orientation = "inverted"   # Was "normal", flip to inverted
        else:
            orientation = "normal"
    else:
        if y > 300:
            orientation = "left"       # Was "right", flip
        elif y < -300:
            orientation = "right"      # Was "left", flip
        else:
            orientation = "normal"

    if orientation != last_orientation:
        print(f"Rotating to: {orientation}")
        rotate(orientation)
        last_orientation = orientation

    time.sleep(1)
