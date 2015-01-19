from graph_tool.all import *

from graphsolver import GraphSolver

class GraphSolverDijkstra(GraphSolver):

	EMPTY_WEIGHT_EDGE = 0.0000001 # With this weight, we minimize also the number of EMPTY cases
	FULL_WEIGHT_EDGE = 1

	def __init__(self, message, filename):
		super(GraphSolverDijkstra, self).__init__(message, filename)

	def init(self):
		super(GraphSolverDijkstra, self).init(GraphSolverDijkstra.EMPTY_WEIGHT_EDGE, GraphSolverDijkstra.FULL_WEIGHT_EDGE)

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
				if self._matrix[r][c] == GraphSolverDijkstra.BLACK: 
					current_dist += GraphSolverDijkstra.FULL_WEIGHT_EDGE

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


if __name__ == "__main__":
	message = 'In matters of truth and justice, there is no difference between large and small problems, for issues concerning the treatment of people are all the same. Albert Einstein'
	filename_qr_code = 'code.png'

	solver = GraphSolverDijkstra(message, filename_qr_code)
	solver.init()
	solver.solve()
	#solver.draw_graph()
