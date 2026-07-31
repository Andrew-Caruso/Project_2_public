import matplotlib.pyplot as plt
import scienceplots 
import numpy as np 
#import pandas as pd 
from scipy.interpolate import make_interp_spline as interp  
import os
#https://pypi.org/project/SciencePlots/#description 
#all plot styles see:
#https://github.com/garrettj403/SciencePlots/wiki/Gallery 
#to remove ticks
#https://www.geeksforgeeks.org/python/how-to-remove-ticks-from-matplotlib-plots/ 


#------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
    #functions 
#-------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------

def loadin(x):
    #input x is name of plot data
    #assumes CSV file type 
    tempDir = currentDir+"/finalPlotData/"+x
    temptempData = np.genfromtxt(tempDir,delimiter='"',dtype=None) #import data file, handling any data type
    bob=np.asarray(temptempData) #convert to numpy array
    tempData=bob[(bob!='False')&(bob!=',')] #remove all false and comma elements
    #NOTE: all values are strings in numpy array
    #likewise the imported csv mathematica code must contain only strings
    #but can convert mathematica list {} to python list [] via 
    #ExportString[{1, 2, 3, 4, 5}, "PythonExpression"] when exporting the data in mathematica 
    return tempData 

def loadin2(x):
    #input x is name of SK theory data 
    #assumes CSV file type
    tempDir2 = currentDir+"/abe2025_SK/"+x
    tempTempData2=np.genfromtxt(tempDir2,delimiter=',',dtype=None) #import data file handling any data type
    tempData2=np.asarray(tempTempData2) #convert to numpy array
    return tempData2

def loadin3(x):
    #input x is name of Kresse theory data 
    #assumes CSV file type
    tempDir3 = currentDir+"/kresse2021_DSNB/"+x
    tempTempData3=np.genfromtxt(tempDir3,delimiter=',',dtype=None) #import data file handling any data type
    tempData3=np.asarray(tempTempData3) #convert to numpy array
    return tempData3

def printer(inArray):
    n=0
    for x in inArray:
        print("index: ",n," type: ",type(x),"value: ",x ,"\n")
        n+=1

def strToArray(x): 
    #assumes input is a string: "[1,2,3,4,...]"
    #i.e. 1D list
    xStrip = x.replace('[','').replace(']','') #remove all instanes of "[" at front or at beginning "]"
    xSep=xStrip.split(",")#split the str based on commas 
    xStrArray=np.asarray(xSep)#convert to numpy array 
    xOut=xStrArray.astype(float) #convert all str elements to float
    return xOut

def strToList(x):
    #assumes input is a string: "[1,2,3,4,...]"
    #i.e. 1D list
    xStrip = x.replace('[','').replace(']','') #remove all instanes of "[" at front or at beginning "]"
    xSep=xStrip.split(",")#split the str based on commas 
    xOut=[float(i) for i in xSep] #convert all str elements to float
    return xOut


def specs(x):
    #assume x is a numpy array 
    blank = " "
    spacing=blank*5
    print("shape (row x column): ",x.shape)
    print("size (elements): ",x.size)
    print("dims (columns): ",x.ndim)
    print("length (rows): ",len(x))
    return 0



def strToArray2(x): 
    #assumes input is a string: "[[1,2],[3,4],...]"
    #2D pairwise list 
    xStrip = x.replace('[','').replace(']','') #remove all instanes of "[" at front or at beginning "]"
    xSep=xStrip.split(",")#split the str based on commas 
    xStrArray=np.asarray(xSep)#convert to numpy array 
    xOutJR=xStrArray.astype(float) #convert all str elements to float
    xOut=xOutJR.reshape(int(xOutJR.size/2),2) #reshape 1D to 2D array
    return xOut 

def strToArray3(inArray):
    #assumes input is a string: "[[1,2,],[3,4,5],...]"
    #create empty list to fill 
    outList=[]
    #convert each component and add to array
    for x in inArray:
        #print(x," ",type(x))
        #print(strToList(x),type(strToList(x)))
        #append sublist to list
        outList.append(strToList(x))
    #convert list of sublists to numpy array 
    outArray=np.asarray(outList) #convert list to numpy array
    return outArray 




def dsnbFluxPlotter(x,y,z,name):
    #take in raw data x (for no MSW, IH, or NH)
    #take in title y 
    #take in chosenfontsize z 
    #create figure for DSNB flux plot for each case 
    tempFig, tempAx= plt.subplots(nrows=1,ncols=1,tight_layout=True)#create figure 
    #chose size of figure
    tempFig.set_figheight(1.2)
    tempFig.set_figwidth(1.7)
    #chose font size is input as z
    #get all dsnb flux data
    tempSFRmax=strToArray2(x[1])
    tempSFRmin=strToArray2(x[3])
    tempFiducial=strToArray2(x[5])
    tempMax=strToArray2(x[7])
    tempMin=strToArray2(x[9])
    #plot no MSW plot data
    tempAx.semilogy(tempFiducial[:,0],tempFiducial[:,1],label='Fiducial',color='black',linestyle='solid',linewidth=1)
    tempAx.semilogy(tempSFRmin[:,0],tempSFRmin[:,1],label='with SFR uncertainty',color='tab:blue',linestyle='solid')
    tempAx.semilogy(tempSFRmax[:,0],tempSFRmax[:,1],color='tab:blue',linestyle='solid')
    tempAx.semilogy(tempMin[:,0],tempMin[:,1],label='without SFR uncertainty',color='tab:green',linestyle='dashed')
    tempAx.semilogy(tempMax[:,0],tempMax[:,1],color='tab:green',linestyle='dashed')
    #plot fillings outer 
    tempAx.fill_between(tempSFRmin[:,0],tempMax[:,1],tempSFRmax[:,1],color='tab:blue',alpha=0.3)
    tempAx.fill_between(tempSFRmin[:,0],tempSFRmin[:,1],tempMin[:,1],color='tab:blue',alpha=0.3)
    #plot fillings inner 
    tempAx.fill_between(tempSFRmin[:,0],tempMin[:,1],tempFiducial[:,1],color='tab:green',alpha=0.3)
    tempAx.fill_between(tempSFRmin[:,0],tempFiducial[:,1],tempMax[:,1],color='tab:green',alpha=0.3)
    #adjust axes
    tempAx.set_xlabel(r"$\text{E}_{\nu} \text{(MeV)}$",fontsize=z,labelpad=2)
    tempAx.set_ylabel(r"$\frac{d\phi}{dE} (\text{MeV}^{-1}\text{cm}^{-2}\text{s}^{-1}$)",fontsize=z,labelpad=2)
    tempAx.set_title(y,fontsize=z)
    tempAx.set_xlim(1,35)
    tempAx.set_ylim(0.2,30)
    tempAx.tick_params(axis='both',which='major',labelsize=z)
    tempAx.set_axisbelow(False) #force ticks to be above curves 
    tempFig.tight_layout(pad=0.1)
    tempAx.legend(loc='upper left',prop={'size':3},bbox_to_anchor=(0.56,0.9))
    #export figure
    #tempFig.savefig(name+".pdf")
    #save directly from shown plot
    #DO NOT use savefig since it does not coincide directly 
    return 0

def strToArray4(x):
    #take in a string in format of "[[[xErrorMin,xErrorMax],yValue]...]"
    #and convert to numpy array such that it is 
    #formated as [[xErrMins,...],[xErrMaxs,...],[yValues,...]]
    #i.e. each column is xErrMin, xErrMax, or yValue
    tempbounds=np.array(strToList(x))
    #reshape into 3 columns: xErrMin, XErrMax, yValue 
    #i.e. as [[[xErrMin,xErrMax, yValue]]...] 
    boundsJR = tempbounds.reshape(-1,3)
    #tranpose (swap rows and columns)
    #i.e. [[xErrMins,...],[xErrMaxs,...],[yValues,...]] 
    bounds=boundsJR.T
    return bounds 


def averager(x):
    #assumes x is two lists
    #[[mins,..],[max,...]]
    #get avereage for pairs of elements
    xValout= [(float(x[1][i]+x[0][i])/2) for i in range(0,len(x[1]))]
    return xValout



#------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
    #body 
#-------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------

#get current working directory
currentDir = os.getcwd() 
#print(currentDir) 
#chose publisher plot style 
plt.style.use(['science','ieee']) 

#objective:
'''
take in mathematica plot data and re-create plots alla python scienceplots
'''
#choose which code to execute 
#0 = 1P and 2P criterion plot
#1 = DSNB flux plots (no MSW, IH, NH)
#2 = integrated DSNB flux plots (with SK bound)
#3 = DSNB flux finale (with SK bounds)
#4 = dSNB flux finale (with theory bounds)
#5 = binned DSNB flux finale (with SK bounds)

plotBool=2

#remove bottom and top axes
#plt.rcParams['axes.spines.top'] = False
#plt.rcParams['axes.spines.right'] = False
#plt.rcParams['xtick.top'] = False
#plt.rcParams['ytick.right'] = False


#------------------------------------------------------------------
    #1P and 2P criterion plot 
#------------------------------------------------------------------
if plotBool==0:
    print("creating 1P and 2P criterion plot")
    #for 1P plot data 
    #import 1P histogram plot data 
    rawHist1Pdata=loadin("hist1Pdata.csv")
    #printer(rawHist1Pdata)
    #formated as NS at 1, BH at 3, 1P value at 5, and 1P success faction at 7
    #with indicators prior to each index
        #convert and extract plot data
        #formated as [x1, x2, x3,...]
    hist1PNS=strToArray(rawHist1Pdata[1])
    hist1PBH=strToArray(rawHist1Pdata[3])
    successFrac1P=rawHist1Pdata[7]
        #get counts and bins
    count1pNS, bins1pNS=np.histogram(hist1PNS)
    count1pBH, bins1pBH=np.histogram(hist1PBH)
        #get 1P criterion
    criterion1P=float(rawHist1Pdata[5])
    #round the value
    critVal1P=str(round(float(rawHist1Pdata[5]),2))


    #for 2P plot data
    #import 2P plot data 
    rawPlot2Pdata=loadin("plot2Pdata.csv")
    #printer(rawPlot2Pdata)
    #formated as BH at 1, NS at 3, BH outliers at 5, NS outliers at 7, 2P criterion points at 9
    #2P crit func str at 11, and success fraction at 13
    #with indicators prior to each index
    successFrac2P=rawPlot2Pdata[13]
        #convert and extract plot data (including outliers and 2P criterion end points)
        #in to convert from strings
        #formated as [[x1,y1],[x2,y2],...]
    plot2PBH=strToArray2(rawPlot2Pdata[1])
    plot2PNS=strToArray2(rawPlot2Pdata[3])
    plot2PBHoutliers=strToArray2(rawPlot2Pdata[5])
    plot2PNSoutliers=strToArray2(rawPlot2Pdata[7])
    plot2PcritPoints=strToArray2(rawPlot2Pdata[9])
        #get string version of 2P func
    plot2Pcriterion=rawPlot2Pdata[11]
    #print(rawPlot2Pdata[1])
    #print(plot2PBH[:,0]) #x values only 
    critVal2P=rawPlot2Pdata[11]
    slope2P=critVal2P[12:15]
    interY2P=critVal2P[25:-4]

    #print success fractions
    print("\n","success fractions:")
    print("1P criterion: ",successFrac1P)
    print("2P criterion: ",successFrac2P)
    print("\n","criteria:")
    print("1P criterion: ",r"\mu_4=",rawHist1Pdata[5])
    print("rounded 1P criterion: ",r"\mu_4=",critVal1P)
    print("2P criterion: ",critVal2P)
    print("slope: ",slope2P)
    print("interY2P: ",interY2P)

    #create figure for 1P/2P plots 
    criterionfig, axCrit = plt.subplots(nrows=1,ncols=2) #figsize=(40,40))#create figure 
    criterionfig.set_size_inches(10,10)
    criterionfig.set_figheight(1.2)
    criterionfig.set_figwidth(4)
    chosenFontSize=4 

    #chose contrasting colors 
    NScolor="goldenrod"
    BHcolor="royalblue"

    #plot 1P histogram
    #see all plot colors: https://matplotlib.org/stable/gallery/color/named_colors.html 
    axCrit[0].stairs(count1pNS,bins1pNS,label="NS",color=NScolor,linewidth=1)
    axCrit[0].stairs(count1pBH,bins1pBH,label="BH",color=BHcolor,linewidth=1)
    axCrit[0].axvline(x=criterion1P,ymin=0,ymax=12,linewidth=1,color="red",label=r"$\mu_4$= "+critVal1P)
    axCrit[0].set_xlabel(r"$\mu_4$",fontsize=chosenFontSize,labelpad=2)
    axCrit[0].set_ylabel("Stellar Count",fontsize=chosenFontSize,labelpad=2)
    axCrit[0].set_title("1 Parameter Criterion",fontsize=chosenFontSize)
    axCrit[0].legend(loc='upper left',prop={'size':3},bbox_to_anchor=(0.59,0.97))
    axCrit[0].tick_params(axis='both',which='major',labelsize=chosenFontSize)
    axCrit[0].set_xlim(0,0.2)
    axCrit[0].set_ylim(0,40)
    #axCrit[0].text(0.15,0.25,r"$\mu_4=$"+critVal1P,transform=axCrit[0].transAxes,fontsize=chosenFontSize)
    #plot 2P plot 
    axCrit[1].set_xlabel(r"$M_4\mu_4$",fontsize=chosenFontSize,labelpad=2)
    axCrit[1].set_ylabel(r"$\mu_4$",fontsize=chosenFontSize,labelpad=2)
    axCrit[1].set_title("2 Parameter Criterion",fontsize=chosenFontSize)
    axCrit[1].tick_params(axis='both',which='major',labelsize=chosenFontSize)
    axCrit[1].scatter(plot2PNS[:,0],plot2PNS[:,1],marker='o',s=0.5,label="NS",color=NScolor,zorder=1)
    axCrit[1].scatter(plot2PBH[:,0],plot2PBH[:,1],marker='o',s=0.5,label="BH",color=BHcolor,zorder=2)
    axCrit[1].plot(plot2PcritPoints[:,0],plot2PcritPoints[:,1],color='red',linewidth=0.4,label=r"$\mu_4$=\,"+slope2P+r"$(M_4\mu_4\!\!)$+"+interY2P)
    axCrit[1].scatter(plot2PNSoutliers[:,0],plot2PNSoutliers[:,1],facecolors='none',marker='o',s=2,label="outlier",color='black',linewidth=0.3,zorder=3)
    axCrit[1].scatter(plot2PBHoutliers[:,0],plot2PBHoutliers[:,1],facecolors='none',marker='o',s=2,color='black',linewidth=0.3,zorder=4)
    axCrit[1].legend(loc="upper right",prop={'size':3},bbox_to_anchor=(0.57,0.98))
    axCrit[1].set_xlim(0,0.39)
    axCrit[1].set_ylim(0,0.2)


    #export and show
    criterionfig.tight_layout(pad=1.1)
    #save the figure directly when figure is shown
    #savefig method does not coincide properly
    criterionfig.show()


#------------------------------------------------------------------
    #DSNB flux plots (no MSW, IH, and NH)  
#------------------------------------------------------------------
if plotBool==1:
    print("creating DSNB flux plots")
    #import no MSW plot data 
    rawPlot2PdataNoMSW=loadin("dsnbFluxPlotDataNoMSW.csv")
    rawPlot2PdataIH=loadin("dsnbFluxPlotDataIH.csv")
    rawPlot2PdataNH=loadin("dsnbFluxPlotDataNH.csv")
    #printer(rawPlot2PdataNoMSW)
    #in to convert from strings
    #in the format of [["name",data],...] 
    #such that index 1 max with SFR, index 3 min with SFR
    #index 5 fiducial case, index 7 max, index 9 min

    #chose font size
    chosenFontSize=4 
    #create DSNB flux plots for no MSW, IH, and NH
    #input data, title, fontSize, and fileName (for exportation)
    dsnbFluxPlotter(rawPlot2PdataNoMSW,"DSNB Flux (No MSW)",chosenFontSize,"dsnbFluxNoMSW")
    dsnbFluxPlotter(rawPlot2PdataIH,"DSNB Flux (IH)",chosenFontSize,"dsnbFluxIH")
    dsnbFluxPlotter(rawPlot2PdataNH,"DSNB Flux (NH)",chosenFontSize,"dsnbFluxNH")



#------------------------------------------------------------------
    #Integrated DSNB flux plots 
#------------------------------------------------------------------
if plotBool==2:
    print("creating integrated DSNB flux plot")
    #rawintDSNBFluxData=loadin("intDSNBPlotData.csv")
    #for two different energy integration ranges 16 MeV or 9 MeV to 40 MeV
    rawintDSNBFluxData1640 =loadin("intDSNBPlotData1640.csv")
    rawintDSNBFluxData940 =loadin("intDSNBPlotData940.csv")
    #printer(rawintDSNBFluxData1640)
    #print("\n")
    #printer(rawintDSNBFluxData940)
    
    #get each case 
    #each case is in order of min, fiducial, max
    #formated as [["caseName",[min,fiducial,max]]...]
    #singleVSbinaries=["single vs binary stars",strToArray(rawintDSNBFluxData[0])]

    #reshape from 1D 20 elements i.e. shape of (20,) 
    #to shape (10,2) such that 
    #1st column is list of [min,fiducial,max]  
    #2nd column is list of CaseNames
    intDSNBfluxData1640=rawintDSNBFluxData1640.reshape(10,2)
    intDSNBfluxData940=rawintDSNBFluxData940.reshape(10,2)
    #specs(intDSNBfluxData1640)
    #specs(intDSNBfluxData940)
    tempcaseNames1640 =intDSNBfluxData1640[:,1]
    tempcaseNames940 =intDSNBfluxData940[:,1]
    tempminFidsMaxs1640=strToArray3(intDSNBfluxData1640[:,0]) #convert from str list to numpy array of sub-arrays
    tempminFidsMaxs940=strToArray3(intDSNBfluxData940[:,0]) #convert from str list to numpy array of sub-arrays
    #print(tempminFidsMaxs)
    #print(tempcaseNames)
    #transpose such that columns become rows, i.e. row1 = mins list, row2= fids list, ro3= maxs list
    #these correspond to yerrMin y and yerrMax 
    minFidsMaxs1640= tempminFidsMaxs1640.T 
    minFidsMaxs940= tempminFidsMaxs940.T 
    #prepend a blank """ for index 0 
    caseNames1640=np.insert(tempcaseNames1640,0,"")
    caseNames940=np.insert(tempcaseNames940,0,"")
    #print("data and names for 16-40 MeV")
    #print("minFidMaxs: \n",minFidsMaxs1640,"\n")
    #print("case names: \n",caseNames1640,"\n")
    #print("data and names for 9-40 MeV")
    #print("minFidMaxs: \n",minFidsMaxs940,"\n")
    #print("case names: \n",caseNames940,"\n")

    #create x points (1 to length of data points)
    #also convert from numpy array to list
    #for integrated 16-40 MeV range
    xVals1640=np.arange(1,len(caseNames1640),1).tolist()
    fullxVals1640=np.arange(0,len(caseNames1640)+1,1).tolist()
    #print("original x values:",xVals1640," ",type(xVals1640))
    #print("full x values: ",fullxVals1640)
    #for integrated 9-40 MeV range
    xVals940=np.arange(1,len(caseNames940)-1,1).tolist() #exclude last
    xVals940= np.append(xVals940,len(caseNames940)-0.75)#add last point with offsef 
    print(len(caseNames940))
    fullxVals940=np.arange(0,len(caseNames940)+1,1).tolist()
    #print("original x values:",xVals940," ",type(xVals940))
    #print("full x values: ",fullxVals940)
    #assume no error in x

    #get error in y as [yErrorMin, yErrorMax]
    #convert list of subarrays into lists of sublists
    #indices in order of min, fiducial, max
    #for integrated 16-40 MeV range
    yErrorMax1640=np.subtract(minFidsMaxs1640[2],minFidsMaxs1640[1]).tolist() #max-fiducial then convert to list
    yErrorMin1640=np.subtract(minFidsMaxs1640[1],minFidsMaxs1640[0]).tolist() #fiducial-min then convert to list
    yError1640=[yErrorMin1640,yErrorMax1640]
    #for integrated 9-40 MeV range
    TEMPyErrorMax940=np.subtract(minFidsMaxs940[2],minFidsMaxs940[1]).tolist() #max-fiducial then convert to list
    yErrorMin940=np.subtract(minFidsMaxs940[1],minFidsMaxs940[0]).tolist() #fiducial-min then convert to list
    #prevent negative value in integrated range 9-40 MeV for pinching parameter alpha 
    yErrorMax940=[0 if i<0 else i for i in TEMPyErrorMax940]
    yError940=[yErrorMin940,yErrorMax940]
    #print("\nyError min&max 1640: ",yError1640[0],"\n",yError1640[1]," ",type(yError1640[0]))
    #print("\nyError min&max 940: ",yError940[0],"\n",yError940[1]," ",type(yError940[0]))
    
    #get y values as fids 
    #convert from numpy array to list 
    yVals1640=minFidsMaxs1640[1].tolist()
    yVals940=minFidsMaxs940[1].tolist()
    #print("\n",yVals1640," ",type(yVals1640))
    #print("\n",yVals940," ",type(yVals940))


    #create figure int dsnb flux plot  
    fig3, ax3 = plt.subplots(nrows=1,ncols=1)#create figure 
    #criterionfig.set_size_inches(0.5,1)
    #adjust figure window height and width
    fig3.set_figheight(1.0)
    fig3.set_figwidth(2.2)
    #adjust plot size
    #fig3.tight_layout(pad=1)
    fig3.tight_layout(h_pad=1,w_pad=1.2)
    #chose font size
    chosenFontSize=4 
    colorList =["black","tab:blue","tab:orange","tab:green","tab:purple","tab:red","tan","crimson","dodgerblue","lightsteelblue","gold"]
    colorBlindList=CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']
    #from thriveth from https://gist.github.com/thriveth/8560036 
    color1=colorBlindList[0]
    color2=colorBlindList[2]

    #plot the converted plot data
    #plot error bars, points, and horizontal line 
    ax3.errorbar(xVals1640,yVals1640,yError1640,fmt='o',markersize=0.5,elinewidth=0.5,ecolor=color1,markerfacecolor=color1,
                 markeredgecolor=color1,capsize=1,capthick=0.5,label=r"$E_{\nu}>16 \text{MeV}$")
    ax3.errorbar(xVals940,yVals940,yError940,fmt='o',markersize=0.5,elinewidth=0.5,ecolor=color2,
                 markerfacecolor=color2,markeredgecolor=color2,capsize=1,capthick=0.5,label=r"$E_{\nu}>9 \text{MeV}$")
    #ax3.axhline(2.7,label=r"SK-IV Bound (2021): 2.7 $\text{cm}^{-1}\text{s}^{-1}$",linewidth=0.5,color="red",linestyle='dashed')
    #ax3.fill_between(fullxVals1640,2.7,6,color='gray',alpha=0.3)
    #plot x axis as case names 
    ax3.set_xticks(list(range(11)))
    ax3.set_xticklabels(caseNames1640.tolist(),rotation=90) #assumes caseNames1640 = caseNames940 
    ax3.tick_params(axis='y',which='major',labelsize=chosenFontSize)
    ax3.tick_params(axis='x',which='major',top=False,labelsize=chosenFontSize)
    ax3.tick_params(axis='x',which='minor',bottom=False,top=False) #remove minor ticks 
    #ax3.set_yticks(range(7),labelsize=chosenFontSize)
    #editing the plot
    #ax3.set_ylim(-5,30)
    ax3.set_xlim(fullxVals1640[0],fullxVals1640[-1]) #assumes xvals1640 = xvals940 
    ax3.set_title("Integrated DSNB Flux",fontsize=chosenFontSize)
    ax3.set_yscale("log")
    ax3.set_ylim(0.7,35)
    ax3.set_ylabel(r"$\phi_{\text{above}} (\text{cm}^{-1}\text{s}^{-1}$)",fontsize=chosenFontSize,labelpad=2)
    #ax3.legend(loc='center',bbox_to_anchor=(0.15,0.7,0.1,0.1),prop={'size':chosenFontSize})#x,y,width,height
    #reference for using annotate: https://stackoverflow.com/questions/25123127/how-do-you-just-show-the-text-label-in-plot-legend-e-g-remove-a-labels-line 
    ax3.annotate(r"$E_{\nu}> 9\ \text{MeV}$", xy=(28, 38), xycoords='axes points',
            fontsize=chosenFontSize, ha='right', va='top', 
            bbox=dict(boxstyle='round',pad=0.2, fc='w',linewidth=0.5,edgecolor=color2))
    ax3.annotate(r"$E_{\nu}> 16\ \text{MeV}$", xy=(30, 23), xycoords='axes points',
            fontsize=chosenFontSize, ha='right', va='top', 
            bbox=dict(boxstyle='round',pad=0.2, fc='w',linewidth=0.5,edgecolor=color1))

    #export plot figure 
    #DO NOT save the figure from shown plot (since it chops the text)
    #instead export and save directly (since it re-scales to save the x axis text)
    #fig3.savefig("intDSNBflux.pdf")
    

#------------------------------------------------------------------
    #DSNB flux plot finale (with SK bound)  
#------------------------------------------------------------------
if plotBool==3:

    print("creating DSNB flux finale plot (with SK bound)")
    #import SK bounds 
    #copy and paste from dsnbDataReader_v8 mathematica notebook  
    #rawSKbounds=loadin("dsnbfluxPlotDataFinale.csv")
    rawSKbounds=loadin("dsnbfluxPlotDataSK.csv")
    #printer(rawSKbounds)

    #import no MSW plot data (error bar plot version) 
    rawPlot2PdataNoMSW=loadin("dsnbFluxPlotDataNoMSW.csv")
    #printer(rawPlot2PdataNoMSW)
    #roughly formated as [[xErrorMin,xErrorMax],yValue] at 0,2,4,6 indices
    #other indices are names 

    #tweak string list format 
    #print(rawSKbounds[0][2:-2]+"]","\n")
    #print(rawSKbounds[2][4:-2]+"]")
    #print(rawSKbounds[4][4:-2]+"]")
    #print(rawSKbounds[6][4:-2]+"]")

    #convert the SK limits strings to numpy arrays 
    #formated as [[xErrMins,...],[xErrMaxs,...],[yValues,...]]
    #i.e. each column is xErrMin, xErrMax, or yValue
        #observed SK VI+VII BDT
    SKbounds1=strToArray4(rawSKbounds[0][2:-2]+"]")
    #print("\n",SKbounds1)
        #observed SK VI+VII NN
    SKbounds2=strToArray4(rawSKbounds[2][4:-2]+"]")
    #print(SKbounds2)
        #observed SK VI BDT 
    SKbounds3=strToArray4(rawSKbounds[4][4:-2]+"]")
    #print(SKbounds3)
        #observed SK IV BDT 
    SKbounds4=strToArray4(rawSKbounds[6][4:-2]+"]")
    #print(SKbounds4)

    #create figure 
    fig4, ax4= plt.subplots(nrows=1,ncols=1,tight_layout=True)
    #chose size of figure
    fig4.set_figheight(1.2)
    fig4.set_figwidth(1.7)
    chosenFontSize=4

    #get all dsnb flux data
    tempSFRmax=strToArray2(rawPlot2PdataNoMSW[1])
    tempSFRmin=strToArray2(rawPlot2PdataNoMSW[3])
    tempFiducial=strToArray2(rawPlot2PdataNoMSW[5])
    tempMax=strToArray2(rawPlot2PdataNoMSW[7])
    tempMin=strToArray2(rawPlot2PdataNoMSW[9])
    #plot no MSW plot data
    ax4.semilogy(tempFiducial[:,0],tempFiducial[:,1],label='Fiducial',color='black',linestyle='solid',linewidth=1)
    ax4.semilogy(tempSFRmin[:,0],tempSFRmin[:,1],label='with SFR uncertainty',color='tab:blue',linestyle='solid')
    ax4.semilogy(tempSFRmax[:,0],tempSFRmax[:,1],color='tab:blue',linestyle='solid')
    ax4.semilogy(tempMin[:,0],tempMin[:,1],label='without SFR uncertainty',color='tab:green',linestyle='dashed')
    ax4.semilogy(tempMax[:,0],tempMax[:,1],color='tab:green',linestyle='dashed')
    #plot fillings outer 
    ax4.fill_between(tempSFRmin[:,0],tempMax[:,1],tempSFRmax[:,1],color='tab:blue',alpha=0.3)
    ax4.fill_between(tempSFRmin[:,0],tempSFRmin[:,1],tempMin[:,1],color='tab:blue',alpha=0.3)
    #plot fillings inner 
    ax4.fill_between(tempSFRmin[:,0],tempMin[:,1],tempFiducial[:,1],color='tab:green',alpha=0.3)
    ax4.fill_between(tempSFRmin[:,0],tempFiducial[:,1],tempMax[:,1],color='tab:green',alpha=0.3)
    #adjust axes
    ax4.set_xlabel(r"$\text{E}_{\nu} \text{(MeV)}$",fontsize=chosenFontSize,labelpad=2)
    ax4.set_ylabel(r"$\frac{d\phi}{dE} (\text{MeV}^{-1}\text{cm}^{-2}\text{s}^{-1}$)",fontsize=chosenFontSize,labelpad=2)
    ax4.set_title("DSNB Flux (No MSW)",fontsize=chosenFontSize)
    ax4.tick_params(axis='both',which='major',labelsize=chosenFontSize,width=0.3) #alter major ticks
    ax4.tick_params(axis='both',which='minor',width=0.3) #change size of minor ticks 
    ax4.set_axisbelow(False) #force ticks to be above curves 
    ax4.set_xlim(5,35)
    #print(ax4.get_ylim())
    ax4.set_ylim(10**-3,2*10**2)


    #get x values
    #print(SKbounds1)
    #via average of (xErrMax+xErrMin)/2 
    #print(SKbounds1)
    xVal1= averager(SKbounds1) 
    xVal2=averager(SKbounds2)
    xVal3=averager(SKbounds3)
    xVal4=averager(SKbounds4)
    #print(xVal1)

    #get x errors as [xErrmin,xErrmax] 
    xError1=[xVal1-SKbounds1[0],SKbounds1[1]-xVal1]
    xError2=[xVal2-SKbounds2[0],SKbounds2[1]-xVal2]
    xError3=[xVal3-SKbounds3[0],SKbounds3[1]-xVal3]
    xError4=[xVal4-SKbounds4[0],SKbounds4[1]-xVal4]

    #get y values 
    yVal1=SKbounds1[2]
    yVal2=SKbounds2[2]
    yVal3=SKbounds3[2]
    yVal4=SKbounds4[2]
    #print(yVal1)

    #display the labels for SK bounds
    SKboundLabel1=rawSKbounds[1]
    SKboundLabel2=rawSKbounds[3]
    SKboundLabel3=rawSKbounds[5]
    SKboundLabel4=rawSKbounds[7]

    #plot SK limits 
    ax4.errorbar(xVal1,yVal1,xerr=xError1,fmt='o',markersize=0.5,elinewidth=0.5,ecolor="red",color='red',label=SKboundLabel1,capsize=1,capthick=0.5)
    ax4.errorbar(xVal2,yVal2,xerr=xError2,fmt='d',markersize=0.5,elinewidth=0.5,ecolor="deepskyblue",color='deepskyblue',label=SKboundLabel2,capsize=1,capthick=0.5)
    ax4.errorbar(xVal3,yVal3,xerr=xError3,fmt='s',markersize=0.5,elinewidth=0.5,ecolor="orange",color='orange',label=SKboundLabel3,capsize=1,capthick=0.5)
    #REMOVED SK IV BDT 2021
    #ax4.errorbar(xVal4,yVal4,xerr=xError4,fmt='v',markersize=0.5,elinewidth=0.5,ecolor="purple",color='purple',label=SKboundLabel4,capsize=1,capthick=0.5)
    #create legend
    ax4.legend(loc='lower left',bbox_to_anchor=(0.06,0.05,0.1,0.1),prop={'size':chosenFontSize/2})

#------------------------------------------------------------------
    #DSNB flux plot finale (with theory bound)  
#------------------------------------------------------------------
if plotBool==4:
    print("creating DSNB flux finale plot (with theory bound)")
    #NOTE:DISUSED 
    #import theory bounds
    #rawIvanez23 =loadin2("Ivanez+23.csv")
    #rawBarranco18 =loadin2("Barranco+18.csv")
    #rawKaplinghat00 =loadin2("Kaplinghat+00.csv")
    #rawNakazato24 =loadin2("Nakazato+24.csv")
    #specs(rawIvanez23)
    #sort Barranco+18 data since it is not in ascending order of indep var x
    #in format of [[x,y],...] 
    #Barranco18=rawBarranco18[np.argsort(rawBarranco18[:,0])]

    #import theory bounds combined extrema from Abe etal. 2025 fig 1
    #rawTheoryMax=loadin2("max_fig1_abe2025.csv")
    #rawTheoryMin=loadin2("min_abe2025_fig1.csv")

    #import fiducial theory bounds from Kresse et al. 2021 
    TEMPrawTheoryMax=loadin3("upperGray_kresse2021_fig5.csv")
    TEMPrawTheoryMin=loadin3("lowerGray_kresse2021_fig5.csv")
    #sort into ascending order (otherwise interpolation fails)
    rawTheoryMax=TEMPrawTheoryMax[np.argsort(TEMPrawTheoryMax[:,0])]
    rawTheoryMin=TEMPrawTheoryMin[np.argsort(TEMPrawTheoryMin[:,0])]
    #delete 2nd index duplicate x (somehow mathematica handled this fine but not python?)
    #print(rawTheoryMax)
    rawTheoryMax=np.delete(rawTheoryMax,[2],axis=0)
    #print(rawTheoryMax)


    #interpolate data
    theoryMaxFunc=interp(rawTheoryMax[:,0],rawTheoryMax[:,1])
    theoryMinFunc=interp(rawTheoryMin[:,0],rawTheoryMin[:,1])

    #import no MSW plot data 
    rawPlot2PdataNoMSW=loadin("dsnbFluxPlotDataNoMSW.csv")

    #create figure 
    fig5, ax5= plt.subplots(nrows=1,ncols=1,tight_layout=True)
    #chose size of figure
    fig5.set_figheight(1.2)
    fig5.set_figwidth(1.7)
    chosenFontSize=4

    #create x values
    xVal1=np.arange(5,50,1).tolist()
    #create new theory bound points
    TheoryMin = np.array([(x,theoryMinFunc(x)) for x in xVal1])
    TheoryMax = np.array([(x,theoryMaxFunc(x)) for x in xVal1])

    #plot our no MSW plot data
    #get all dsnb flux data
    tempSFRmax=strToArray2(rawPlot2PdataNoMSW[1])
    tempSFRmin=strToArray2(rawPlot2PdataNoMSW[3])
    tempFiducial=strToArray2(rawPlot2PdataNoMSW[5])
    tempMax=strToArray2(rawPlot2PdataNoMSW[7])
    tempMin=strToArray2(rawPlot2PdataNoMSW[9])
    #plot no MSW plot data
    ax5.semilogy(tempFiducial[:,0],tempFiducial[:,1],label='Fiducial',color='black',linestyle='solid',linewidth=1)
    ax5.semilogy(tempSFRmin[:,0],tempSFRmin[:,1],label='with SFR uncertainty',color='tab:blue',linestyle='solid')
    ax5.semilogy(tempSFRmax[:,0],tempSFRmax[:,1],color='tab:blue',linestyle='solid')
    ax5.semilogy(tempMin[:,0],tempMin[:,1],label='without SFR uncertainty',color='tab:green',linestyle='dashed')
    ax5.semilogy(tempMax[:,0],tempMax[:,1],color='tab:green',linestyle='dashed')
    #plot fillings outer 
    #ax5.fill_between(tempSFRmin[:,0],tempMax[:,1],tempSFRmax[:,1],color='tab:blue',alpha=0.3)
    #ax5.fill_between(tempSFRmin[:,0],tempSFRmin[:,1],tempMin[:,1],color='tab:blue',alpha=0.3)
    #plot fillings inner 
    #ax5.fill_between(tempSFRmin[:,0],tempMin[:,1],tempFiducial[:,1],color='tab:green',alpha=0.3)
    #ax5.fill_between(tempSFRmin[:,0],tempFiducial[:,1],tempMax[:,1],color='tab:green',alpha=0.3)

    #plot theory bounds from fig 5 Kresse et al. 2021 of their fiducial model 
    #originall used theory bands from fig 1 Abe et al. 2025 SK Collab
    theoryColor="gray"
    #NOTE:DISUSED 
    #raw lists data 
    #ax5.semilogy(rawIvanez23[:,0],rawIvanez23[:,1],color=theoryColor,label="Ivanez+23")
    #ax5.semilogy(Barranco18[:,0],Barranco18[:,1],color=theoryColor,label="Barranco+18")
    #ax5.semilogy(rawKaplinghat00[:,0],rawKaplinghat00[:,1],color=theoryColor,label="Kaplinghat+00")
    #ax5.semilogy(rawNakazato24[:,0],rawNakazato24[:,1],color=theoryColor,label="Nakazato+24")
    #plot theory bounds combined extrema 
    ax5.semilogy(TheoryMin[:,0],TheoryMin[:,1],color=theoryColor,linestyle="dotted",label="theory band")
    ax5.semilogy(TheoryMax[:,0],TheoryMax[:,1],color=theoryColor,linestyle="dotted")
    #create filling for theory bounds
    ax5.fill_between(TheoryMax[:,0],TheoryMin[:,1],TheoryMax[:,1],color=theoryColor,alpha=0.5,linewidth=0)


    #beautify the plot
    ax5.set_xlabel(r"$\text{E}_{\nu} \text{(MeV)}$",fontsize=chosenFontSize,labelpad=2)
    ax5.set_ylabel(r"$\frac{d\phi}{dE} (\text{MeV}^{-1}\text{cm}^{-2}\text{s}^{-1}$)",fontsize=chosenFontSize,labelpad=2)
    ax5.set_title("DSNB Flux",fontsize=chosenFontSize)
    ax5.tick_params(axis='both',which='major',labelsize=chosenFontSize,width=0.3) #alter major ticks
    ax5.tick_params(axis='both',which='minor',width=0.3) #change size of minor ticks 
    ax5.set_axisbelow(False) #force ticks to be above curves 
    ax5.set_xlim(5,35)
    ax5.set_ylim(10**-3,2*10**2)
    ax5.legend(loc='upper right',bbox_to_anchor=(0.8,0.8,0.1,0.1),prop={'size':chosenFontSize/2})

#------------------------------------------------------------------
    #binned DSNB flux plot finale (with SK bound)  
#------------------------------------------------------------------
if plotBool==5:

    print("creating binned DSNB flux finale plot (with SK bound)")
    #import SK bounds 
    #copy and paste from dsnbDataReader_v8 mathematica notebook  
    #rawSKbounds=loadin("dsnbfluxPlotDataFinale.csv")
    rawSKbounds=loadin("dsnbfluxPlotDataSK.csv")
    #printer(rawSKbounds)

    #import no MSW plot data binned 
    #already binned using same  energy bins as SK  
    #original format (works for step plot in mathematica, but NOT python)
    #x data formated as start x values plus one x midpoint at end 
    #y data formated as x values and one duplicate at end
    #xStartyValsPlus = loadin("xStartyValsPlus.csv") #fiducial 
    #xStartyValsPlusMin = loadin("xStartyValsPlusMin.csv") #min without SFR uncertainty
    #xStartyValsPlusMax = loadin("xStartyValsPlusMax.csv") #max without SFR uncertainty
    #xStartyValsPlusMinSFR = loadin("xStartyValsPlusMinSFR.csv") #min with SFR uncertainty
    #xStartyValsPlusMaxSFR = loadin("xStartyValsPlusMaxSFR.csv") #max with SFR uncertainty
    #--- Alternatively, use a different format
    #new format (hopefully works for python step plot but NOT mathematica )
    #x data formated as start x values plus one x midpoint at end 
    #y data formated as x values and one duplicate at end
    xStartyValsPlus = loadin("xStartyValsPlus2.csv") #fiducial 
    xStartyValsPlusMin = loadin("xStartyValsPlusMin2.csv") #min without SFR uncertainty
    xStartyValsPlusMax = loadin("xStartyValsPlusMax2.csv") #max without SFR uncertainty
    xStartyValsPlusMinSFR = loadin("xStartyValsPlusMinSFR2.csv") #min with SFR uncertainty
    xStartyValsPlusMaxSFR = loadin("xStartyValsPlusMaxSFR2.csv") #max with SFR uncertainty

    #get all dsnb flux data
    tempFiducial=np.reshape(strToArray3(xStartyValsPlus)[0],(6,2))
    tempSFRmax=np.reshape(strToArray3(xStartyValsPlusMaxSFR)[0],(6,2))
    tempSFRmin=np.reshape(strToArray3(xStartyValsPlusMinSFR)[0],(6,2))
    tempMax=np.reshape(strToArray3(xStartyValsPlusMax)[0],(6,2))
    tempMin=np.reshape(strToArray3(xStartyValsPlusMin)[0],(6,2))
    #print(xStartyValsPlus)
    #print(tempFiducial)
    #specs(tempFiducial)
    #print(tempFiducial[:,0])
    #print(tempFiducial[:,1])


    #convert the SK limits strings to numpy arrays 
        #tweak string list format 
        #print(rawSKbounds[0][2:-2]+"]","\n")
        #print(rawSKbounds[2][4:-2]+"]")
        #print(rawSKbounds[4][4:-2]+"]")
        #print(rawSKbounds[6][4:-2]+"]")
    #formated as [[xErrMins,...],[xErrMaxs,...],[yValues,...]]
    #i.e. each column is xErrMin, xErrMax, or yValue
        #observed SK VI+VII BDT
    SKbounds1=strToArray4(rawSKbounds[0][2:-2]+"]")
    #print("\n",SKbounds1)
        #observed SK VI+VII NN
    SKbounds2=strToArray4(rawSKbounds[2][4:-2]+"]")
    #print(SKbounds2)
        #observed SK VI BDT 
    SKbounds3=strToArray4(rawSKbounds[4][4:-2]+"]")
    #print(SKbounds3)
        #observed SK IV BDT 
    SKbounds4=strToArray4(rawSKbounds[6][4:-2]+"]")
    #print(SKbounds4)

    #create figure 
    fig4, ax4= plt.subplots(nrows=1,ncols=1,tight_layout=True)
    #chose size of figure
    fig4.set_figheight(1.2)
    fig4.set_figwidth(1.7)
    chosenFontSize=4

    #plot no MSW plot data
    ax4.step(tempFiducial[:,0],tempFiducial[:,1],label='Fiducial',color='black',linestyle='solid',linewidth=1)
    ax4.step(tempSFRmin[:,0],tempSFRmin[:,1],label='with SFR uncertainty',color='tab:blue',linestyle='solid')
    ax4.step(tempSFRmax[:,0],tempSFRmax[:,1],color='tab:blue',linestyle='solid')
    ax4.step(tempMin[:,0],tempMin[:,1],label='without SFR uncertainty',color='tab:green',linestyle='dashed')
    ax4.step(tempMax[:,0],tempMax[:,1],color='tab:green',linestyle='dashed')

    #original (does not work but close)
    #plot fillings outer 
    #ax4.fill_between(tempSFRmin[:,0],tempMax[:,1],tempSFRmax[:,1],color='tab:blue',alpha=0.3)
    #ax4.fill_between(tempSFRmin[:,0],tempSFRmin[:,1],tempMin[:,1],color='tab:blue',alpha=0.3)
    #plot fillings inner 
    #ax4.fill_between(tempSFRmin[:,0],tempMin[:,1],tempFiducial[:,1],color='tab:green',alpha=0.3)
    #ax4.fill_between(tempSFRmin[:,0],tempFiducial[:,1],tempMax[:,1],color='tab:green',alpha=0.3)
    #adjust axes
    ax4.set_xlabel(r"$\text{E}_{\nu} \text{(MeV)}$",fontsize=chosenFontSize,labelpad=2)
    ax4.set_ylabel(r"$\frac{d\phi}{dE} (\text{MeV}^{-1}\text{cm}^{-2}\text{s}^{-1}$)",fontsize=chosenFontSize,labelpad=2)
    ax4.set_title("DSNB Flux (No MSW)",fontsize=chosenFontSize)
    ax4.tick_params(axis='both',which='major',labelsize=chosenFontSize,width=0.3) #alter major ticks
    ax4.tick_params(axis='both',which='minor',width=0.3) #change size of minor ticks 
    ax4.set_axisbelow(False) #force ticks to be above curves 
    ax4.set_xlim(5,35)
    #print(ax4.get_ylim())
    ax4.set_ylim(10**-3,2*10**2)
    ax4.set_yscale("log")


    #get x values
    #print(SKbounds1)
    #via average of (xErrMax+xErrMin)/2 
    #print(SKbounds1)
    xVal1= averager(SKbounds1) 
    xVal2=averager(SKbounds2)
    xVal3=averager(SKbounds3)
    xVal4=averager(SKbounds4)
    #print(xVal1)

    #get x errors as [xErrmin,xErrmax] 
    xError1=[xVal1-SKbounds1[0],SKbounds1[1]-xVal1]
    xError2=[xVal2-SKbounds2[0],SKbounds2[1]-xVal2]
    xError3=[xVal3-SKbounds3[0],SKbounds3[1]-xVal3]
    xError4=[xVal4-SKbounds4[0],SKbounds4[1]-xVal4]

    #get y values 
    yVal1=SKbounds1[2]
    yVal2=SKbounds2[2]
    yVal3=SKbounds3[2]
    yVal4=SKbounds4[2]
    #print(yVal1)

    #display the labels for SK bounds
    SKboundLabel1=rawSKbounds[1]
    SKboundLabel2=rawSKbounds[3]
    SKboundLabel3=rawSKbounds[5]
    SKboundLabel4=rawSKbounds[7]

    #plot SK limits 
    ax4.errorbar(xVal1,yVal1,xerr=xError1,fmt='o',markersize=0.5,elinewidth=0.5,ecolor="red",color='red',label=SKboundLabel1,capsize=1,capthick=0.5)
    ax4.errorbar(xVal2,yVal2,xerr=xError2,fmt='d',markersize=0.5,elinewidth=0.5,ecolor="deepskyblue",color='deepskyblue',label=SKboundLabel2,capsize=1,capthick=0.5)
    ax4.errorbar(xVal3,yVal3,xerr=xError3,fmt='s',markersize=0.5,elinewidth=0.5,ecolor="orange",color='orange',label=SKboundLabel3,capsize=1,capthick=0.5)
    #REMOVED SK IV BDT 2021
    #ax4.errorbar(xVal4,yVal4,xerr=xError4,fmt='v',markersize=0.5,elinewidth=0.5,ecolor="purple",color='purple',label=SKboundLabel4,capsize=1,capthick=0.5)
    #create legend
    #ax4.legend(loc='upper right',bbox_to_anchor=(0.85,0.85,0.1,0.1),prop={'size':chosenFontSize/2})
    ax4.legend(loc='lower left',bbox_to_anchor=(0.06,0.05,0.1,0.1),prop={'size':chosenFontSize/2})

#-------------------------------------------------------------------
#outside all if branches
#show plo
plt.show()
