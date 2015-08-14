"""
Valmor F. de Almeida dealmeidav@ornl.gov; vfda

Pyplot module.

Tue Jun 24 01:03:45 EDT 2014
"""
#*********************************************************************************
import os, sys, io, time, datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator
#*********************************************************************************

#---------------------------------------------------------------------------------
# All time sequences on hold will be plotted here and the temporary storage of
# these time sequences will be cleared at the end.

def _PlotTimeSeqDashboard( self, initialTime=0.0, finalTime=0.0 ):

  nSequences = len(self.timeSequences_tmp)
  if nSequences == 0: return

  s = '_PlotTimeSeqDashboard(): from: '+str(initialTime)+' to '+str(finalTime)
  self.log.debug(s)

  s = '_PlotTimeSeqDashboard(): # of sequences: '+str(nSequences)
  self.log.debug(s)

  nVar = 0
  for seq in self.timeSequences_tmp:
    nVar += seq.GetNVariables()

  s = '_PlotTimeSeqDashboard(): # of variables: '+str(nVar)
  self.log.debug(s)

  # multiple sequences are stored coming from various sources
  # collect all variables in a list for mapping on the dashboards
  variablesData = list()
  for seq in self.timeSequences_tmp:
    for (spec,values) in seq.GetVariables().items():
      variablesData.append( (spec,values) )
  assert len(variablesData) == nVar

  today = datetime.datetime.today().strftime("%d%b%y %H:%M:%S")
  
  # loop over variables and assign to the dashboards  
  iDash = 0
  for iVar in range(nVar):

    if iVar % 9 == 0: # if a multiple of 8 start a new dashboard

      if iVar != 0: # flush any current figure
        figName = 'pyplot_'+str(self.slotId)+'-timeseq-dashboard-'+str(iDash)+'.png'
        fig.savefig(figName,dpi=200,fomat='png')
        plt.close(str(self.slotId)+'_'+str(iDash))
        s = '_PlotTimeSeqDashboard(): created plot: '+figName
        self.log.debug(s)
        iDash += 1
      # end of: if iVar != 0: # flush any current figure

      fig = plt.figure(str(self.slotId)+'_'+str(iDash))

      gs = gridspec.GridSpec(3,3)
      gs.update( left=0.08,right=0.98,wspace=0.4,hspace=0.4 )

      axlst = list()

      nPlotsNeeded = nVar - iVar 
      count = 0
      for i in range(3):
        for j in range(3):
          axlst.append( fig.add_subplot(gs[i, j]) )
          count += 1
          if count == nPlotsNeeded: break
        if count == nPlotsNeeded: break

      axes = np.array(axlst)

      text = today+': cortix.viz.PyPlot_'+str(self.slotId)+': Time-Sequence Dashboard'
      fig.text(.5,.95,text,horizontalalignment='center',fontsize=14)

      axs = axes.flat
 
      axId = 0

    # end of: if iVar % 9 == 0: # if a multiple of 9 start a new dashboard

    (spec,val) = variablesData[iVar]

    ax = axs[axId]
    axId += 1
 
    varName = spec[0]
    varUnit = spec[1]

    if varUnit == 'gram': varUnit = 'g'
    if varUnit == 'gram/min': varUnit = 'g/min'

    timeUnit  = spec[2]
    varLegend = spec[3]
    varScale  = spec[4]
    assert varScale == 'log' or varScale == 'linear' or varScale == 'log-linear' \
           or varScale == 'linear-log' or varScale == 'linear-linear' or \
           varScale == 'log-log'

    if timeUnit == 'minute': timeUnit = 'min'
 
    data = np.array(val)

#      assert len(data.shape) == 2, 'not a 2-column shape: %r in var %r of %r; stop.' % (data.shape,varName,varLegend)
    if len(data.shape) != 2: 
      s = '_PlotTimeSeqDashboard(): bad data; variable: '+varName+' unit: '+varUnit+' legend: '+varLegend+' shape: '+str(data.shape)+' skipping...'
      self.log.warn(s)
      continue #  simply skip bad data and log

    x = data[:,0]
    if varScale == 'linear' or varScale == 'linear-linear' or \
       varScale == 'linear-log' and x.max() >= 120.0:
       x /= 60.0
       if timeUnit == 'min': timeUnit = 'h'

    y = data[:,1]

    if y.max() >= 1000.0 and varScale != 'linear-log' and \
                  varScale != 'log-log' and varScale != 'log': 
      y /= 1000.0
      if varUnit == 'gram' or varUnit == 'g': varUnit = 'kg'
      if varUnit == 'cc': varUnit = 'L'
      if varUnit == 'Ci': varUnit = 'kCi'
      if varUnit == 'W': varUnit = 'kW'
      if varUnit == 'gram/min' or varUnit == 'g/min': varUnit = 'kg/min'
      if varUnit == '': varUnit = 'x1e3'

    if y.max() <= .001 and varScale != 'linear-log' and \
                  varScale != 'log-log' and varScale != 'log': 
      y *= 1000000.0
      if varUnit == 'gram' or varUnit == 'g': varUnit = 'ug'
      if varUnit == 'cc': varUnit = 'u-cc'
      if varUnit == 'gram/min' or varUnit == 'g/min': varUnit = 'ug/min'

    if y.max() <= .1 and varScale != 'linear-log' and \
                  varScale != 'log-log' and varScale != 'log': 
      y *= 1000.0
      if varUnit == 'gram' or varUnit == 'g': varUnit = 'mg'
      if varUnit == 'cc': varUnit = 'm-cc'
      if varUnit == 'gram/min' or varUnit == 'g/min': varUnit = 'mg/min'
  
    ax.set_xlabel('Time ['+timeUnit+']',fontsize=9)
    ax.set_ylabel(varName+' ['+varUnit+']',fontsize=9)

    ymax  = y.max()
    dy    = ymax * .1
    ymax += dy
    ymin  = y.min()
    ymin -= dy

    if abs(ymin-ymax) <= 1.e-4:
      ymin = -1.0
      ymax =  1.0

    ax.set_ylim( ymin, ymax )

    for l in ax.get_xticklabels(): l.set_fontsize(10)
    for l in ax.get_yticklabels(): l.set_fontsize(10)

    if timeUnit == 'h' and x.max()-x.min() <= 5.0:
      majorLocator = MultipleLocator(1.0)
      minorLocator = MultipleLocator(0.5)

      ax.xaxis.set_major_locator(majorLocator)
      ax.xaxis.set_minor_locator(minorLocator)

    if varScale == 'log' or varScale == 'log-log':
      ax.set_xscale('log')
      ax.set_yscale('log')
      positiveX = x > 0.0
      x = np.extract(positiveX, x)
      y = np.extract(positiveX, y)
      positiveY = y > 0.0
      x = np.extract(positiveY, x)
      y = np.extract(positiveY, y)
      if y.size > 0:
        if y.min() > 0.0 and y.max() > y.min(): 
          ymax  = y.max()
          dy    = ymax * .1
          ymax += dy
          ymin  = y.min()
          ymin -= dy
          if ymin < 0.0 or ymin > ymax/1000.0: ymin = ymax/1000.0
          ax.set_ylim( ymin, ymax )
        else:       
          ax.set_ylim( 1.0 , 10.0 )
      else: 
        ax.set_ylim( 1.0, 10.0 )

    if varScale == 'log-linear':
      ax.set_xscale('log')
      positiveX = x > 0.0
      x = np.extract(positiveX, x)
      y = np.extract(positiveX, y)

    if varScale == 'linear-log':
      ax.set_yscale('log')
      positiveY = y > 0.0
      x = np.extract( positiveY, x )
      y = np.extract( positiveY, y )
#      assert x.size == y.size, 'size error; stop.'
      if y.size > 0:
        if y.min() > 0.0 and y.max() > y.min(): 
          ymax  = y.max()
          dy    = ymax * .1
          ymax += dy
          ymin  = y.min()
          ymin -= dy
          if ymin < 0.0 or ymin > ymax/1000.0: ymin = ymax/1000.0
          ax.set_ylim( y.min(), ymax )
        else:                                   
          ax.set_ylim( 1.0, 10.0 )
      else: 
        ax.set_ylim( 1.0, 10.0 )

    #...................
    # make the plot here

    ax.plot( x, y, 's-', color='black', linewidth=0.5, markersize=2,  \
             markeredgecolor='black', label=varLegend )

    #...................

    ax.legend( loc='best', prop={'size':7} )

    s = '_PlotTimeSeqDashboard(): plotted '+varName+' from '+varLegend
    self.log.debug(s)

  # end of: for iVar in range(nVar):

  figName = 'pyplot_'+str(self.slotId)+'-timeseq-dashboard-'+str(iDash)+'.png'
  fig.savefig(figName,dpi=200,fomat='png')
  plt.close(str(self.slotId)+'_'+str(iDash))
  s = '_PlotTimeSeqDashboard(): created plot: '+figName
  self.log.debug(s)

  s = '_PlotTimeSeqDashboard(): done with plotting'
  self.log.debug(s)

  # clear timeSequences_tmp
  self.timeSequences_tmp = list()


  return

#*********************************************************************************
