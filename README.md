```
     ___  ___     _   _    ______       __      
     |  \/  |    | | | |   | ___ \     / _|     
 _ __| .  . | ___| |_| |__ | |_/ /__ _| |_ ___  
| '__| |\/| |/ _ \ __| '_ \|    // _` |  _/ _ \ 
| |  | |  | |  __/ |_| | | | |\ \ (_| | || (_) |
|_|  \_|  |_/\___|\__|_| |_\_| \_\__,_|_| \___/ 
                                                
                                                
```                                             
[![Build Status](https://travis-ci.org/phoenixding/rmethrafo.svg?branch=master)](https://travis-ci.org/phoenixding/rmethrafo)                                     		 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)	
			 
# INTRODUCTION


This software is designed to estimate genome-wide absolute methylation 
level based on the MeDIP-Seq data. This is the R wrapped version of the
MethRafo package in python. 

# SUPPORTED PLATFORMS

Linux, Mac OS

# PREREQUISITES

python 2.7.x

It was installed by default for most Linux distributions and MAC.  
If not, please refer to https://www.python.org/downloads/ for installation 
instructions. 

Python packages dependencies:  
-- scikit-learn   
-- scipy  
-- numpy  
-- pyBigWig

External packages dependencies:  
The software requires the following external packages to process bam files.
(The following packages must be installed if you want to calculate methylation
level based on raw bam files).
--samtools  
--bedtools  
--bedGraphToBigWig  

We provided a "pre_install" shell script to install those dependencies automatically. 
However, please install them manually if the automatic installation fails. 
```
$ ./pre_install
```

Note, you might need to close the terminal afterwards and open a new 
terminal for the following processes. 

manual dependencies installation (**skip this section if the automatic dependency installation succeeded**):   

* (1) samtools, bedtools  
	For debian/ubuntu based linux, you can install samtools,bedtools directly by:
	```
	$sudo apt-get install samtools
	$sudo apt-get install bedtools
	```
	For redhat/centos/fedora linux, you can install samtools, bedtools directly by:
	```
	$sudo yum install samtools
	$sudo yum install bedtools
	```
	If you can't install samtools,bedtools using the commands above, please refer to 
	the manual pages for installation instructions.   
	samtools: http://samtools.sourceforge.net/   
	bedtools: http://bedtools.readthedocs.io/en/latest/  
	
	For mac os, you can install samtools, bedtools directly by :
	
	brew tap homebrew/science
	brew install samtools 
	brew install bedtools
	
	If you don't have the Homebrew package manager in your system, please refer https://brew.sh/ for installation instructions. 

* (2) bedGraphToWigBig  
	First download the excutable file from UCSC web-site.

	For Linux, 
	http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/  
	For Mac os,
	http://hgdownload.cse.ucsc.edu/admin/exe/macOSX.x86_64/

	Second, add the script to os path.   
	Open a terminal, then type
	```
	$export PATH=$PATH:~/path_to_bedGraphToWigBig_Folder
	```
	If you need it permanently, add the above command to your ~/.profile  

	Please refer to the following page for how to set $PATH on linux.  
	http://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux

# INSTALLATION

Open R and type in: 

```R
library(devtools)
devtools::install_github("phoenixding/rmethrafo")
```
if devtools is not installed in your R, please install it by:


```R
install.packages("devtools")

```

Or, you can download the repository from github, then build and install 
the R-package

```
$ R CMD build rmethrafo
$ R CMD INSTALL rmethrafo_1.0.tar.gz
```

USAGE
========================================================================
   
The following 4 commands were provided by the methrafo package:   
rmethrafo::download, rmethrafo::bamScript, rmethrafo::train, rmethrafo::predict.     

* *1) rmethrafo::download*   
	This command is used to download the genome files.  
	Files: chromosome sequences(e.g. chr1.fa.gz), chromosome sizes(e.g. hg19.chrom.sizes)
	```R
	rmethrafo::download(reference_genome_id,output_directory)
	```
	example:  
	```
	rmethrafo::download("hg19","hg19")
	```
	reference_genome_id represents the ID of the genome (e.g. hg19,mm10, et al.)

* *2) rmethrafo::bamScript*     
	This command is used to convert bam file to bigWig file (RPKM).  
	```R
	rmethrafo::bamScript(bamFile,genome_size)
	```
	bamFile => bam file path  
	genome_size file => chromosome sizes file path
	
	```
	chr1	249250621
	chr2	243199373
	chr3	198022430
	chr4	191154276
	chr5	180915260
	chr6	171115067
	chr7	159138663
	chrX	155270560
	chr8	146364022
	chr9	141213431
	chr10	135534747
	chr11	135006516
	chr12	133851895
	chr13	115169878
	chr14	107349540
	chr15	102531392
	chr16	90354753
	chr17	81195210
	chr18	78077248
	chr20	63025520
	chrY	59373566
	chr19	59128983
	chr22	51304566
	chr21	48129895
	```
	
	example:  
	```
	rmethrafo::bamScript("example_medip.bam" "hg19/hg19.chrom.sizes")
	```

*  *3) rmethrafo::train*  
	This command is used to train the random forest model.
	```R
	rmethrafo::train(genome_index,medip_rpkm,bs_seq,trained_model_prefix)
	
	```
	genome_index: The downloaded genome reference folder path (e.g. hg19).    
	medip_rpkm : The bigWig file representing the RPKM on each position of the genome based on MeDIP-Seq data.    
	bs_seq: The bigWig file representing the Bisulfite-Seq methylation level (ground truth).     
	Note: if your input is .bam file, please use rmethrafo::bamScript to convert it to bigWig format first.  
	
	example:  
	```R
	rmethrafo::train("hg19","example_medip.bw","example_bisulfite.bw","trained_model.pkl")
	```

* *4) rmethrafo::predict*  
	This command is used to predict the methylation level based on MeDIP-Seq data.
	
	example:  
	```R
	rmethrafo::predict("hg19","example_medip.bw","model/rr.pkl","example_out")
	```
	
# TEST EXAMPLE
We provided a test example inside the "test" folder. 
"test.R" is the R script to perform the test on the example dataset. 

```R
library("rmethrafo")
# download reference genome
#rmethrafo::download("hg19","hg19")

# process the bam file (bigWig from bam)
rmethrafo::bamScript("example_medip.bam","hg19/hg19.chrom.sizes")


# predict based on the bigwig file from bam
rmethrafo::predict("hg19","example_medip.bam.sort.bam.bedGraph.sort.bw", paste(path.package("rmethrafo"),"model/rr.pkl",sep="/"),"e1_out")

# predict based on the bigwig file directly
rmethrafo::predict("hg19","example_medip.bw", paste(path.package("rmethrafo"),"model/rr.pkl",sep="/"),"e2_out")

```
	  
# CREDITS

This software was developed by ZIV-system biology group @ Carnegie Mellon University  
Implemented by Jun Ding


# LICENSE 

This software is under MIT license.  
see the LICENSE.txt file for details. 


# CONTACT

zivbj at cs.cmu.edu  
jund  at andrew.cmu.edu




                                 
                                 
                                 
                                 
                                 

                                                         
