from pngtools import PNGTools
from qrcodegenerator import QRCodeGenerator
from Queue import Queue

from graphsolver import GraphSolver

class Vertex:

	NO_DISTANCE = -1
	NO_PARENT = -1

	def __init__(self, id):
		self._id = id
		self._d = Vertex.NO_DISTANCE
		self._p = Vertex.NO_PARENT

	def get_id(self):
		return self._id

	def get_d(self):
		return self._d

	def get_p(self):
		return self._p

	def set_d(self, d):
		self._d = d

	def set_p(self, p):
		self._p = p

	def _to_string(self):
		output = str(self._id) + ' parent : ' 
		if self._p == Vertex.NO_PARENT:
			output += '- '
		else:
			output += str(self._p.get_id())

		return output + ', distance : ' + str(self._d)

	def __hash__(self):
		return self._id

	def __str__(self):
		return self._to_string()

	def __repr__(self):
		return self._to_string()

class Edge:

	def __init__(self, u, v, w):
		self._u = u
		self._v = v
		self._w = w

	def set_w(self, w):
		self._w = w

	def get_u(self):
		return self._u

	def get_v(self):
		return self._v

	def get_w(self):
		return self._w

	def _to_string(self):
		return str(self._u.get_id()) + ' =' + str(self._w) + '= > ' + str(self._v.get_id())

	def __str__(self):
		return self._to_string()

	def __repr__(self):
		return self._to_string()

class SimpleGraph:

	def __init__(self):
		self._vertices = []
		self._edges = {}

	def add_vertex(self, v):
		v = Vertex(v)
		self._vertices.append(v)
		self._edges[v] = []
		return v

	def add_edge(self, u, v, w):
		self._edges[u].append(Edge(u, v, w))

	def breadth_first_search(self, s, queue_extra_content=[]):
		for v in self._vertices:
			v.set_p(Vertex.NO_PARENT)
			v.set_d(Vertex.NO_DISTANCE)

		q = Queue()
		q.put(s)
		s.set_d(0)
		for v in queue_extra_content:
			q.put(v)
		
		tree = []
		while not q.empty():
			u = q.get()
			for e in self._edges[u]:
				v = e.get_v()
				if v.get_d() == Vertex.NO_DISTANCE:
					v.set_d(u.get_d() + e.get_w())
					v.set_p(u)
					tree.append(e)
					q.put(v)
		return tree

	def get_vertices(self):
		return self._vertices

	def get_edges(self):
		return self._edges

	def _to_string(self):
		s = ''
		for v in self._vertices:
			s += str(v.get_id()) + ' -> '
			if v in self._edges:
				for e in self._edges[v]:
					s += str(e) + ' |'

			s = s[:-1] + '\n'
		return s

	def __str__(self):
		return self._to_string()

	def __repr__(self):
		return self._to_string()

class SimpleGraphSolver:

	EMPTY_WEIGHT_EDGE = 0
	FULL_WEIGHT_EDGE = 1

	def __init__(self, message, filename):
		self._qr_code_generate = QRCodeGenerator()
		self._png_tools = PNGTools()
		self._filename = filename
		self._matrix = self._qr_code_generate.generate(message, filename)
		self._g = SimpleGraph()

		self._vertices = [] # #vertices = W*W
		self._edges = [] # #edges = W*(W-1)*2*2
		self._start_vertices = [] # #vertices = W
		self._exit_vertices = [] # #vertices = W

	# O(V^2)
	def init(self):
		self._generate_vertices()
		self._generate_edges()
		self._find_start_end_vertices()

		print self._g

	# O(V^2)
	def _generate_vertices(self):
		for i in range(0, len(self._matrix)):
			self._vertices.append([])
			for j in range(0, len(self._matrix[i])):
				self._vertices[-1].append(self._g.add_vertex(i*len(self._matrix) + j))
		
	# O(W*(W-1)*2*2) => O(W^2) => O(V)
	def _generate_edges(self):
		for i in range(0,len(self._matrix[0])):
			self._edges.append([])
			for j in range(0, len(self._matrix[i])):
				self._edges[-1].append([])
				self._compute_add_value_edge(i, j, SimpleGraphSolver.EMPTY_WEIGHT_EDGE, SimpleGraphSolver.FULL_WEIGHT_EDGE)

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

			e = self._g.add_edge(self._vertices[i][j], self._vertices[n[0]][n[1]], value)
			self._edges[-1][-1].append(e)

if __name__ == "__main__":
	message = 'D'#In matters of truth and justice, there is no difference between large and small problems, for issues concerning the treatment of people are all the same. Albert Einstein'
	filename_qr_code = 'code.png'

	solver = SimpleGraphSolver(message, filename_qr_code)
	solver.init()
