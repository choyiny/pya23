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
        """ (Frac, Frac or int, Frac or int) -> NoneType
        Initializes the Fraction. Reduce the fraction
        to the simplest form.
        """
        # if both are int
        if (isinstance(numerator, int) and
            isinstance(denominator, int)):
            self._num = numerator
            self._denom = denominator

        # at least 1 is frac
        else:
            new_frac = numerator / denominator
            self._num = new_frac.get_num()
            self._denom = new_frac.get_denom()

        # simplify fraction
        if simplify:
            self.simplify()

    def __str__(self):
        """ (Frac) -> str
        Returns str(self)
        """
        if self.get_denom() != 1:
            output = "{}/{}".format(self.get_num(), self.get_denom())
        else:
            output = str(self.get_num())

        return output

    def get_num(self):
        return self._num

    def get_denom(self):
        return self._denom

    def copy(self):
        return Frac(self.get_num(), self.get_denom())

    def rec(self):
        """ (Frac) -> NoneType
        Returns the reciprocal of the fraction.
        """
        return Frac(self.get_denom(), self.get_num())

    def simplify(self):
        """ (Frac) -> NoneType
        Simplifies the fraction
        """
        # calculate gcd
        the_gcd = gcd(self.get_num(), self.get_denom())

        # divide by gcd, keep integer
        self._num = self.get_num() // the_gcd
        self._denom = self.get_denom() // the_gcd


    def __neg__(self):
        """ (Frac or int) -> NoneType
        Returns -self
        """
        return Frac(-self.get_num(), self.get_denom())

    def __eq__(self, other):
        """ (Frac, Frac or int) -> bool
        Returns self == other.
        """
        if isinstance(self, Frac) and isinstance(other, Frac):
            output = ((self.get_num() == other.get_num()) and
                      (self.get_denom() == other.get_denom()))
        else:
            other_frac = Frac(other, 1)
            output = self == other_frac

        return output

    def __mul__(self, value, simplify=True):
        """ (Frac, Frac or int) -> Frac
        Returns self * value
        """
        # if multiply value is int
        if isinstance(value, int):
            num = self.get_num() * value
            denom = self.get_denom()

        # if multiply value is another Frac
        if isinstance(value, Frac):
            num = self.get_num() * value.get_num()
            denom = self.get_denom() * value.get_denom()

        # create new fraction and return
        return Frac(num, denom, simplify)

    def __rmul__(self, value, simplify=True):
        return self.__mul__(value, simplify)

    def __add__(self, value, simplify=True):
        """ (Frac, Frac or int) -> Frac
        Returns self + value
        """
        # if value is int, then make a Frac out of it
        if isinstance(value, int):
            value = Frac(value, 1)

        # find gcd
        the_gcd = gcd(self.get_denom(), value.get_denom())

        # multiply denominator and divide
        # by gcd
        denom = self.get_denom() * value.get_denom() // the_gcd

        # find numerator
        num = (self.get_num() * value.get_denom() // the_gcd +
               value.get_num() * self.get_denom() // the_gcd)

        return Frac(num, denom, simplify)

    def __radd__(self, value, simplify=True):
        """ (Frac, Frac or int) -> Frac
        Returns value + self
        """
        return self + value

    def __sub__(self, value, simplify=True):
        """ (Frac, Frac or int) -> Frac
        Returns self - value
        """
        return self + -value

    def __rsub__(self, value, simplify=True):
        """ (Frac, Frac or int) -> Frac
        Returns value - self
        """
        return -(self + -value)

    def __truediv__(self, value, simplify=True):
        """ (Frac, Frac or int) -> Frac
        Returns self / value
        """
        # case for integer
        if isinstance(value, int):
            output = self.__mul__(Frac(1, value), simplify)

        # case for another Frac
        elif isinstance(value, Frac):
            output = self.__mul__(value.rec(), simplify)

        return output

    def __rtruediv__(self, value, simplify=True):
        """ (Frac, Frac or int) -> Frac
        Returns value / self
        """
        return self.rec() * value
