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

# helper function for gcd
def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x


class Frac:
    """ A class representing a fraction """

    def __init__(self, numerator, denominator, simplify=True):
        """ (Frac, int, int) -> NoneType
        Initializes the Fraction. Reduce the fraction
        to the simplest form.
        """
        # store numerator and denominator
        self._num = numerator
        self._denom = denominator

        # simplify fraction
        if simplify:
            self.simplify()

    def __str__(self):
        """ (Frac) -> str
        Returns str(self)
        """
        return "{} / {}".format(self._num, self._denom)

    def rec(self):
        """ (Frac) -> NoneType
        Returns the reciprocal of the fraction.
        """
        return Frac(self._denom, self._num)

    def simplify(self):
        """ (Frac) -> NoneType
        Simplifies the fraction
        """
        # calculate gcd
        gcd = gcd(_num, _denom)

        # divide by gcd, keep integer
        self._num = self._num // gcd
        self._denom = self._denom // gcd


    def neg(self):
        """ (Frac or int) -> NoneType
        Makes fraction or int negative.
        """
        self._num = -self._num

    def __eq__(self, other):
        """ (Frac) -> bool
        Returns self == other.
        """
        return ((self._num == other.num) and
                (self._denom == other._denom))

    def __rmul__(self, value, simplify=True):
        """ (Frac, Frac or int) -> NoneType
        Returns self * value
        """
        # if multiply value is int
        if isinstance(value, int):
            num = self._num * value
            denom = self._denom

        # if multiply value is another Frac
        if isinstance(value, Frac):
            num = self._num * value._num
            denom = self._denom * value._denom

        # create new fraction and return
        return Frac(num, denom, simplify)

    def __radd__(self, value, simplify=True):
        """ (Frac, Frac or int) -> NoneType
        Returns self + value
        """
        # if value is int, then make a Frac out of it
        if isinstance(value, int):
            value = Frac(value, 1)

        # multiply denominator
        denom = self._denom * value._denom

        # find numerator
        num = (self._num * value._denom +
                     value._num * self._denom)

        return Frac(num, denom, simplify)

    def __rsub__(self, value, simplify=True):
        """ (Frac, Frac or int) -> NoneType
        Returns self - value
        """
        self.__radd__(value.neg(), simplify)

    def __div__(self, value, simplify=True):
        """ (Frac, Frac or int) -> NoneType
        Returns self / value
        """
        # case for integer
        if isinstance(value, int):
            self.__rmul__(Frac(1, value), simplify)

        # case for another Frac
        elif isinstance(value, Frac):
            self.__rmul__(value.rec(), simplify)
