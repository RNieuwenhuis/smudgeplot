import argparse
import sys
import os
import logging

class parser():
    def __init__(self):
        argparser = argparse.ArgumentParser(
            # description='Inference of ploidy and heterozygosity structure using whole genome sequencing data',
            usage='''smudgeplot <task> [options] \n
tasks: cutoff    Calculate meaningful values for lower/upper kmer histogram cutoff.
       hetkmers  Calculate unique kmer pairs from a Jellyfish or KMC dump file.
       plot      Generate 2d histogram; infere ploidy and plot a smudgeplot.
       map       Map kmers of individual smudges to a genome.\n\n''')
        argparser.add_argument('task', help='Task to execute; for task specific options execute smudgeplot <task> -h')
        argparser.add_argument('-v', '--version', action="store_true", default = False, help="print the version and exit")
        # print version is a special case
        if len(sys.argv) > 1:
            if sys.argv[1] in ['-v', '--version']:
                self.task = "version"
                return
            # the following line either prints help and die; or assign the name of task to variable task
            self.task = argparser.parse_args([sys.argv[1]]).task
        else:
            self.task = ""
        # if the task is known (i.e. defined in this file);
        if hasattr(self, self.task):
            # load arguments of that task
            getattr(self, self.task)()
        else:
            argparser.print_usage()
            logging.error('"' + self.task + '" is not a valid task name')
            exit(1)

    def hetkmers(self):
        '''
        Calculate unique kmer pairs from a Jellyfish or KMC dump file.
        '''
        argparser = argparse.ArgumentParser(prog = 'smudgeplot hetkmers',
            description='Calculate unique kmer pairs from a Jellyfish or KMC dump file.')
        argparser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Alphabetically sorted Jellyfish or KMC dump file (stdin).')
        argparser.add_argument('-o', help='The pattern used to name the output (kmerpairs).', default='kmerpairs')
        argparser.add_argument('--middle', dest='middle', action='store_const', const = True, default = False,
                          help='Get all kmer pairs one SNP away from each other (default: just the middle one).')
        self.arguments = argparser.parse_args(sys.argv[2:])

    def plot(self):
        '''
        Generate 2d histogram; infer ploidy and plot a smudgeplot.
        '''
        argparser = argparse.ArgumentParser(prog = 'smudgeplot plot', description='Generate 2d histogram for smudgeplot')
        argparser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='name of the input tsv file with covarages (default \"coverages_2.tsv\")."')
        argparser.add_argument('-o', help='The pattern used to name the output (smudgeplot).', default='smudgeplot')
        argparser.add_argument('-q', help='Remove kmer pairs with coverage over the specified quantile; (default none).', type=float, default=1)
        argparser.add_argument('-L', help='The lower boundary used when dumping kmers (default min(total_pair_cov) / 2).', type=int, default=0)
        argparser.add_argument('-n', help='The expected haploid coverage (default estimated from data).', type=int, default=0)
        argparser.add_argument('-t', '--title', help='name printed at the top of the smudgeplot (default none).', default='')
        argparser.add_argument('-m', '-method', help='The algorithm for annotation of smudges (default \'local_aggregation\')', default='local_aggregation')
        argparser.add_argument('-nbins', help='The number of nbins used for smudgeplot matrix (nbins x nbins) (default autodetection).', type=int, default=0)
        # argparser.add_argument('-k', help='The length of the kmer.', default=21)
        argparser.add_argument('-kmer_file', help='Name of the input files containing kmer seuqences (assuming the same order as in the coverage file)', default = "")
        argparser.add_argument('--homozygous', action="store_true", default = False, help="Assume no heterozygosity in the genome - plotting a paralog structure; (default False).")
        self.arguments = argparser.parse_args(sys.argv[2:])

    def cutoff(self):
        '''
        Calculate meaningful values for lower/upper kmer histogram cutoff.
        '''
        argparser = argparse.ArgumentParser(prog = 'smudgeplot cutoff', description='Calculate meaningful values for lower/upper kmer histogram cutoff.')
        argparser.add_argument('infile', type=argparse.FileType('r'), help='Name of the input kmer histogram file (default \"kmer.hist\")."')
        argparser.add_argument('boundary', help='Which bounary to compute L (lower, default) or U (upper)', default = 'L')
        self.arguments = argparser.parse_args(sys.argv[2:])

    def map(self):
        '''
        Identify extracted kmer pairs from individual smudges to a genome.
        '''
        argparser = argparse.ArgumentParser(prog = 'smudgeplot map', description='Identify extracted kmer pairs from individual smudges to a genome.')
        argparser.add_argument('genomefile', help='The reference genome (fasta file; can be gunzipped).')
        argparser.add_argument('-o', help='The pattern used to read kmers and output (default \"smudgeplot\").', default='smudgeplot')
        argparser.add_argument('-s', help='Smudge to be mapped (intiger, ordered by size; default is to map all smudges)', type = int, default = 0)
        self.arguments = argparser.parse_args(sys.argv[2:])
