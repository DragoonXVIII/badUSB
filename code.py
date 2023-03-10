import usb_hid
import time
import board
import busio
import storage
import digitalio

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode


# Wait for Trinkey to be initalized
time.sleep(1)

# Only for code testing purpouse
time.sleep(5)

# Initialize the keyboard and keyboard layout
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)


# Creating serial command connection

# Step 1: enable COM7 port in CMD
# Step 1.1: open CMD by running run utility
keyboard.press(Keycode.GUI, Keycode.R)         #pressing WIN+R to open run utility
keyboard.release_all()
time.sleep(1)                                  #wait for run utility to open

keyboard_layout.write("cmd")                   #typing cmd in run utility to open cmd
keyboard.release_all()
keyboard.press(Keycode.ENTER)
keyboard.release_all()
time.sleep(3)                                  #wait for CMD to open

keyboard_layout.write("mode COM7: baud=115200")#writing opening serial connection command to CMD
keyboard.release_all()
keyboard.press(Keycode.ENTER)
keyboard.release_all()
time.sleep(1)                                  #wait till CMD response (not always positive)

#keyboard.press(Keycode.ALT)                    #shutting down CMD
#keyboard.press(Keycode.F4)
#keyboard.release_all()
#time.sleep(1)

uart = busio.UART(board.TX, board.RX, baudrate=115200) #creating serial connection between Trinkey and CMD
time.sleep(1)                                  #wait till connection will be estabilished
                                               #DONE

#Step 2: Use estabilished serial connection as u want
uart.write(b"win: dir\r\n")                         #send the "dir" command to the Command Prompt
time.sleep(1)                                  #wait till CMD response

if uart.in_waiting:                            #print the output from the Command Prompt
    print(uart.read(uart.in_waiting))
    filename = "example.txt"
    # Open the file for writing
    with open(filename, "w") as f:
        # Write the updated contents to the file
        f.write(uart.read(uart.in_waiting))

else:
    print("No data received from UART")


#Button test
button = digitalio.DigitalInOut(board.BUTTON)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

if not button.value:
    print("Boot button is pressed")

while True:
    time.sleep(1)





