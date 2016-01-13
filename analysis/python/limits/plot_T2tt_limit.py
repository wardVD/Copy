import ROOT

import sys, ctypes

from StopsDilepton.tools.helpers import getObjFromFile
#from StopsDilepton.tools.tdrStyle import tdrStyle
#tdrStyle(padRightMargin=0.15)
from StopsDilepton.tools.interpolate import interpolate, rebin
from StopsDilepton.tools.niceColorPalette import niceColorPalette

ifile = '/afs/hephy.at/data/rschoefbeck01/StopsDilepton/results/test/isOS-nJets2p-nbtag1p-met80-metSig5-dPhiJet0-dPhiJet-mll20/limits/T2tt.root'

T2tt_obs        = getObjFromFile(ifile, "T2tt_exp").Clone('T2tt_obs') #FIXME!!! This is just for now...
T2tt_exp        = getObjFromFile(ifile, "T2tt_exp")
T2tt_exp_up     = getObjFromFile(ifile, "T2tt_exp_up")
T2tt_exp_down   = getObjFromFile(ifile, "T2tt_exp_down")

T2tt_obs_smooth = interpolate(T2tt_obs)
T2tt_exp_smooth = interpolate(T2tt_exp)
T2tt_exp_up_smooth = interpolate(T2tt_exp_up)
T2tt_exp_down_smooth = interpolate(T2tt_exp_down)
for i in range(1):
  T2tt_obs_smooth = interpolate(T2tt_obs_smooth)
  T2tt_exp_smooth = rebin(T2tt_exp_smooth)
  T2tt_exp_up_smooth = rebin(T2tt_exp_up_smooth)
  T2tt_exp_down_smooth = rebin(T2tt_exp_down_smooth)
T2tt_obs_smooth.SetName("T2tt_obs_smooth")
T2tt_exp_smooth.SetName("T2tt_exp_smooth")
T2tt_exp_up_smooth.SetName("T2tt_exp_up_smooth")
T2tt_exp_down_smooth.SetName("T2tt_exp_down_smooth")

#theory uncertainty on observed limit
from StopsDilepton.tools.xSecSusy import xSecSusy
xSecSusy_ = xSecSusy()
T2tt_obs_up_smooth   = T2tt_obs_smooth.Clone("T2tt_obs_up_smooth") 
T2tt_obs_down_smooth = T2tt_obs_smooth.Clone("T2tt_obs_down_smooth") 
T2tt_obs_up_smooth  .Reset() 
T2tt_obs_down_smooth.Reset() 
x, y, z = [ROOT.Long() for x in range(3)]
for ix in range(T2tt_obs_smooth.GetNbinsX()):
  for iy in range(T2tt_obs_smooth.GetNbinsY()):
    mStop = T2tt_obs_smooth.GetXaxis().GetBinLowEdge(ix)
    mNeu  = T2tt_obs_smooth.GetYaxis().GetBinLowEdge(iy)
    v = T2tt_obs_smooth.GetBinContent(T2tt_obs_smooth.FindBin(mStop, mNeu))
    if v>0:
      scaleup = xSecSusy_.getXSec(channel='stop13TeV',mass=mStop,sigma=1)/xSecSusy_.getXSec(channel='stop13TeV',mass=mStop,sigma=0) 
      scaledown = xSecSusy_.getXSec(channel='stop13TeV',mass=mStop,sigma=-1)/xSecSusy_.getXSec(channel='stop13TeV',mass=mStop,sigma=0) 
      T2tt_obs_up_smooth.SetBinContent(T2tt_obs_smooth.FindBin(mStop, mNeu), v*scaleup) 
      T2tt_obs_down_smooth.SetBinContent(T2tt_obs_smooth.FindBin(mStop, mNeu), v*scaledown) 

def getContours(h):
  _h = h.Clone()
  contlist = [0.5,1.0,1.5]
  idx = contlist.index(1.0)
  c_contlist = ((ctypes.c_double)*(len(contlist)))(*contlist)
  ctmp = ROOT.TCanvas()
  _h.SetContour(len(contlist),c_contlist)
  _h.Draw("contzlist")
  ctmp.Update()
  contours = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
  graph_list = contours.At(idx)
  contours = []
  np = 0
  idx_graph = 0
  for i in range(graph_list.GetEntries()):
      contours.append( graph_list.At(i).Clone("cont_"+str(i)) )
      if contours[i].GetN()>np:
          np=contours[i].GetN()
          idx_graph = i
  del ctmp
  return contours

ROOT.gStyle.SetPadRightMargin(0.15)
c1 = ROOT.TCanvas()
niceColorPalette(255)

contours_exp      = getContours(T2tt_exp_smooth)
contours_exp_up   = getContours(T2tt_exp_up_smooth)
contours_exp_down = getContours(T2tt_exp_down_smooth)
contours_obs      = getContours(T2tt_obs_smooth)
contours_obs_up   = getContours(T2tt_obs_up_smooth)
contours_obs_down = getContours(T2tt_obs_down_smooth)

contour_exp      = contours_exp[2]     .Clone("contour_exp")   
contour_exp_up   = contours_exp_up[2]  .Clone("contour_exp_up")
contour_exp_down = contours_exp_down[2].Clone("contour_exp_down")
contour_obs      = contours_obs[2]     .Clone("contour_obs")
contour_obs_up   = contours_obs_up[2]  .Clone("contour_obs_up")
contour_obs_down = contours_obs_down[2].Clone("contour_obs_down")

T2tt_obs_smooth.GetZaxis().SetRangeUser(0.2, 99)
T2tt_obs.Draw('COLZ')
c1.SetLogz()

def cleanContour(g):
  x, y = ROOT.Double(), ROOT.Double()
  remove=[]
  for i in range(g.GetN()):
    g.GetPoint(i, x, y)
    if  x>600 or (x<410) or y>250:
      remove.append(i)
  for i in reversed(remove):
    g.RemovePoint(i)
  
cleanContour(contour_exp)
cleanContour(contour_exp_up)
cleanContour(contour_exp_down)
cleanContour(contour_obs)
cleanContour(contour_obs_up)
cleanContour(contour_obs_down)

for g in [contour_exp, contour_exp_up, contour_exp_down, contour_obs_up, contour_obs_down]:
  g.Draw('same')

ofileName = '/afs/hephy.at/user/r/rschoefbeck/www/etc/T2tt'
c1.Print(ofileName+'.png')
from StopsDilepton.PlotsSMS.inputFile import inputFile
from StopsDilepton.PlotsSMS.smsPlotXSEC import smsPlotXSEC
from StopsDilepton.PlotsSMS.smsPlotCONT import smsPlotCONT
from StopsDilepton.PlotsSMS.smsPlotBrazil import smsPlotBrazil

tempFileName = "tmp.root"
temp = ROOT.TFile(tempFileName,"recreate")
T2tt_obs_smooth.Write()
contour_exp.Write()
contour_exp_up.Write()
contour_exp_down.Write()
contour_obs.Write()
contour_obs_up.Write()
contour_obs_down.Write()
temp.Close()

# read input arguments
modelname = "T2tt" 
analysisLabel = "SUS-16-NaN" 
outputname = ofileName 

# read the config file
fileIN = inputFile('T2tt_limit.cfg')

# classic temperature histogra
xsecPlot = smsPlotXSEC(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "")
xsecPlot.Draw()
xsecPlot.Save("%sXSEC" %outputname)

# only lines
contPlot = smsPlotCONT(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "")
contPlot.Draw()
contPlot.Save("%sCONT" %outputname)

# brazilian flag (show only 1 sigma)
brazilPlot = smsPlotBrazil(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "")
brazilPlot.Draw()
brazilPlot.Save("%sBAND" %outputname)

