#!/usr/bin/env python
"""
Author: Valmor de Almeida dealmeidav@ornl.gov; vfda

Fuel slug 

VFdALib support classes 

Thu Dec 15 16:18:39 EST 2016
"""

#*******************************************************************************
import os, sys
import pandas
from ..phase.interface import Phase
from ._fuelslug     import _FuelSlug      # constructor
from ._getattribute import _GetAttribute  
#*******************************************************************************

#*******************************************************************************
class FuelSlug():

 def __init__( self, 
               specs         = pandas.Series(),
               fuelPhase     = Phase(),
               claddingPhase = Phase()
             ):

  # constructor
  _FuelSlug( self, 
             specs, fuelPhase, claddingPhase )

#*******************************************************************************

#*******************************************************************************
# Setters and Getters methods
#-------------------------------------------------------------------------------
# These are passing arguments by value effectively. Because the python objects
# passed into/out of the function are immutable.

 def GetSpecs(self):
     return self._specs
 specs = property(GetSpecs,None,None,None)

 def GetFuelPhase(self):
     return self._fuelPhase
 fuelPhase = property(GetFuelPhase,None,None,None)

 def GetCladdingPhase(self):
     return self._claddingPhase
 claddingPhase = property(GetCladdingPhase,None,None,None)

 def GetAttribute(self, name, phase=None, symbol=None, series=None):
     return _GetAttribute( self, name, symbol, series )

#*******************************************************************************
# Printing of data members
 def __str__( self ):
     s = 'FuelSlug(): \n\t specs \n\t %s \n\t fuelPhase \n\t %s \n\t claddingPhase \n\t %s'
     return s % (self._specs, self._fuelPhase, self._claddingPhase)

 def __repr__( self ):
     s = 'FuelSlug(): \n\t specs \n\t %s \n\t fuelPhase \n\t %s \n\t claddingPhase \n\t %s'
     return s % (self._specs, self._fuelPhase, self._claddingPhase)
#*******************************************************************************
