# -*- coding: utf-8 -*-
# http://sourceforge.net/projects/srst
#
# Uses blastn to identify MLST from finished genomes or contig sets
# See srst.sourceforge.net for a readme file, as well as the SRST script for determining MLST
# direct from Illumina reads.
# Questions, comments, corrections, please email kholt@unimelb.edu.au

#Copyright 2012 University of Melbourne All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, are
#permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice, this list of
#      conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright notice, this list
#      of conditions and the following disclaimer in the documentation and/or other materials
#      provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY <COPYRIGHT HOLDER> ''AS IS'' AND ANY EXPRESS OR IMPLIED
#WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
#CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This is a python script that uses blastn to extract MLST information from assembled genomes
or contigs.You need to have python installed, and blastn must be installed and accessible
in your path (download BLAST+ from ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/).

Usage:
python mlstBLAST.py -s Sp_summary.txt -d spneumoniae.txt genome1.fasta genome2.fasta genome3.fasta

Options:
  -h, --help            show this help message and exit
  -s SUMMARY, --summary=SUMMARY
                        text file giving paths to allele sequences (one
                        line/file per locus)
  -d DATABASE, --database=DATABASE
                        MLST profile database (col1=ST, other cols=loci, must
                        have loci names in header)
  -n NAMESEP, --namesep=NAMESEP
                        separator for allele names (either '-' (default) or '_')

Required inputs are:

(1) Locus variant sequences in fasta format, available from http://pubmlst.org/data/

E.g. for S. pneumoniae, download these files:

http://pubmlst.org/data/alleles/spneumoniae/aroe.tfa
http://pubmlst.org/data/alleles/spneumoniae/ddl_.tfa
http://pubmlst.org/data/alleles/spneumoniae/gdh_.tfa
http://pubmlst.org/data/alleles/spneumoniae/gki_.tfa
http://pubmlst.org/data/alleles/spneumoniae/recP.tfa
http://pubmlst.org/data/alleles/spneumoniae/spi_.tfa
http://pubmlst.org/data/alleles/spneumoniae/xpt_.tfa

(2) A text file listing the locations of these fasta files (-s).

E.g. you can generate the appropriate list of the files above, using this command:

ls *.tfa > Sp_summary.txt

which gives you a file called 'Sp_summary.txt' containing this list:

aroe.tfa
ddl_.tfa
gdh_.tfa
gki_.tfa
recP.tfa
spi_.tfa
xpt_.tfa

(3) A MLST profile database, which can be downloaded from http://pubmlst.org/data/ (-d).

E.g. for S. pneumoniae, download this file:
http://pubmlst.org/data/profiles/spneumoniae.txt

(4) Your assembled sequences, with each strain in a separate fasta/multifasta formatted file.

(5) You may need to check what delimiter is used in the locus variant sequences, to separate the locus name from the variant number (-n).
Note that some MLST databases use a different character (e.g. ‘_’) to separate the locus label (‘aroe’) from the allele number (‘1’), so it might be aroe_1, aroe_2 rather than aroe-1, aroe-2. This is OK but the script assumes by default that a dash ‘-' is used, so if it is anything other than this you need to specify it in the command via the –n argument.

Output:

Column 1 = strain name, taken from the input files (eg genome1, genome2, genome3)
Column 2 = ST with perfect match to the genome
            if no perfect match is found, this will be 0
            if a novel combination of known alleles is identified, this will be given a new number
Columns 3-n = locus variants for each allele, where perfect matches to known variants were identified
Subsequent columns = closest ST and locus variants
            where no perfect match is found for a given locus, the nearest locus will be reported, followed by the % nucleotide identity of the match and % of the sequence length of the match (if no matches with >90% identity and >90% length are found, none will be reported)
            where perfect or imperfect allele matches were obtained for all loci, the closest ST will be reported
            if a novel combination of known alleles is identified, this will be given a new number
"""
import os
import re
import sys
import string
import subprocess
import collections
from optparse import OptionParser


def main():

    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    # required qsub options
    parser.add_option("-s", "--summary", action="store", dest="summary", help="text file giving paths to allele sequences (one line/file per locus)", default="")
    parser.add_option("-d", "--database", action="store", dest="database", help="MLST profile database (col1=ST, other cols=loci, must have loci names in header)", default="")
    parser.add_option("-n", "--namesep", action="store", dest="namesep", help="separator for allele names (either '-' (default) or '_')", default="-")

    return parser.parse_args()

if __name__ == "__main__":

    (options, args) = main()

    if options.database == "":
        print "No MLST databse provided (-d)"

    # key = id (file name before extension), value = path to sequences
    locus_seqs = {}

    if options.summary == "":
        print "No query sequences provided (-s)"
    else:
        f = file(options.summary, "r")
        for line in f:
            line.rstrip()
            (path, fileName) = os.path.split(line)
            if not os.path.exists(fileName + ".nin"):
                os.system("makeblastdb -dbtype nucl -logfile blast.log -in " + fileName)
            (fileName, ext) = os.path.splitext(fileName)
            locus_seqs[fileName] = line
        f.close()

    # key = concatenated string of alleles, value = st
    sts = {}
    # changeable variable holding the highest current ST, incremented when novel combinations are encountered
    max_st = 0
    header = []
    f = file(options.database, "r")
    for line in f:
        fields = line.rstrip().split("\t")
        if len(header) == 0:
            header = fields
            # remove st label
            header.pop(0)
        else:
            sts[",".join(fields[1:])] = fields[0]
            if int(fields[0]) > max_st:
                max_st = int(fields[0])
    f.close()

    # check the loci match up
    for locus in header:
        if locus not in locus_seqs:
            DoError("Locus " + locus + "in ST database file " + options.database + " but no matching sequence in " + options.summary)
    # key1 = strain, key2 = locus, value = best match (clean for ST, annotated)
    best_match = collections.defaultdict(dict)
    # key1 = strain, key2 = locus, value = perfect match if available
    perfect_match = collections.defaultdict(dict)

    # print header
    print "\t".join(["strain", "perfectMatchST"] + header + ["bestMatchST"] + header)

    for contigs in args:
        tmp = contigs + ".tmp"
        (dir, fileName) = os.path.split(contigs)
        (name, ext) = os.path.splitext(fileName)
        perfect_st = []
        best_st = []
        best_st_annotated = []
        for locus in header:
            # correct order to build up concatenated ST
            locus_seq = locus_seqs[locus]
            cmd = " ".join(["blastn", "-query", contigs, "-db", locus_seq.rstrip(), "-max_target_seqs", "1", "-outfmt '6 qseqid sacc pident length slen qlen'", ">", tmp, "\n"])
            os.system(cmd)
            # read results
            if os.stat(tmp)[6] != 0:
                # file is not empty, ie match found
                match = ""
                f = file(tmp, "r")
                # only has one line
                fields = f.readline().rstrip().split("\t")
                (contig, allele, pcid, length, allele_length, contig_length) = (fields[0], fields[1].split(options.namesep)[1], float(fields[2]), int(fields[3]), int(fields[4]), int(fields[5]))
                if pcid == 100.00 and allele_length == length:
                    match = ""
                    perfect_st.append(allele)
                    best_st.append(allele)
                    best_st_annotated.append(allele)
                elif pcid > 90 and float(length)/float(allele_length) > 0.9:
                    match = "/" + str(pcid) + "," + str(float(length)/float(allele_length))
                    perfect_st.append("-")
                    best_st.append(allele)
                    best_st_annotated.append(allele + match)
                else:
                    # no allele at all
                    perfect_st.append("-")
                    best_st.append("-")
                    best_st_annotated.append("-")
                f.close()
            else:
                # no allele at all
                perfect_st.append("-")
                best_st.append("-")
                best_st_annotated.append("-")
            os.system("rm -rf "+tmp)

        # assign ST
        pst = ",".join(perfect_st)
        bst = ",".join(best_st)

        if pst in sts:
            pst = sts[pst]
        elif "-" not in pst:
            # new combination
            max_st += 1
            sts[pst] = str(max_st)
            pst = str(max_st)
        else:
            pst = "0"

        if bst in sts:
            bst = sts[bst]
        elif "-" not in bst:
            # new combination
            max_st += 1
            sts[bst] = str(max_st)
            bst = str(max_st)
        else:
            bst = "0"

        if best_st != best_st_annotated:
            bst = "*"+bst

        print "\t".join([name, pst] + perfect_st + [bst] + best_st_annotated)
