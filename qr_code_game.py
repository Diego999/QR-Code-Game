import pyqrcode
import png
from graph_tool.all import *

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

	def trim_border(self, filename, thickness):
		(width, height, pixels, metadata) = self._read_file(filename)
		width -= PNGTools.BORDER_FACTOR*thickness
		height -= PNGTools.BORDER_FACTOR*thickness

		data = []
		for p in pixels:
			data.append(p[thickness:-thickness])
		data = data[thickness:-thickness]

		self._write_file(filename, self._read_pixels(data), len(data))

	def generate_png_path(self, path, filename_in, filename_out):
		(width, height, pixels, metadata) = self._read_file(filename_in)

		data = []
		for p in pixels:
			data.append(p)

		self._write_file(filename_out, self._modify_pixels_by(path, data), len(data))

	def _read_file(self, filename):
		return png.Reader(filename).read()

	def _write_file(self, filename, data, width):
		f = open(filename, 'wb')
		png.Writer(width, len(data)).write(f, data)
		f.close()

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

	def _modify_pixels_by(self, pixels, data):
		width = len(list(data[0]))/PNGTools.SIZE_RGB
		height = len(data)
		for p in pixels:
			row = p/height
			col = PNGTools.SIZE_RGB*(p%width)
			new_row = list(data[row])
			if new_row[col+0] == PNGTools.BLACK_RGB[0] and new_row[col+1] == PNGTools.BLACK_RGB[1] and new_row[col+2] == PNGTools.BLACK_RGB[2]:
				new_row[col+0] = PNGTools.MODIFY_BLOCK_COLOR_R;new_row[col+1] = PNGTools.MODIFY_BLOCK_COLOR_G;new_row[col+2] = PNGTools.MODIFY_BLOCK_COLOR_B
			else:
				new_row[col+0] = PNGTools.MODIFY_PATH_COLOR_R;new_row[col+1] = PNGTools.MODIFY_PATH_COLOR_G;new_row[col+2] = PNGTools.MODIFY_PATH_COLOR_B				
			data[row] = tuple(new_row)
		return data

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

class GraphSolver:

	BLACK = '1'
	WHITE = '0'

	WHITE_FLOAT = [1, 1, 1, 1]
	BLACK_FLOAT = [0, 0, 0, 1]

	PATH_FLOAT = [0, 1, 0, 1]
	PATH_BLOCK_FLOAT = [0, 0, 1, 1]

	EMPTY_WEIGHT_EDGE = 0.0000001 # With this weight, we minize also the number of EMPTY BLOCK
	FULL_WEIGHT_EDGE = 1

	PREFIX_FILENAME_SOL = 's_'
	PREFIX_FILENAME_GRAPH = 'graph_'

	#Let W defines the number of vertices in one size of the QRCode (Anyway, a QRCode is a square)
	#Let V defines the number of vertices
	#Let E defines the number of edges

	def __init__(self, message, filename):
		self._qr_code_generate = QRCodeGenerator()

		self._png_tools = PNGTools()
		self._filename = filename
		self._matrix = self._qr_code_generate.generate(message, filename_qr_code)
		self._g = Graph() #Grid Graph
		self._vertices = [] # #vertices = W*W
		self._edges = [] # #edges = W*(W-1)*2*2
		self._start_vertices = [] # #vertices = W
		self._exit_vertices = [] # #vertices = W

		self._vertices_pos = self._g.new_vertex_property("vector<double>")
		self._vertices_color = self._g.new_vertex_property("vector<double>")
		self._weights = self._g.new_edge_property("double")

	# O(V^2)
	def init(self):
		self._generate_vertices()
		self._generate_edges()
		self._find_start_end_vertices()

	def draw_graph(self):
		graph_draw(self._g, vertex_text=self._g.vertex_index, pos=self._vertices_pos, vertex_fill_color=self._vertices_color, vertex_size=30, edge_text=self._weights, edge_pen_width=4, output_size=(1024*2,2*1024), edge_text_distance=0, edge_font_size=10, vertex_font_size=10, output=GraphSolver.PREFIX_FILENAME_GRAPH + self._filename)

	# O(V^V LgV)
	def solve(self):
		min_dist = 100000
		pair_vertex = ()
		tree = None
		# V loops, => O(V^2 lgV)
		for start_vertex in self._start_vertices:
			# O(V lgV), cf Documentation
			dist, pred = dijkstra_search(self._g, start_vertex, self._weights)

			# O(V)
			for exit_vertex in self._exit_vertices:
				current_dist = dist[exit_vertex]
				r = int(start_vertex)/len(self._matrix)
				c = int(start_vertex)%len(self._matrix[0])

				#Take into account if the start vertex is a BLOCK, we have to count its destruction
				if self._matrix[r][c] == GraphSolver.BLACK: 
					current_dist += GraphSolver.FULL_WEIGHT_EDGE

				if current_dist < min_dist:
					pair_vertex = (start_vertex, exit_vertex)
					min_dist = current_dist
					tree = pred

		node = pair_vertex[1]
		path = [int(node), tree[node]]
		while tree[node] != self._g.vertex_index[pair_vertex[0]]:
			node = self._g.vertex(tree[node])
			path.append(tree[node])
		
		path = self._clean_path(path)

		for p in path:
			r = p/len(self._matrix)
			c = p%len(self._matrix[0])
			self._vertices_color[self._vertices[r][c]] = GraphSolver.PATH_FLOAT if self._matrix[r][c] == GraphSolver.WHITE else GraphSolver.PATH_BLOCK_FLOAT

		self._png_tools.generate_png_path(path, self._filename, GraphSolver.PREFIX_FILENAME_SOL + self._filename)

	# O(len(path)) => O(n) but it practice nearly O(1)
	def _clean_path(self, path):
		flag = False
		start = 0
		while not flag:
			if path[start] >= (len(self._matrix)-1)*len(self._matrix[0]) and path[start+1] >= (len(self._matrix)-1)*len(self._matrix[0]) and self._matrix[-1][path[start+1]%len(self._matrix[-1])] == '0':
				start += 1
			else:
				flag = True
		path = path[start:]
		path = path[::-1]

		flag = False
		start = 0
		while not flag:
			if path[start] < len(self._matrix[0]) and path[start+1] < len(self._matrix[0]) and self._matrix[0][path[start+1]] == GraphSolver.WHITE:
				start += 1
			else:
				flag = True
		return path[start:]

	# O(V^2)
	def _generate_vertices(self):
		for i in range(0, len(self._matrix)):
			self._vertices.append([])
			for j in range(0, len(self._matrix[i])):
				self._vertices[-1].append(self._g.add_vertex())
				self._vertices_pos[self._vertices[i][j]] = (j, i)
				if self._matrix[i][j] == GraphSolver.WHITE:
					self._vertices_color[self._vertices[i][j]] = GraphSolver.WHITE_FLOAT
				else:
					self._vertices_color[self._vertices[i][j]] = GraphSolver.BLACK_FLOAT
		
	# O(W*(W-1)*2*2) => O(W^2) => O(V^2)
	def _generate_edges(self):
		for i in range(0,len(self._matrix[0])):
			self._edges.append([])
			for j in range(0, len(self._matrix[i])):
				self._edges[-1].append([])
				self._compute_add_value_edge(i, j)

	# O(2*W) => O(W)
	def _find_start_end_vertices(self):
		for j in range(0, len(self._matrix[0])):
			self._start_vertices.append(self._vertices[0][j])

		for j in range(0, len(self._matrix[-1])):
			self._exit_vertices.append(self._vertices[-1][j])

	# O(4) => O(1)
	def _compute_add_value_edge(self, i, j):
		tuples = [(-1,0),(1,0),(0,-1),(0,1)]
		neighboors = []
		for t in tuples:
			if i+t[0] >= 0 and i+t[0] < len(self._matrix[0]) and j+t[1] >= 0 and j+t[1] < len(self._matrix):
				neighboors.append((i+t[0], j+t[1]))

		current_value = self._matrix[i][j]
		for n in neighboors:
			neighboor_value = self._matrix[n[0]][n[1]]

			if neighboor_value == GraphSolver.WHITE and current_value == GraphSolver.WHITE or neighboor_value == GraphSolver.WHITE and current_value == GraphSolver.BLACK:
				value = GraphSolver.EMPTY_WEIGHT_EDGE
			else:
				value = GraphSolver.FULL_WEIGHT_EDGE

			e = self._g.add_edge(self._vertices[i][j], self._vertices[n[0]][n[1]])
			self._edges[-1][-1].append(e)
			self._weights[e] = value

if __name__ == "__main__":
	message = 'DIEGO ROCKS !'
	filename_qr_code = 'code.png'

	solver = GraphSolver(message, filename_qr_code)
	solver.init()
	solver.solve()
	solver.draw_graph()
