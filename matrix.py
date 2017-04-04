"""
# Copyright Cho Yin Yong, 2017
# Distributed under the terms of the GNU General Public License.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

class Matrix:
    """ A representation of a matrix """

    def __init__(self, list_rep):
        """ (Matrix, list) -> NoneType
        Initializes the matrix
        """
        # list to store the matrix information
        self._data = []

        if list_rep != []:
            for row in list_rep:
                self._data.append(row[:])

    def __str__(self):
        """ (Matrix) -> str
        Return the string representation of the Matrix
        """

        rep = ''
        for row in self._data:
            rep += str(row) + '\n'

        return rep.rstrip()

    def copy(self):
        """ (SquareMatrix) -> SquareMatrix
        Return a copy of self
        """
        return SquareMatrix(self._data)

    def get_size(self):
        """ (Matrix) -> tuple of (int, int)
        Return a tuple of the width and height of the matrix.
        """
        width = len(self._data)
        height = len(self._data[0])

        return (width, height)

    def read(self, i, j):
        """ (Matrix, int, int) -> int
        Returns the value in the ith row and jth column
        of the square matrix.
        """
        # reading data will use O(1) in worst case
        return self._data[i - 1][j - 1]

    def read_row(self, i):
        """ (Matrix, int) -> list
        Return a list representation of the row
        """
        return self._data[i - 1][:]

    def remove_row(self, i):
        """ (Matrix, int) -> list
        Remove row ``i`` of the matrix.
        """
        del self._data[i - 1]

    def read_column(self, j):
        """ (Matrix) -> list
        Return a list representation of the column.
        """
        column = []
        for i in range(1, self.get_size()[0] + 1):
            column.append(self.read(i, j))

        return column

    def remove_column(self, j):
        """ (Matrix) -> NoneType
        Remove the ``j``th column of the matrix.
        """

        for column in range(self.get_size()[1]):
            self._data[column] = (self._data[column][:j - 1] +
                                  self._data[column][j:])

    def replace_column(self, j, column_list):
        """ (Matrix, list) -> NoneType
        Replaces the ``i``th row and  ``j``th column
        with the column list.

        REQ: len(column_list) equal to the number
             of rows.
        """
        for i in range(len(column_list)):
            column_value = column_list[i]
            self.write(i + 1, j, column_value)

    def write(self, i, j, x):
        """ (Matrix, int, int, int) -> NoneType
        Replace value in ith row and jth column with
        x.
        """
        # assigning value also uses O(1) in worst case
        self._data[i - 1][j - 1] = x

    def transpose(self):
        """ (Matrix) -> Matrix
        Return the transpose of self.
        """
        transposed_list = []

        # create empty columns based on how many rows
        for i in range(self.get_size()[0]):
            transposed_list.append([])

        for i in range(self.get_size()[0]):
            for j in range(self.get_size()[1]):
                transposed_list[i].append(self.read(j + 1, i + 1))

        return SquareMatrix(transposed_list)

    def scalar_multiply(self, x):
        """ (Matrix) -> NoneType
        Return the matrix after scalar multiplication
        """
        for i in range(1, self.get_size()[0] + 1):
            for j in range(1, self.get_size()[1] + 1):
                self.write(i, j, x * self.read(i, j))


class SquareMatrix(Matrix):
    """ A representation of a square matrix """

    def minor(self, i, j):
        """ (SquareMatrix) -> SquareMatrix
        Return the minor matrix of ``A_ij``
        """
        # make copy of original matrix
        minor_matrix = self.copy()

        # remove ith row and jth column of the minor matrix
        minor_matrix.remove_column(j)
        minor_matrix.remove_row(i)

        # return the minor matrix
        return minor_matrix

    def det(self):
        """ (SquareMatrix) -> int
        Given a square matrix, return its determinant.
        If matrix is empty or 1x1, return None.
        """
        # dummy var for output
        determinant = 0

        # if self is a 2x2 matrix:
        if self.get_size() == (2, 2):
            # use the formula to get determinant
            determinant = (self.read(1, 1) * self.read(2, 2) -
                           self.read(1, 2) * self.read(2, 1))

        # if self is larger than 2x2:
        else:
            # we want to expand along the first row
            for i in range(1, self.get_size()[0] + 1):

                # get the value of A_1i
                a_1i = self.read(1, i)

                # calculate det(minor_matrix if A_1i
                # is not 0
                if a_1i != 0:

                    # get minor matrix's determinant
                    minor = self.minor(1, i)
                    minor_det = minor.det()

                    # add to the determinant
                    determinant += a_1i * (-1)**(1 + i) * minor_det

        return determinant


def dot_product(a, b):
    """ (list of int, list of int) -> float
    Given two list representation of vectors, return its
    dot product.

    REQ: len(a) == len(b)
    """
    product = 0
    for i in range(len(a)):
        product += a[i] * b[i]


def cross_product(a, b):
    """ (list of int, list of int) -> list
    Given two list representation of vectors, return its
    cross product.

    The cross product involves finding the determinant
    of the following matrix:

    | i    j   k |
    | a0  a1  a2 |
    | b0  b1  b2 |
    """
    # create three matrices
    i = SquareMatrix([[a[1], a[2]], [b[1], b[2]]])
    j = SquareMatrix([[a[0], a[2]], [b[0], b[2]]])
    k = SquareMatrix([[a[0], a[1]], [b[0], b[1]]])

    # return its cross product
    return [i.det(), -j.det(), k.det()]


def adjoint(A):
    """ (SquareMatrix) -> SquareMatrix
    Given a square matrix, return the adjoint of the matrix.

    The adjoint is the transpose of the cofactor matrix A.
    """
    # get the size of matrix
    size = A.get_size()[0]

    # adjoint list
    adjoint_list = []

    # special case for 1x1 square matrix
    if size == 1:
        adjoint = A.copy()

    # special case for 2x2 square matrix
    elif size == 2:
        adjoint = SquareMatrix([[A.read(2, 2), -A.read(1, 2)],
                                [-A.read(2, 1), A.read(1, 1)]])

    # general case for 3x3 matrix and above
    else:
        # loop through row and columns
        for i in range(1, size + 1):

            # append an empty row
            adjoint_list.append([])

            for j in range(1, size + 1):

                # calculate the determinant of the minor matrix ij
                minor_det = (-1)**(i + j) * A.minor(i, j).det()

                # put it in the adjoint list
                adjoint_list[i - 1].append(minor_det)

        # take the transpose of the adjoint list
        adjoint = SquareMatrix(adjoint_list).transpose()

    # return the adjoint
    return adjoint


def inverse(A):
    """ (SquareMatrix) -> SquareMatrix
    Return the inverse matrix of A using the determinant and
    adjoint method, with the following formula:

    A^{-1} = 1/{A.det()} * adj(A)

    where * is the scalar multiplication of a matrix.
    """
    # get adjoint of A
    adjoint = adjoint(A)

    # calculate the reciprocal of A.det()
    factor = 1 / A.det()

    return adjoint.scalar_multiply(factor)


def cramer(A, b):
    """ (SquareMatrix, list) -> set of float
    Given a square matrix ``A`` and a vector ``b``, return
    the solutions of Ax = b using the Cramer's rule.

    Returns an empty set if det(A) == 0

    The Cramer's rule is defined as the follow:

    If Ax = b is a system of n linear equations in n unknowns
    and det(A) != 0, then the unique solution is of the form

    x_k = det(B_k) / det(A) for k = 1, 2, ..., n

    det(B_k) is defined as the matrix ``A`` with the column
    ``k`` replaced by b.

    Unfortunately, this algorithm has the complexity
    O(n * n!).
    """
    # dummy set for solutions
    solutions = set()

    # calculate the determinant of A
    a_det = A.det()

    # if the matrix has a unique solution
    if a_det != 0:
        # get the number of columns of A
        num_cols = A.get_size()[1]

        # loop through the number of columns
        for j in range(1, num_cols + 1):

            # make a new copy of A
            B_i = A.copy()

            # replace column to create B_k
            B_i.replace_column(j, b)

            # calculate the solution according to
            # Cramer's rule
            solutions.add(B_i.det() / a_det)

    return solutions


if __name__ == "__main__":
    one = SquareMatrix([[1, 2, 1], [-3, 1, -2], [2, 3, -1]])

    two = SquareMatrix([[1, 3, -2], [0, 1, 5], [-2, -6, 7]])
    print(adjoint(two))
