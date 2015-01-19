import png

class PNGTools:

	BLACK_RGB = [0, 0, 0]
	WHITE_RGB = [255, 255, 255]

	MODIFY_PATH_COLOR_R = 0
	MODIFY_PATH_COLOR_G = 255
	MODIFY_PATH_COLOR_B = 0

	MODIFY_BLOCK_COLOR_R = 0
	MODIFY_BLOCK_COLOR_G = 0
	MODIFY_BLOCK_COLOR_B = 255

	BORDER_FACTOR = 2
	SIZE_RGB = 3

	"""
		Trim the original QR Code png picture
	"""
	def trim_border(self, filename, thickness):
		data = []
		for p in self._read_file(filename)[2]: # [2] = data
			data.append(p[thickness:-thickness])
		data = data[thickness:-thickness]
		self._write_file(filename, self._read_pixels(data), len(data))

	"""
		Generate the modify QR Code png picture with the solution
	"""
	def generate_png_path(self, path, filename_in, filename_out):
		data = []
		for p in self._read_file(filename_in)[2]:#[2] = data
			data.append(p)
		self._write_file(filename_out, self._modify_pixels_by(path, data), len(data))

	def _read_file(self, filename):
		return png.Reader(filename).read()

	def _write_file(self, filename, data, width):
		f = open(filename, 'wb')
		png.Writer(width, len(data)).write(f, data)
		f.close()

	"""
		Transform the original GRAY-BIT code of the png picture to a RGB one
	"""
	def _read_pixels(self, data):
		data_output = []
		for d in data:
			row = []
			for dd in d:
				if dd == 0:
					row.extend(PNGTools.BLACK_RGB)
				else:
					row.extend(PNGTools.WHITE_RGB)
			data_output.append(tuple(row))
		return data_output

	"""
		Draw the solution
	"""
	def _modify_pixels_by(self, pixels, data):
		width = len(list(data[0]))/PNGTools.SIZE_RGB
		height = len(data)
		for p in pixels:
			row = p/height
			col = PNGTools.SIZE_RGB*(p%width)
			new_row = list(data[row]) # The given data by pypng is in tuple and to modify a tuple, we have to convert it into list and then back to tuple
			
			#If it is a BLOCK case, we color it with the specified color, otherwise, we color the EMPTY case with the specified one
			if new_row[col+0] == PNGTools.BLACK_RGB[0] and new_row[col+1] == PNGTools.BLACK_RGB[1] and new_row[col+2] == PNGTools.BLACK_RGB[2]:
				new_row[col+0] = PNGTools.MODIFY_BLOCK_COLOR_R;new_row[col+1] = PNGTools.MODIFY_BLOCK_COLOR_G;new_row[col+2] = PNGTools.MODIFY_BLOCK_COLOR_B
			else:
				new_row[col+0] = PNGTools.MODIFY_PATH_COLOR_R;new_row[col+1] = PNGTools.MODIFY_PATH_COLOR_G;new_row[col+2] = PNGTools.MODIFY_PATH_COLOR_B				
			data[row] = tuple(new_row)
		return data