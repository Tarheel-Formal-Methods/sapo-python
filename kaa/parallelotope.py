import numpy as np
from sympy import Matrix, linsolve, EmptySet

from kaa.lputil import minLinProg, maxLinProg

"""
Object encapsulating routines calculating properties of parallelotopes.
"""
class Parallelotope:

    def __init__(self, A, b, vars):
        self.vars = vars
        self.dim = len(vars)

        self.A = A[:self.dim]
        self.b = b

        #print("self.d:   {}".format(self.d))

    """
    Return list of functions transforming the n-unit-box over the parallelotope.
    @params
    """
    def getGeneratorRep(self):

        base_vertex = self._computeBaseVertex()
        gen_list = self._computeGenerators(base_vertex)
        #print("Base Vertex:", base_vertex )
        #print("Gen Vertex: ", gen_list)


        expr_list = base_vertex
        for var_ind, var in enumerate(self.vars):
            for i in range(self.dim):
                expr_list[i] += gen_list[var_ind][i] * var
        #print("Expr List:" , expr_list)
        return expr_list
    
    """
    Calculate generators as substraction: vertices - base_vertex.
    We calculate the vertices by solving the following linear system for each vertex i:


    Ax = [b_1, ... , -b_{i+n}, ... , b_n]^T

    Note that this simply finds the vertex to calculate the generator vectors.
    The parallelotope will be exprssed as sum of the base vertex and the convex combination of the generators.

   p(a_1, ... ,a_n) =  q + \sum_{j} a_j * g_j

    where q is the base vertex and the g_j are the generators. a_j will be in the unitbox [0,1]

    @params base_vertex: base vertex
    """
    def _computeGenerators(self, base_vertex):

        upper_b = self.b[:self.dim]

        vertices = []
        coeff_mat = self._convertMatFormat(self.A)

        for i in range(self.dim):
            negated_bi = np.copy(upper_b)
            negated_bi[i] = -self.b[i + self.dim]
            negated_bi = self._convertMatFormat(negated_bi)
            
            sol_set_i = linsolve((coeff_mat, negated_bi), self.vars)
            vertex_i = self._convertSolSetToList(sol_set_i)
            vertices.append(vertex_i)

        #print("Vertices:", vertices)
        return [ [x-y for x,y in zip(vertices[i], base_vertex)] for i in range(self.dim) ]
       

    """
    Calculate the base vertex of the parallelotope (variable q)
    We calculate the vertices by solving a linear system of the following form:

    Ax = u_b

    where u_b are the offsets for the upper facets of parallelotope (first half of self.b).
    """
    def _computeBaseVertex(self):

        upper_b = self.b[:self.dim]

        coeff_mat = self._convertMatFormat(self.A)
        offset_mat = self._convertMatFormat(upper_b)

        sol_set = linsolve((coeff_mat, offset_mat), self.vars)
        return self._convertSolSetToList(sol_set)

    """
    Convert numpy matrix into sympy matrix
    @params mat: numpy matrix
    """
    def _convertMatFormat(self, mat):
        return Matrix(mat.tolist())
    
    """
    Takes solution set returned by sympy and converts into list
    @params fin_set: FiniteSet
    """
    def _convertSolSetToList(self, fin_set):
 ,
        assert fin_set is not EmptySet

        return list(fin_set.args[0])
