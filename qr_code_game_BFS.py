from Queue import Queue
from sets import Set

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
		return str(self._id)

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
		return str(self._u) + ' -' + str(self._w) + '-> ' + str(self._v)

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


	def _to_string(self):
		s = ''
		for v in self._vertices:
			s += str(v) + ' -> '
			if v in self._edges:
				for e in self._edges[v]:
					s += str(e) + ' |'

			s = s[:-1] + '\n'
		return s

	def __str__(self):
		return self._to_string()

	def __repr__(self):
		return self._to_string()

if __name__ == "__main__":
	g = SimpleGraph()

