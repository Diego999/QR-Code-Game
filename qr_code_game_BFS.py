from graph_tool.all import *

from graphsolver import GraphSolver

class GraphSolverBFS(GraphSolver):

	EMPTY_WEIGHT_EDGE = 0
	FULL_WEIGHT_EDGE = 1

	def __init__(self, message, filename):
		super(GraphSolverBFS, self).__init__(message, filename)

	def init(self):
		super(GraphSolverBFS, self).init(GraphSolverBFS.EMPTY_WEIGHT_EDGE, GraphSolverBFS.FULL_WEIGHT_EDGE)

	def solve(self):
		pass
		


if __name__ == "__main__":
	message = 'In matters of truth and justice, there is no difference between large and small problems, for issues concerning the treatment of people are all the same. Albert Einstein'
	filename_qr_code = 'code.png'

	solver = GraphSolverBFS(message, filename_qr_code)
	solver.init()
	solver.solve()
	#solver.draw_graph()
