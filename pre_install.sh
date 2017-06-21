#!/bin/bash

# check operating system (linux or windows)

if [ "$OSTYPE" == "linux-gnu"  ]; then
	if [ -n "$(which apt-get)" ]; then
		# samtools
		echo "righton"
		sudo apt-get install samtools
		# bedtools
		sudo apt-get install bedtools 
	elif [-n "$(which yum)" ]; then
		sudo yum install samtools
		sudo yum instlal bedtools
	else
		echo "automatic installation fails, please install bedtools, samtools manually!"
	fi
	# install bedGraphToBigWig
	curl -O http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/bedGraphToBigWig
	chmod +x bedGraphToBigWig
	echo 'PATH=$PATH:'"$PWD">>~/.profile
	echo 'export PATH' >>~/.profile
	source ~/.profile
	
	# install python packages
	sudo pip install pyBigWig
	sudo pip install numpy
	sudo pip install scipy
	sudo pip install scikit-learn
	
elif [ "$OSTYPE" == "darwin"* ]; then 
	#install home brew
	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	
	# install samtools, bedtools
	brew tap homebrew/science
	brew install tabix
	brew install samtools
	brew install bedtools
	
	curl -O http://hgdownload.cse.ucsc.edu/admin/exe/macOSX.x86_64/bedGraphToBigWig
	chmod +x bedGraphToBigWig
	echo 'PATH=$PATH:'"$PWD">>~/.profile
	echo 'export PATH' >>~/.profile
	source ~/.profile
	
	# install python packages
	sudo pip install pyBigWig
	sudo pip install numpy
	sudo pip install scipy
	sudo pip install scikit-learn
else 
	echo "Sorry, $OSTYPE is not supported,please use Linux or Mac OSX."
	
fi
