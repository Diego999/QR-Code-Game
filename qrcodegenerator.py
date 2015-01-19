import pyqrcode
from pngtools import PNGTools

class QRCodeGenerator:

	BOUND = 1
	SEPARATOR = '\n'

	def __init__(self):
		self._png_tools = PNGTools()

	def generate(self, message, filename):
		qrcode =  pyqrcode.create(message)
		qrcode.png(filename)
		self._png_tools.trim_border(filename, QRCodeGenerator.BOUND)
		return self._transform_to_matrix(qrcode)

	def _transform_to_matrix(self, qrcode):
		matrix = []
		for r in qrcode.text().split(QRCodeGenerator.SEPARATOR):
			matrix.append(r[QRCodeGenerator.BOUND:-QRCodeGenerator.BOUND])
		matrix = matrix[QRCodeGenerator.BOUND:-QRCodeGenerator.BOUND]
		return matrix