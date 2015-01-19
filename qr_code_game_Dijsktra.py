import pyqrcode
import png
from graph_tool.all import *
from pngtools import PNGTools
from qrcodegenerator import QRCodeGenerator

class GraphSolver:

	BLACK = '1'
	WHITE = '0'

	WHITE_FLOAT = [1, 1, 1, 1]
	BLACK_FLOAT = [0, 0, 0, 1]

	PATH_FLOAT = [0, 1, 0, 1]
	PATH_BLOCK_FLOAT = [0, 0, 1, 1]

	EMPTY_WEIGHT_EDGE = 0.0000001 # With this weight, we minimize also the number of EMPTY cases
	FULL_WEIGHT_EDGE = 1

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
	def init(self):
		self._generate_vertices()
		self._generate_edges()
		self._find_start_end_vertices()

	def draw_graph(self):
		graph_draw(self._g, vertex_text=self._g.vertex_index, pos=self._vertices_pos, vertex_fill_color=self._vertices_color, vertex_size=30, edge_text=self._weights, edge_pen_width=4, output_size=(1024*2,2*1024), edge_text_distance=0, edge_font_size=10, vertex_font_size=10, output=GraphSolver.PREFIX_FILENAME_GRAPH + self._filename)

	# O(V^(3/2) LgV)
	def solve(self):
		min_dist = 100000
		pair_vertex = ()
		tree = None
		# V^1/2 loops, => O(V^(3/2) lgV)
		for start_vertex in self._start_vertices:
			# O(V lgV), cf Documentation
			dist, pred = dijkstra_search(self._g, start_vertex, self._weights)

			# O(V^1/2)
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
		
		path = path[::-1]

		for p in path:
			r = p/len(self._matrix)
			c = p%len(self._matrix[0])
			self._vertices_color[self._vertices[r][c]] = GraphSolver.PATH_FLOAT if self._matrix[r][c] == GraphSolver.WHITE else GraphSolver.PATH_BLOCK_FLOAT

		self._png_tools.generate_png_path(path, self._filename, GraphSolver.PREFIX_FILENAME_SOL + self._filename)

	# O(V^2)
	def _generate_vertices(self):
		for i in range(0, len(self._matrix)):
			self._vertices.append([])
			for j in range(0, len(self._matrix[i])):
				self._vertices[-1].append(self._g.add_vertex())
				self._vertices_pos[self._vertices[i][j]] = (j, i)
				self._vertices_color[self._vertices[i][j]] = GraphSolver.WHITE_FLOAT if self._matrix[i][j] == GraphSolver.WHITE else GraphSolver.BLACK_FLOAT
		
	# O(W*(W-1)*2*2) => O(W^2) => O(V)
	def _generate_edges(self):
		for i in range(0,len(self._matrix[0])):
			self._edges.append([])
			for j in range(0, len(self._matrix[i])):
				self._edges[-1].append([])
				self._compute_add_value_edge(i, j)

	# O(2*W) => O(V^1/2)
	def _find_start_end_vertices(self):
		for j in range(0, len(self._matrix[0])):
			self._start_vertices.append(self._vertices[0][j])
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

			#Define the case where the weight of an edge should be EMPTY or FULL
			if neighboor_value == GraphSolver.WHITE and current_value == GraphSolver.WHITE or neighboor_value == GraphSolver.WHITE and current_value == GraphSolver.BLACK:
				value = GraphSolver.EMPTY_WEIGHT_EDGE
			else:
				value = GraphSolver.FULL_WEIGHT_EDGE

			e = self._g.add_edge(self._vertices[i][j], self._vertices[n[0]][n[1]])
			self._edges[-1][-1].append(e)
			self._weights[e] = value

if __name__ == "__main__":
	message = 'Test'#In matters of truth and justice, there is no difference between large and small problems, for issues concerning the treatment of people are all the same. Albert Einstein'
	filename_qr_code = 'code.png'

	solver = GraphSolver(message, filename_qr_code)
	solver.init()
	solver.solve()
	#solver.draw_graph()
