from STPrg_base import STPrg_base_class
import utime

class STPrg_RotLine(STPrg_base_class):
    ActColor = 0
    LastChangeTime = 0
    def __init__(self, LED):
        super().__init__(LED, 1, 200)
        self.map = ( (1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0),
                     (0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0),
                     (0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0),
                     (0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1),
                     (0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0),
                     (0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0))
        self.colors = ( (255, 255, 255),
                        (255, 255,   0),
                        (255,   0,   0),
                        (  0, 255, 255),
                        (  0, 255,   0),
                        (255,   0, 255) )


    def Periodic(self, MaxStep):
        frlu = utime.ticks_ms() - STPrg_RotLine.LastChangeTime
        if frlu > STPrg_base_class.Delay:
            ActMapRow = self.map[STPrg_base_class.StepCounter]
            (r, g, b) = self.colors[STPrg_RotLine.ActColor]
            for i in range(16):
                if ActMapRow[i] == 0:
                    STPrg_base_class.LED.set_pixel(i, 0, 0, 0)
                else:
                    STPrg_base_class.LED.set_pixel(i, r, g, b)
            STPrg_base_class.LED.show(True)
            super().Periodic(len(self.map))
        
            STPrg_RotLine.LastChangeTime = utime.ticks_ms()
        
    def SubBtnShort(self):
        STPrg_RotLine.ActColor += 1
        if STPrg_RotLine.ActColor >= len(self.colors):
            STPrg_RotLine.ActColor = 0
            
    
        
    