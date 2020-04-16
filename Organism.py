"""
Organism.py
"""

import struct
import random

################################################################################
class Organism:

    """
    Class attributes:
    bits: the list of bits representing the coefficients of the polynomial
    floats: the corresponding list of floats
    fitness: the fitness value for this organism
    normFit: the normalized fitness value for this organism
    accFit: the accumulated normalized fitness value for this organism
    """

    # Constructor method.
    # numCoeffs: the number of coefficients in the polynomial.
    # bits: (optional) the bit list for this organism.
    def __init__(self, numCoeffs, bits=[]):
        # Check if there was an input bits list.
        if len(bits) > 0:
            # Set our bits list to the input.
            self.bits = bits
        else:
            # Create a list of random bits 0 and 1 of length numCoeffs*64.
            self.bits = [round(random.random()) for x in range(numCoeffs*64)]

        # Calculate the floats list.
        # Note: this will ensure that the number of bits is a multiple of 64.
        self.floats = getFloats(self.bits)
        
        # Set initial fitness to 0 - we will get this value later.
        self.fitness = 0

        # Set the normalized fitness to 0 as well.
        self.normFit = 0
        
        # Set initial accumulated normalized fitness to 0 as well.
        self.accFit = 0

    # The repr method that will print the floats and fitness values.
    def __repr__(self):
        s = 'Polynomial:\n'
        s += str(self.floats[0])
        for n in range(1,len(self.floats)):
            s += '\n+ ' + str(self.floats[n]) + ' x^' + str(n)
        s += '\n\nFitness:\n' + str(self.fitness)
        if self.fitness != 0:
            s += '\n\nAverage Squared Error:\n' + str(1/self.fitness)
        return s

    # The isClone method will return True if the two organisms are the same.
    def isClone(self, other):
        return self.bits == other.bits

    # We will need to sort by the organisms' fitness values.
    # So overload our comparison operators for fitness based comparisons.
    def __lt__(self,other):
        return self.fitness < other.fitness
    def __le__(self,other):
        return self.fitness <= other.fitness
    def __eq__(self,other):
        return self.fitness == other.fitness
    def __ne__(self,other):
        return self.fitness != other.fitness
    def __ge__(self,other):
        return self.fitness >= other.fitness
    def __gt__(self,other):
        return self.fitness > other.fitness

################################################################################

"""
getFloats: this function will take in our binary list and return a corresponding
           list of double precision floats.

INPUTS
binL: the binary list of 0s and 1s, length must be multiple of 64.

OUTPUTS
floatL: the corresponding list of floats of length len(binL)/64.
"""
def getFloats(binL):
    # First, ensure that the input has a proper length.
    if len(binL) % 64 != 0:
        raise ValueError('Binary list length not multiple of 64.')

    # Create the floatL list of proper length.
    floatL = [0.0 for x in range(len(binL)//64)]

    # Now loop over the number of floats: len(binL)//64.
    for n in range(len(binL)//64):
        # Get the next 64 bits, combine them into a string with join, and
        # add a '0b' in front to indicate that they are a bit representation.
        s = '0b' + ''.join(str(x) for x in binL[64*n:64*(n+1)])

        # Now interpret these bits as an int.
        q = int(s, 0)

        # Now we can use the struct package to get a byte representation.
        b8 = struct.pack('Q', q)

        # Finally, we can unpack these bytes to get the floating point value.
        floatL[n] = struct.unpack('d', b8)[0]

    # Return the list of floats.
    return floatL
