import machine
import WS2812B
import utime
import math
from STPrg_RotLine import STPrg_RotLine
from STPrg_RunLine import STPrg_RunLine1
from STPrg_Warning import STPrg_Warning1

btnYellow_pt = None
btnOrange_pt = None
ActProgram = 0
TorchMode = False

def btnYellow_callback(param):
    global btnYellow_pt
    global ActProgram
    global STPrograms
    if btnYellow.value() == 1 and btnYellow_pt == None:
        btnYellow_pt = utime.ticks_ms()
    elif btnYellow.value() == 0 and btnYellow_pt != None:
        btnYellow_pd = utime.ticks_ms() - btnYellow_pt
        btnYellow_pt = None
        if btnYellow_pd > 100:
            if btnYellow_pd < 500:
                STPrograms[ActProgram].SubBtnShort()
            else:
                STPrograms[ActProgram].SubBtnLong()

def btnOrange_callback(param):
    global btnOrange_pt
    global ActProgram
    global STPrograms
    if btnOrange.value() == 1 and btnOrange_pt == None:
        btnOrange_pt = utime.ticks_ms()
    elif btnOrange.value() == 0 and btnOrange_pt != None:
        btnOrange_pd = utime.ticks_ms() - btnOrange_pt
        btnOrange_pt = None
        if btnOrange_pd > 100:
            if btnOrange_pd < 500:
                ActProgram += 1
                if ActProgram >= len(STPrograms):
                    ActProgram = 0
                STPrograms[ActProgram].PrgReset()
            else:
                pass

LEDMatrix = WS2812B.WS2812B(16, 0, 17, 0)
RP1 = machine.ADC(26)
RP1_val = math.floor(RP1.read_u16() * 215 / 65535) + 40
LEDMatrix.brightness (RP1_val)
LastBrightness = RP1_val

btnYellow = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)
btnOrange = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_DOWN)
btnYellow.irq(trigger = machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=btnYellow_callback)
btnOrange.irq(trigger = machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=btnOrange_callback)

STPrograms = ( STPrg_Warning1(LEDMatrix),
               STPrg_RotLine(LEDMatrix),
               STPrg_RunLine1(LEDMatrix) )

RP2 = machine.ADC(27)
RP2_val = RP2.read_u16() * 100 / 65535
LastSpeed = RP2_val
STPrograms[ActProgram].SpeedSet(RP2_val)


while True:
    RP1_val = math.floor(RP1.read_u16() * 215 / 65535) + 40
    if LastBrightness != RP1_val:
        LEDMatrix.brightness (RP1_val)
        LastBrightness = RP1_val
        if TorchMode:
            LEDMatrix.show(True)
    RP2_val = RP2.read_u16() * 100 / 65535
    if LastSpeed != RP2_val:
        STPrograms[ActProgram].SpeedSet(RP2_val)
        LastSpeed = RP2_val
    if btnOrange.value() == 1:
        btnOrPD = utime.ticks_ms() - btnOrange_pt
        if btnOrPD > 1000:
            TorchMode = True
            LEDMatrix.fill(255, 255, 255)
            LEDMatrix.show(True)
    else:
        TorchMode = False
    if not TorchMode:
        STPrograms[ActProgram].Periodic(0)

    

