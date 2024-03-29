import simplejson

class NeopixelStrip(object):

    def __init__(self, length):
        self.length = length
        self.pixel_array = []
        self._shown = False

        for i in range(self.length):
            new_pixel = Pixel()
            self.pixel_array.append(new_pixel)
    
    def change_pixel_value(self, pixel, r, g, b):
        new_pixel = Pixel()
        new_pixel.r = r
        new_pixel.g = g
        new_pixel.b = b
        self.pixel_array[pixel] = new_pixel
        #if new_pixel != self.pixel_array[pixel]:
        #    self.pixel_array[pixel] = new_pixel
        #    self._shown = False
        #    return True
        #return False
        return True

    def show(self):
        self._shown = True

    def has_been_shown(self):
        return self._shown        

    def __json__(self):
        return simplejson.dumps(self.pixel_array, for_json=True)
    
    for_json = __json__

class Pixel(object):

    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0

    def __eq__(self, other):
        if isinstance(other, Pixel):
            if other.r == self.r and other.g == self.g and other.b == self.b:
                return True
            return False
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __json__(self):
        return [self.r, self.g, self.b]
    
    for_json = __json__
            