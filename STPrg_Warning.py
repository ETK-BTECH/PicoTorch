from STPrg_base import STPrg_base_class
import utime

class STPrg_Warning1(STPrg_base_class):
    LastChangeTime = 0
    Submode = 0
    def __init__(self, LED):
        super().__init__(LED, 1000, 10000)
        self._LED = LED
        self.Delay = 50
        

    def Periodic(self, MaxStep):
        frlu = utime.ticks_ms() - STPrg_Warning1.LastChangeTime
        if STPrg_Warning1.Submode == 0:
            self.r = 255
            self.g = 0
            self.b = 0
        elif STPrg_Warning1.Submode == 1:
            self.r = 255
            self.g = 255
            self.b = 255
        if frlu > self.Delay:
            if STPrg_base_class.StepCounter == 0:
                self._LED.fill(100, 0, 0)
                self._LED.set_pixel(0, self.r, self.g, self.b)
                self._LED.set_pixel(3, self.r, self.g, self.b)
                self._LED.set_pixel(12, self.r, self.g, self.b)
                self._LED.set_pixel(15, self.r, self.g, self.b)
                self.Delay = 50
            elif STPrg_base_class.StepCounter == 1:
                self._LED.fill(100, 0, 0)
                self._LED.set_pixel(0, 0, 0, 0)
                self._LED.set_pixel(3, 0, 0, 0)
                self._LED.set_pixel(12, 0, 0, 0)
                self._LED.set_pixel(15, 0, 0, 0)
                self.Delay = 50
            elif STPrg_base_class.StepCounter == 2:
                self._LED.fill(100, 0, 0)
                self._LED.set_pixel(0, self.r, self.g, self.b)
                self._LED.set_pixel(3, self.r, self.g, self.b)
                self._LED.set_pixel(12, self.r, self.g, self.b)
                self._LED.set_pixel(15, self.r, self.g, self.b)
                self.Delay = 50
            elif STPrg_base_class.StepCounter == 3:
                self._LED.fill(100, 0, 0)
                self._LED.set_pixel(0, 0, 0, 0)
                self._LED.set_pixel(3, 0, 0, 0)
                self._LED.set_pixel(12, 0, 0, 0)
                self._LED.set_pixel(15, 0, 0, 0)
                self.Delay = 50
            elif STPrg_base_class.StepCounter == 4:
                self._LED.fill(100, 0, 0)
                self._LED.set_pixel(0, self.r, self.g, self.b)
                self._LED.set_pixel(3, self.r, self.g, self.b)
                self._LED.set_pixel(12, self.r, self.g, self.b)
                self._LED.set_pixel(15, self.r, self.g, self.b)
                self.Delay = 50
            elif STPrg_base_class.StepCounter == 5:
                self._LED.fill(100, 0, 0)
                self._LED.set_pixel(0, 0, 0, 0)
                self._LED.set_pixel(3, 0, 0, 0)
                self._LED.set_pixel(12, 0, 0, 0)
                self._LED.set_pixel(15, 0, 0, 0)
                self.Delay = STPrg_base_class.Delay
            self._LED.show(True)
            super().Periodic(6)
            STPrg_Warning1.LastChangeTime = utime.ticks_ms()
        
    def SubBtnShort(self):
        STPrg_Warning1.Submode += 1
        if STPrg_Warning1.Submode >= 2:
            STPrg_Warning1.Submode = 0