
import time
import board
import busio
import digitalio
import adafruit_lis3dh
from pymouse import PyMouse
from pynput.mouse import Button, Controller


# Hardware I2C setup. Use the CircuitPlayground built-in accelerometer if available;
# otherwise check I2C pins.
if hasattr(board, "ACCELEROMETER_SCL"):
    i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
else:
    i2c = board.I2C()  # uses board.SCL and board.SDA
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)


# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G


#####  BUTTON IO   #####
button_1 = digitalio.DigitalInOut(board.D5)
button_1.direction = digitalio.Direction.OUTPUT

button_2 = digitalio.DigitalInOut(board.D6)
button_2.direction = digitalio.Direction.OUTPUT

#pip install pynput
mouse = Controller()
temp1 = 0
temp2 = 0


#### Start position of cursor####
m=PyMouse()
(P,H) = m.position()
acc_list = [2,2,3,3,6,10]

#### Running part #####
while True:
    # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
    # z axis values.  Divide them by 9.806 to convert to Gs./ adafruit_lis3dh.STANDARD_GRAVITY
    x, y, z = [value for value in lis3dh.acceleration]

    ###Button Left Click and hold function###
    if button_1.value and temp1 == 0:
        mouse.press(Button.left)
        temp1 = 1
    elif button_1.value == False and temp1 == 1:
        mouse.release(Button.left)
        temp1 = 0

    ###Button Right Click and hold function###
    if button_2.value and temp2 == 0:
        mouse.press(Button.right)
        temp2 = 1
    elif button_2.value == False and temp2 == 1:
        mouse.release(Button.right)
        temp2 = 0

    ###Accelerativ for cursor movement###
    if abs(x)>0.5 or abs(y)>0.5:
        if P<0:
            P = 0
        elif P>765:
            P = 765
        else:
            if abs(x)<5:
                P = P-acc_list[round(x)-1]*x
            else:
                P=P-x*
                10
        if H<0:
            H = 0
        elif H>1380:
            H = 1380
        else:
            if abs(y)<1.5:
                H = H + (acc_list[round(y)-1]*y)/3
            else:
                H=H+y*10
        m.move(int(H), int(P))
        #print("Mouse moved to", P, H)
    time.sleep(0.0001)
    print("%0.3f %0.3f" % (x, y))
