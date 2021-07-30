import WS2812B
import time

class STPrg_base_class:
    StepCounter = 0
    LED = None
    MinDelay = 0
    MaxDelay = 100
    Delay = 10
        
    def __init__(self, LED, MinDelay, MaxDelay):
        STPrg_base_class.LED = LED
        STPrg_base_class.MinDelay = MinDelay
        STPrg_base_class.MaxDelay = MaxDelay

    def StepUpdate(self):
        pass
    
    def Periodic(self, MaxStep):
        STPrg_base_class.StepCounter += 1
        if(STPrg_base_class.StepCounter >= MaxStep):
            STPrg_base_class.StepCounter = 0
            
    def SubBtnShort(self):
        pass
    
    def SubBtnLong(self):
        pass
    
    def SpeedSet(self, SpeedPercentage):
        dStep = (STPrg_base_class.MaxDelay - STPrg_base_class.MinDelay) / 100
        STPrg_base_class.Delay = (dStep * SpeedPercentage) + STPrg_base_class.MinDelay
        
    def PrgReset(self):
        STPrg_base_class.StepCounter = 0
        