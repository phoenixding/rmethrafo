download <- function(name,out) {
  path <- paste(system.file(package="rmethrafo"), "download_genomes.py", sep="/")
  command <- paste("python", path, name, out)
  response <- system(command)
  print(response)
}

bamScript <- function(bamFile,genome_size){
	path<-paste(system.file(package="rmethrafo"), "bamScripts.py", sep="/")
	command<- paste("python",path,bamFile,genome_size)
	response<-system(command)
	print(response)
}

predict<- function(genome_index,medip_rpkm,model,out_prefix){
	path<- paste(system.file(package="rmethrafo"), "meth_predict.py", sep="/")
	command<- paste("python", path,genome_index,medip_rpkm,model,out_prefix)
	response<-system(command)
	print(response)
}

train<- function(genome_index,medip_rpkm,bs_seq,trained_model_prefix){
	path<-paste(system.file(package="rmethrafo"),"meth_train.py", sep="/")
	command<-paste("python", path, genome_index,medip_rpkm,bs_seq,trained_model_prefix)
	response<-system(command)
	print(response)
}



