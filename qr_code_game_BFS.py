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
		self._vertices.append(v)

	def add_edge(self, u, v, w):
		e = Edge(u, v, w)
		if u not in self._edges:
			self._edges[u] = [e]
		else:
			self._edges[u].append(e)

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


