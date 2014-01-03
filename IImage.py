from PIL import Image, ImageDraw

class IImage(object):

	def __init__(self, arg):
		if type(arg) == type('path'):
			self.pil = Image.open(arg, 'r')
		elif type(arg) == type(('size', 'tuple')):
			self.pil = Image.new('RGBA', arg, 'black')
		else:
			self.pil = arg
		self.width, self.height = self.pil.size

	def save(self, path, extension='JPEG', quality=80):
		self.pil.save(path, extension, quality=quality)
		return self

	def flipH(self):
		data = (self.width, 0, 0, self.height)
		self.pil = self.pil.transform((self.width,self.height), Image.EXTENT, data)
		return self

	def flipV(self):
		data = (0, self.height, self.width, 0)
		self.pil = self.pil.transform((self.width,self.height), Image.EXTENT, data)
		return self

	def flipHV(self):
		return self.flipH().flipV()

	def flipVH(self):
		return self.flipV().flipH()

	def rotate(self, angle):
		self.pil = self.pil.rotate(angle)
		return self

	def paste(self, iimg, x, y):
		self.pil.paste(iimg.pil, (x,y))
		return self

	def thumbnail(self, width, height, mode):
		self.pil.thumbnail((width,height), mode)
		return self

	def compositeWith(self, iimg, mask):
		self.pil = Image.composite(self.pil, iimg.pil, mask.pil.convert('L'))
		return self

	def fillPolygon(self, points, color):
		maskdraw = ImageDraw.Draw(self.pil)
		maskdraw.polygon(points, color)
		return self

	def copy(self):
		return IImage(self.pil.copy())

	def makeSquare(self):
		side = min(self.width, self.height)
		box = (
			(self.width - side) // 2,
			(self.height - side) // 2,
			(self.width + side) // 2,
			(self.height + side) // 2
		)
		self.pil = self.pil.crop(box)
		return self
	
	def mirrorTopLeft(self):
		points = [
			(0, 0),
			(0, self.height),
			(self.width, 0)
		]
		mask = IImage((self.width, self.height))
		mask.fillPolygon(points, "white")
		rotated = self.copy().rotate(-90).flipV()
		self.compositeWith(rotated, mask)
		return self

	def mirrorTopRight(self):
		points = [
			(0, 0),
			(self.width, 0),
			(self.width, self.height)
		]
		mask = IImage((self.width, self.height))
		mask.fillPolygon(points, "white")
		rotated = self.copy().rotate(90).flipV()
		self.compositeWith(rotated, mask)
		return self

	def mirrorBottomLeft(self):
		points = [
			(0, 0),
			(0, self.height),
			(self.width, self.height)
		]
		mask = IImage((self.width, self.height))
		mask.fillPolygon(points, "white")
		rotated = self.copy().rotate(90).flipV()
		self.compositeWith(rotated, mask)
		return self

	def mirrorBottomRight(self):
		points = [
			(0, self.height),
			(self.width, self.height),
			(self.width, 0)
		]
		mask = IImage((self.width, self.height))
		mask.fillPolygon(points, "white")
		rotated = self.copy().rotate(-90).flipV()
		self.compositeWith(rotated, mask)
		return self

	def blendWith(self, iimg, alpha=0.5):
		self.pil = Image.blend(self.pil, iimg.pil, alpha)
		return self

	def kaleidoscope(self):
		img0 = self.copy().flipH()
		img1 = self.copy().flipV()
		img2 = self.copy().flipHV()
		self = IImage.combine(self, img0, img1, img2)
		return self

	@classmethod
	def combine(cls, iimg0, iimg1, iimg2, iimg3):
		width, height = iimg0.width, iimg0.height
		newSize = (width*2, height*2)
		canvas = IImage(newSize)
		canvas.paste(iimg0, 0, 0)
		canvas.paste(iimg1, width, 0)
		canvas.paste(iimg2, 0, height)
		canvas.paste(iimg3, width, height)

		return canvas.thumbnail(width, height, Image.NEAREST)
