from IImage import IImage
import subprocess
import os, sys

class Pattern:
	def __init__(self, paths):
		self.folder = os.path.split(paths)[0]
		self.filenames = os.path.split(paths)[1]
		self.imgPaths = paths
		self.imgNumber = len(os.listdir(self.folder))

		if '.' in self.filenames:
			self.extension = self.filenames[self.filenames.rindex('.'):]

	def toVideo(self, outputPath='output.mpg', frameRate="24"):
		subprocess.call([
			"ffmpeg",
			"-r", frameRate,		#frame rate
			"-i", self.imgPaths,	#input path
			"-qscale", '1',			#same quality as source
			"-y", 					#overwrite output
			outputPath				#output path
		])
		return self

	def apply(self, methodList):
		for method in methodList:
			for n in range(1, self.imgNumber+1):
				displayProgress('Applying '+method, n, self.imgNumber)
				imgPath = self.imgPaths % n
				iimg = IImage(imgPath)
				iimg = getattr(iimg, method)()
				iimg.save(imgPath)
		return self

def displayProgress(text, n, total):
	sys.stdout.write("\r" + text + " %.2f%%" % (n*100/float(total)))
	sys.stdout.flush()
	if n==total:
		sys.stdout.write("\n")
