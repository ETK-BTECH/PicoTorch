import WS2812B
import machine
import utime

LEDMatrix = WS2812B.WS2812B(16, 0, 17, 0)
btn1 = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)
btn2 = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_DOWN)

RP1 = machine.ADC(26)
RP2 = machine.ADC(27)

LEDMatrix.fill(0, 0, 0)

LEDMatrix.set_pixel(0, 127, 127, 127)
LEDMatrix.set_pixel(3, 127, 0, 0)
LEDMatrix.set_pixel(4, 0, 127, 0)
LEDMatrix.show(True)

while True:
    
    print( RP1.read_u16(), end=' ... ')
    print( RP2.read_u16())
    
    
    if btn1.value() == 1:
        LEDMatrix.set_pixel(14, 0, 127, 0)
    else:
        LEDMatrix.set_pixel(14, 0, 0, 0)
    if btn2.value() == 1:
        LEDMatrix.set_pixel(15, 0, 127, 0)
    else:
        LEDMatrix.set_pixel(15, 0, 0, 0)
    
    LEDMatrix.show(True)
    utime.sleep(0.1)