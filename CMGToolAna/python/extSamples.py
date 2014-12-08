#!/usr/bin/python

import sys
import os
from glob import glob
from sys import exit

from ROOT import gROOT
from ROOT import TFile

# default samples location
locSamp = 'DESY'

def help():
    print 'First argument analysis:'
    print './runreader.py Analyzer TYPE_SAMPLE [Location (%s)]' % locSamp
    print ' TYPE = MC, data'
    print ' SAMPLE = ',

    from DESYsamples import SAMPLES
    print SAMPLES

    sys.exit(0)

def GetNevents(loc):
    EvtFile = open(loc+"ttHLepSkimmer/events.txt", "r")
    theInts = []
    for val in EvtFile.read().split():
        if val.isdigit():
            theInts.append(val)
        EvtFile.close()
    return float(theInts[0])

def GetTreeName(file):
    keylist = file.GetListOfKeys()
    treeKey = keylist.At(0)
    treeName = treeKey.GetName()

    if 'tree' in treeName:
        return treeName
    else:
        print 'Tree not found in ', file.GetName()
        exit(0)

# choose the analysis and a sample
srcdir = '../src/'

if len(sys.argv)>1:
    if sys.argv[1]=='testSamples':
        print 'Testing samples file'

    if sys.argv[1]=='SingleS_P':  # single lepton testing version
        gROOT.LoadMacro(srcdir+'readerSingleS_P.C+')
        from ROOT import readerSingleS_P as reader
    elif sys.argv[1]=='TreeAnalyzer':  # single lepton testing version
        gROOT.LoadMacro(srcdir+'ClassObjects.C+')
        gROOT.LoadMacro(srcdir+'TreeAnalyzer_SingleLep.C+')
        from ROOT import TreeAnalyzer as reader
    elif sys.argv[1]=='TreeAnalyzer_ext':  # test external object definitions
        gROOT.LoadMacro(srcdir+'TreeAnalyzer_ext.C+')
        from ROOT import TreeAnalyzer as reader
    elif sys.argv[1]=='SingleLeptCMSana':  # single lepton CMS artur
        gROOT.LoadMacro(srcdir+'SingleLeptCMSana.C+')
        from ROOT import TreeAnalyzer_ext as reader
    elif sys.argv[1]=='TreeAnalyzer_BKG':  # single lepton testing version
        gROOT.LoadMacro(srcdir+'TreeAnalyzer_BKG.C+')
        from ROOT import TreeAnalyzer_BKG as reader
    elif sys.argv[1]=='TreeOutput':  # test tree output
        gROOT.LoadMacro(srcdir+'ClassObjects.C+')
        gROOT.LoadMacro(srcdir+'TreeOutput.C+')
        from ROOT import TreeWriter as reader
    else:
        help()
else:
    help()

# check sample location in sys.argv
if 'EOS' in sys.argv:
    from EOSsamples import *
else:
    from DESYsamples import *

# fill sample dictionaries
foundFlag=False

# loop over the samples in the arguments
for arg in sys.argv:
    for scene in scenarios:
        for samp in SAMPLES:
            if arg == scene+'_'+samp:
                foundFlag=True
                fileNames=''
                print 'Sample', scene,  samp, inDir[scene][samp]

                # loop over HTbins (if any)
                for i,HT in enumerate(dirsHT[samp]):
                    if len(dirsHT[samp]) > 1:
                        print 'HTbin', HT

                    # Get sample directory
                    sampDir = inDir[scene][samp]+HT
                    # Calculate number of events
                    entries = GetNevents(sampDir)
                    print "cross section x lumi", xsec_lumi[samp][i], "Events generated", entries
                    fileNames=fileNames+inDir[scene][samp]+dirsHT[samp][i]+treename+' '+str(xsec_lumi[samp][i]/entries)+' '
                    print "file name to be processed", fileNames
                    print fileNames,samp,scene
                    reader(fileNames,scene+'_'+samp)

if not foundFlag: help()
