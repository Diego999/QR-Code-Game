from Queue import Queue

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

	v = []
	for i in range(0, 9):
		v.append(g.add_vertex(i))

	g.add_edge(v[0], v[1], 22)
	g.add_edge(v[0], v[3], 11)
	g.add_edge(v[2], v[1], 55)
	g.add_edge(v[4], v[2], 44)
	g.add_edge(v[1], v[4], 33)
	g.add_edge(v[3], v[4], 88)
	g.add_edge(v[5], v[3], 66)

	g.add_edge(v[3], v[6], 77)
	g.add_edge(v[6], v[5], 99)
	g.add_edge(v[6], v[8], 1010)
	g.add_edge(v[6], v[7], 1212)
	g.add_edge(v[7], v[6], 1111)
	g.add_edge(v[8], v[7], 13)
	

	g.breadth_first_search(v[0])
