#!/usr/bin/env python
"""
methrafo.predict <genome_index><RPKM bigwig><model><output_prefix>
eg.
methrafo.precit hg19 example.bw trained_model.pkl example_out
"""

import pdb,sys,os
import gzip
from File import *
import re
import pyBigWig
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from sklearn.ensemble import RandomForestRegressor
import math
import cPickle as pickle

#-----------------------------------------------------------------------
def fetchGenome(chrom_id,gref):
	with gzip.open(gref+'/'+chrom_id+'.fa.gz','rb') as f:
			lf=f.read()
			lf=lf.split("\n")
			chrom_id=lf[0].split('>')[1]
			chrom_seq="".join(lf[1:])
			chrom_seq=chrom_seq.upper()
	return [chrom_id,chrom_seq]
 
def cgVector(chrom):
	chrom_seq=chrom[1]
	cgV=[m.start() for m in re.finditer('CG',chrom_seq)]
	return cgV
	

def scoreVector(chrom,cgv,bwFile):
	bw=pyBigWig.open(bwFile)
	chrom_name=chrom[0]
	sc=bw.values(chrom_name,0,len(chrom[1]))
	sv=[0 if math.isnan(sc[item]) else sc[item]  for item in cgv ]
	return sv
	
def nearbyCGVector(cgv,nearbycut):
	nearcgs=[]
	for i in range(len(cgv)):
		j=i-1
		leftcgs=[]
		rightcgs=[]
		while (j>0):
			if abs(cgv[j]-cgv[i])>nearbycut:
				break 
			else:
				leftcgs.append(j)
			j=j-1
		
		j=i+1
		while (j<len(cgv)):
			if abs(cgv[j]-cgv[i])>nearbycut:
				break
			else:
				rightcgs.append(j)
			j=j+1
		inearcgs=leftcgs+rightcgs
		nearcgs.append(inearcgs)
	return nearcgs
	
def nearbyCGScoreVector(chrom,bwFile,cgv,nearcgs):
	# the contribution of nearby CGs on current CG
	nearcgsS=[]
	bw=pyBigWig.open(bwFile)
	chrom_name=chrom[0]
	k=5 # distance weight parameter
	for i in range(len(nearcgs)):
		cgi=nearcgs[i]
		si=0
		for j in cgi:
			dij=abs(cgv[j]-cgv[i])
			try:
				sj=bw.stats(chrom_name,cgv[j],cgv[j]+1)[0]
			except:
				sj=0
			sj=0 if sj==None else sj
			si+=(sj/dij)*k
		nearcgsS.append(si)
	return nearcgsS
			
def Vector2Wig(chri,cgv,rv):
	wigString="variableStep chrom="+chri+" span=2"
	wigS=[]
	for i in range(len(cgv)):
		wigS.append(str(cgv[i])+' '+str(rv[i]))
	wigS='\n'.join(wigS)
	wigString=wigString+'\n'+wigS
	return wigString
	
#----------------------------------------------------------------------


def main():
	# reference genomes
	
	if len(sys.argv[1:])!=4:
		print(__doc__)
		sys.exit(0)
		
	gref=sys.argv[1]
	chroms=os.listdir(gref)
	dchrom={}
	# bigwig file-MeDIP-seq
	bwFile=sys.argv[2]
	
	f=open(sys.argv[3],'rb')
	rfregressor=pickle.load(f)
	f.close()
	
	nearbycut=90
	output=sys.argv[4]
	
	#----------------------------------------------------------------------
	print("predicting...")
	wig_track="track type=wiggle_0  visibility=full"
	f=open(output+'.wig','a')
	f.write(wig_track+'\n')
	for i in chroms:
		if i[0:3]=='chr':
			iid=i.split('.')[0]
			try:
				chromi=fetchGenome(iid,gref)
				cgv=cgVector(chromi)
				sv=scoreVector(chromi,cgv,bwFile)
				nearcgs=nearbyCGVector(cgv,nearbycut)   # number of cgs nearby
				FI=[]
				for j in range(len(cgv)):
					fij=[sv[j],len(nearcgs[j])]
					FI.append(fij)
					
				rv=list(rfregressor.predict(FI))
				wig_rv=Vector2Wig(iid,cgv,rv)
				f.write(wig_rv+'\n')
				print(iid)
			except:
				pass 
	f.close()


if __name__=="__main__":
	main()
	
	
		
		


