import colorsys
import struct
import random

class Theme:
	def __iter__(self):
		return self;
	def next(self):
		return (0, 0, 0)

class StaticColor(Theme):
	def __init__(self, h):
		h = h[1:]
		r,g,b = struct.unpack('BBB',h.decode('hex'))
		self.color = (r/255.0, g/255.0, b/255.0)
	def next(self):
		return self.color

class Rainbow(Theme):
	def __init__(self, period, intensity):
		self.i = 0
		self.period = float(period)
		self.intensity = float(intensity)
	def next(self):
		self.i += 1
		self.i = self.i % self.period
		return colorsys.hsv_to_rgb(self.i/self.period, 1, self.intensity)

class Strobe(Theme):
	def __init__(self, black_period, light_period):
		self.bt = black_period
		self.lt = light_period
		self.i = 0
		self.black = True
	def next(self):
		self.i += 1
		period = self.bt if self.black else self.lt
		if (self.i % period == 0):
			self.black = not self.black
			self.i = 0
		ret = (0,0,0) if self.black else (1, 1, 1)
		return ret

class RandomStrobe(Theme):
	def __init__(self, black_period, light_period):
		self.bt = black_period
		self.lt = light_period
		self.i = 0
		self.black = True
		self.color = (1,1,1)
	def next(self):
		self.i += 1
		period = self.bt if self.black else self.lt
		if (self.i % period == 0):
			self.black = not self.black
			self.i = 0
			self.color = colorsys.hsv_to_rgb(random.random(),1,0.8)
		ret = (0,0,0) if self.black else self.color
		return ret

def interpolate(s, e, a):
	return (s[0]+(e[0]-s[0])*a, s[1]+(e[1]-s[1])*a, s[2]+(e[2]-s[2])*a)

class RGBGradient(Theme):
	def __init__(self, start, end, period):
		self.s = start
		self.e = end
		self.period = period
		self.i = 0
	def next(self):
		self.i += 1
		self.i = self.i % self.period
		alpha = abs(self.i-(self.period/2))/(self.period/2.0)
		return interpolate(self.s, self.e, alpha)

class HSVGradient(Theme):
	def __init__(self, start, end, period):
		self.s = start
		self.e = end
		self.period = period
		self.i = 0
	def next(self):
		self.i += 1
		self.i = self.i % self.period
		alpha = abs(self.i-(self.period/2))/(self.period/2.0)
		return colorsys.hsv_to_rgb(interpolate(self.s, self.e, alpha))
