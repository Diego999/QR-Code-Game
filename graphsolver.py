from graph_tool.all import *

from pngtools import PNGTools
from qrcodegenerator import QRCodeGenerator

class GraphSolver(object):

	BLACK = '1'
	WHITE = '0'

	WHITE_FLOAT = [1, 1, 1, 1]
	BLACK_FLOAT = [0, 0, 0, 1]

	PATH_FLOAT = [0, 1, 0, 1]
	PATH_BLOCK_FLOAT = [0, 0, 1, 1]

	PREFIX_FILENAME_SOL = 's_'
	PREFIX_FILENAME_GRAPH = 'graph_'

	#Let W defines the number of vertices in one size of the QRCode (Anyway, a QRCode is a square) => V^1/2
	#Let V defines the number of vertices
	#Let E defines the number of edges

	def __init__(self, message, filename):
		self._qr_code_generate = QRCodeGenerator()

		self._png_tools = PNGTools()
		self._filename = filename
		self._matrix = self._qr_code_generate.generate(message, filename)
		self._g = Graph() # Directed Grid Graph
		self._vertices = [] # #vertices = W*W
		self._edges = [] # #edges = W*(W-1)*2*2
		self._start_vertices = [] # #vertices = W
		self._exit_vertices = [] # #vertices = W

		self._vertices_pos = self._g.new_vertex_property("vector<double>")
		self._vertices_color = self._g.new_vertex_property("vector<double>")
		self._weights = self._g.new_edge_property("double")

	# O(V^2)
	def init(self, value_white, value_black):
		self._generate_vertices()
		self._generate_edges(value_white, value_black)
		self._find_start_end_vertices()

	def draw_graph(self):
		graph_draw(self._g, vertex_text=self._g.vertex_index, pos=self._vertices_pos, vertex_fill_color=self._vertices_color, vertex_size=30, edge_text=self._weights, edge_pen_width=4, output_size=(1024*2,2*1024), edge_text_distance=0, edge_font_size=10, vertex_font_size=10, output=GraphSolver.PREFIX_FILENAME_GRAPH + self._filename)

	# O(V^2)
	def _generate_vertices(self):
		for i in range(0, len(self._matrix)):
			self._vertices.append([])
			for j in range(0, len(self._matrix[i])):
				self._vertices[-1].append(self._g.add_vertex())
				self._vertices_pos[self._vertices[i][j]] = (j, i)
				self._vertices_color[self._vertices[i][j]] = GraphSolver.WHITE_FLOAT if self._matrix[i][j] == GraphSolver.WHITE else GraphSolver.BLACK_FLOAT
		
	# O(W*(W-1)*2*2) => O(W^2) => O(V)
	def _generate_edges(self, value_empty, value_full):
		for i in range(0,len(self._matrix[0])):
			self._edges.append([])
			for j in range(0, len(self._matrix[i])):
				self._edges[-1].append([])
				self._compute_add_value_edge(i, j, value_empty, value_full)

	# O(2*W) => O(V^1/2)
	def _find_start_end_vertices(self):
		for j in range(0, len(self._matrix[0])):
			self._start_vertices.append(self._vertices[0][j])
			self._exit_vertices.append(self._vertices[-1][j])

	# O(4) => O(1)
	def _compute_add_value_edge(self, i, j, value_empty, value_full):
		tuples = [(-1,0),(1,0),(0,-1),(0,1)]
		neighboors = []
		for t in tuples:
			if i+t[0] >= 0 and i+t[0] < len(self._matrix[0]) and j+t[1] >= 0 and j+t[1] < len(self._matrix):
				neighboors.append((i+t[0], j+t[1]))

		current_value = self._matrix[i][j]
		for n in neighboors:
			neighboor_value = self._matrix[n[0]][n[1]]

			#Define the case where the weight of an edge should be EMPTY or FULL
			if neighboor_value == GraphSolver.WHITE and current_value == GraphSolver.WHITE or neighboor_value == GraphSolver.WHITE and current_value == GraphSolver.BLACK:
				value = value_empty 
			else:
				value = value_full

			e = self._g.add_edge(self._vertices[i][j], self._vertices[n[0]][n[1]])
			self._edges[-1][-1].append(e)
			self._weights[e] = value