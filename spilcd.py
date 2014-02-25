import spidev
import time

class SpiLcd:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.lsbfirst = False
        self.spi.max_speed_hz = 500000
        self.set_backlight(False)
        self.initialize()
    def set_backlight(self, value):
        if value:
            self.backlight = 0x80
        else:
            self.backlight = 0x40
    def send4(self, cmd):
        #print "mandando 4bits 0x%02x" % (cmd)
        self.spi.xfer([ (self.backlight) | cmd])
        self.spi.xfer([ (self.backlight) | 0x10 | cmd])
        time.sleep(.0000005)
        self.spi.xfer([ (self.backlight) | cmd])
    def cmd(self, cmd):
        #print "mandando cmd 0x%02x" % (cmd)
        self.send4((cmd >> 4) & 0x0f)
        time.sleep(.005)
        self.send4(cmd & 0x0f)
        time.sleep(.005)
    def data(self, d):
        #print "mandando data 0x%02x" % (d)
        self.send4(0x20 | ((d >> 4) & 0x0f))
        time.sleep(.0002)
        self.send4(0x20 | (d & 0x0f))
        time.sleep(.0002)
    def initialize(self):
        self.send4(0x03)
        time.sleep(.005)
        self.send4(0x03)
        time.sleep(.0002)
        self.send4(0x03)
        time.sleep(.0002)
        self.send4(0x02)
        time.sleep(.005)
        self.cmd(0x28)
        self.cmd(0x08)
        self.cmd(0x01)
        self.cmd(0x06)
        self.cmd(0x0c)
    def write(self, txt):
        for c in txt:
            self.data(ord(c))
    def clear(self):
        self.cmd(0x01)
    def goto(self,row=0,col=0):
        self.cmd(0x80 + (row%2)*0x40 + (row//2)*0x14 + col)


### Test code for 20x4

LCD = SpiLcd()
bl = False

while True:
    LCD.set_backlight(bl)
    bl = not bl
    LCD.write("holiwi")
    LCD.goto(1,1)
    LCD.write("chai")
    LCD.goto(2,2)
    LCD.write("miau")
    LCD.goto(3,3)
    LCD.write("guau")
    time.sleep(1)
    LCD.clear()
    time.sleep(1)
