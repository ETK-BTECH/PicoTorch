from STPrg_base import STPrg_base_class
import utime

class STPrg_RunLine1(STPrg_base_class):
    ActColor = 0
    LastChangeTime = 0
    def __init__(self, LED):
        super().__init__(LED, 1, 500)
        self.map = ( (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0),
                     (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.5),
                     (0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0),
                     (1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                     (0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                     (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                     (1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                     (0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                     (0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
                     (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0),
                     (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5),
                     (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        self.colors = ( (255, 255, 255),
                        (255, 255,   0),
                        (255,   0,   0),
                        (  0, 255, 255),
                        (  0, 255,   0),
                        (255,   0, 255) )

    def Periodic(self, MaxStep):
        frlu = utime.ticks_ms() - STPrg_RunLine1.LastChangeTime
        if frlu > STPrg_base_class.Delay:
            ActMapRow = self.map[STPrg_base_class.StepCounter]
            (r, g, b) = self.colors[STPrg_RunLine1.ActColor]
            for i in range(16):
                STPrg_base_class.LED.set_pixel(i, r * ActMapRow[i], g * ActMapRow[i], b * ActMapRow[i])
            STPrg_base_class.LED.show(True)
            super().Periodic(len(self.map))
        
            STPrg_RunLine1.LastChangeTime = utime.ticks_ms()
        
    def SubBtnShort(self):
        STPrg_RunLine1.ActColor += 1
        if STPrg_RunLine1.ActColor >= len(self.colors):
            STPrg_RunLine1.ActColor = 0