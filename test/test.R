library("rmethrafo")
# download reference genome
rmethrafo::download("hg19","hg19")

# process the bam file (bigWig from bam)
rmethrafo::bamScript("example_medip.bam","hg19/hg19.chrom.sizes")


# predict based on the bigwig file from bam
rmethrafo::predict("hg19","example_medip.bam.sort.bam.bedGraph.sort.bw", paste(path.package("rmethrafo"),"model/rr.pkl",sep="/"),"e1_out")

# predict based on the bigwig file directly
rmethrafo::predict("hg19","example_medip.bw", paste(path.package("rmethrafo"),"model/rr.pkl",sep="/"),"e2_out")


