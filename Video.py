import subprocess
import os, sys

class Video:
	def __init__(self, path=''):
		# TODO: find a video library
		self.path = path
		self.filename = os.path.split(self.path)[1]
		if '.' in self.filename:
			self.filename = self.filename[:self.filename.rindex('.')]

	def toFrames(self,):
		outputDir = self.filename + '_frames/'
		
		if not os.path.exists(outputDir):
			subprocess.call(['mkdir', outputDir])

		# TODO: Read from file
		frameRate = "24" 
		frameSize = "1280x720"

		subprocess.call([
			"ffmpeg",
			"-i", self.path, # Input path
			"-an", # Disable audio
			"-sameq", # Same quality as source
			"-r", frameRate, # Frame rate
			"-s", frameSize , # Frame size
			outputDir + self.filename + "%d.jpg"	#output path
		])

