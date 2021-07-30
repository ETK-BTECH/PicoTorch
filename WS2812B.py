import array, time
from machine import Pin
import rp2

@rp2.asm_pio (sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)                .side(0)   [T3 - 1]
    jmp(not_x, "do_zero")    .side(1)   [T1 - 1]
    jmp("bitloop")            .side(1)   [T2 - 1]
    label("do_zero")
    nop()                    .side(0)   [T2 - 1]
    wrap()
    
    
class WS2812B:
    def __init__ (self, num_leds, state_machine, pin, delay=0.001):
        self.pixels = array.array ("I", [0 for _ in range(num_leds)])
        self.GCpixels = array.array ("I", [0 for _ in range(num_leds)])
        self.sm = rp2.StateMachine (state_machine, ws2812, freq=8000000, sideset_base=Pin(pin))
        self.sm.active (1)
        self.num_leds = num_leds
        self.delay = delay
        self.brightnessvalue = 255
        self.GAMMA_CORRECT_FACTOR = 2.8
        
    # Set the overal value to adjust brightness when updating LEDs
    def brightness (self, brightness = None):
        if brightness == None:
            return self.brightnessvalue
        else:
            if (brightness < 1):
                brightness = 1
            elif (brightness > 255):
                brightness = 255
        for i in range(self.num_leds):
            red = (self.pixels[i] & 0x0000FF00) >> 8
            green = (self.pixels[i] & 0x00FF0000) >> 16
            blue = self.pixels[i] & 0x000000FF
            red = red / (self.brightnessvalue / 255)
            green = green / (self.brightnessvalue / 255)
            blue = blue / (self.brightnessvalue / 255)
            nblue = round(blue * (brightness / 255))
            nred = round(red * (brightness / 255))
            ngreen = round(green * (brightness / 255))
            self.pixels[i] = nblue | nred << 8 | ngreen << 16
        self.brightnessvalue = brightness
        
    # Create a gradient with two RGB colors between "pixel1" and "pixel2 (inclusive)
    def set_pixel_line_gradient (self, pixel1, pixel2, left_red, left_green, left_blue, right_red, right_green, right_blue):
        if pixel2 - pixel1 == 0: return
        right_pixel = max (pixel1, pixel2)
        left_pixel = min (pixel1, pixel2)
        for i in range(right_pixel - left_pixel + 1):
            fraction = i / (right_pixel - left_pixel)
            red = round((right_red - left_red) * fraction + left_red)
            green = round((right_green - left_green) * fraction + left_green)
            blue = round((right_blue - left_blue) * fraction + left_blue)
            self.set_pixel(left_pixel + i, red, green, blue)
            
    # Set an array of pixels starting from "pixel1" to "pixel2" to the desired color
    def set_pixel_line (self, pixel1, pixel2, red, green, blue):
        for i in range(pixel1, pixel2 + 1):
            self.set_pixel(i, red, green, blue)
            
    def set_pixel (self, pixel_num, red, green, blue):
        # Adjust color values with brightness level
        blue = round(blue * (self.brightness() / 255))
        red = round(red * (self.brightness() / 255))
        green = round(green * (self.brightness() / 255))
        self.pixels[pixel_num] = blue | red << 8 | green << 16
    
    # Rotate x pixels to the left
    def rotate_left (self, num_of_pixels):
        if num_of_pixels == None:
            num_of_pixels = 1
        self.pixels = self.pixels[num_of_pixels:] + self.pixels[:num_of_pixels]
    
    # Rotate x pixels to the right
    def rotate_right (self, num_of_pixels):
        if num_of_pixels == None:
            num_of_pixels = 1
        num_of_pixels = -1 * num_of_pixels
        self.pixels = self.pixels[num_of_pixels:] + self.pixels[:num_of_pixels]
        
    def show(self, GammaCorrection=False):
        if GammaCorrection:
            for i in range(self.num_leds):
                red = (self.pixels[i] & 0x0000FF00) >> 8
                green = (self.pixels[i] & 0x00FF0000) >> 16
                blue = self.pixels[i] & 0x000000FF
                self.GCpixels[i] = self.gamma_correct(blue) | self.gamma_correct(red) << 8 | self.gamma_correct(green) << 16
            for i in range(self.num_leds):
                self.sm.put(self.GCpixels[i], 8)
        else:
            for i in range(self.num_leds):
                self.sm.put(self.pixels[i], 8)
        time.sleep(self.delay)
    
    def fill(self, red, green, blue):
        for i in range(self.num_leds):
            self.set_pixel(i, red, green, blue)
        time.sleep(self.delay)

    def gamma_correct(self, led_val):
        max_val = (1 << 8) - 1.0
        corrected = pow(led_val / max_val, self.GAMMA_CORRECT_FACTOR) * max_val
        return int(min(255, max(0, corrected)))