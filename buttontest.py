from button import *
import time


b = Button(23, debounce=0.1)

while True:
    if b.is_pressed():
        print("Pressed!")
