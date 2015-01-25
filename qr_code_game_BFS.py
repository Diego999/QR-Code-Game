from pngtools import PNGTools
from qrcodegenerator import QRCodeGenerator
from collections import deque

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
		self._start = 0

	def add_vertex(self, v):
		v = Vertex(v)
		self._vertices.append(v)
		self._edges[v] = []
		return v

	def add_edge(self, u, v, w):
		e = Edge(u, v, w)
		self._edges[u].append(e)
		return e

	def remove_edge(self, e):
		u = e.get_u()
		self._edges[u].remove(e)

	def breadth_first_search(self,queue_content = []):
		for v in self._vertices:
			v.set_p(Vertex.NO_PARENT)
			v.set_d(Vertex.NO_DISTANCE)

		q = deque()
		for v in queue_content:
			q.append(v)
			v.set_d(0)

		tree = []
		while q:
			u = q.popleft()
			for e in self._edges[u]:
				v = e.get_v()
				if v.get_d() == Vertex.NO_DISTANCE:
					v.set_d(u.get_d() + e.get_w())
					v.set_p(u)
					tree.append(e)
					if e.get_w() == 0:
						q.appendleft(v)
					else:
						q.append(v)

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

from random import shuffle

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

	# O(V)
	def solve(self):
		whites = []
		blacks = []

		for j in range(0, len(self._matrix[0])):
			if self._matrix[0][j] == GraphSolver.WHITE:
				whites.append(self._vertices[0][j])
			else:
				blacks.append(self._vertices[0][j])
		tree = self._g.breadth_first_search(whites+blacks)

		'''
		Suppose to find the best path between several minimum black cases paths. Doesn't work
		good_edges = []
		bad_edges = []
		for i in range(0, len(self._edges)):
			for j in range(0, len(self._edges[i])):
				for e in self._edges[i][j]:
					if e.get_v().get_d() == e.get_u().get_d() + e.get_w():
						good_edges.append(e)
					else:
						bad_edges.append(e)

		for e in bad_edges:
			self._g.remove_edge(e)
		for e in good_edges:
		 	e.set_w(SimpleGraphSolver.FULL_WEIGHT_EDGE)

		tree = self._g.breadth_first_search(whites+blacks)'''

		v_min = self._vertices[-1][0]
		min_dist = v_min.get_d()
		for v in self._vertices[-1]:
			if v.get_d() < min_dist:
				v_min = v
				min_dist = v.get_d()

		v = v_min
		path = [v.get_id()]
		while v.get_p() != Vertex.NO_PARENT:
			path.append(v.get_p().get_id())
			v = v.get_p()

		path = path[::-1]
		print path
		self._png_tools.generate_png_path(path, self._filename, GraphSolver.PREFIX_FILENAME_SOL + self._filename)

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
	message = 'In matters of truth and justice, there is no difference between large and small problems, for issues concerning the treatment of people are all the same. Albert Einstein'
	filename_qr_code = 'code.png'

	solver = SimpleGraphSolver(message, filename_qr_code)
	solver.init()
	solver.solve()
