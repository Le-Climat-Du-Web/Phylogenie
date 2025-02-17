#####################################################################################
#                           Import & Librairies                                     #
#####################################################################################
import sys
import time
import random
import string
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Bio import Entrez, AlignIO, SeqIO, Phylo
from Bio.Align.Applications import ClustalwCommandline, MuscleCommandline
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.Phylo import PhyloXML
from Bio.Phylo.Applications import PhymlCommandline

######################################################################################
######################################################################################

def get_random_string(length):
    """Générer une chaîne aléatoire de longueur fixe"""
    str = string.ascii_lowercase
    return ''.join(random.choice(str) for i in range(length))


def get_fasta(id_list):
    # Create a random name for each user session and create corresponding
    # directories in order to allow multiple simultaneous uses without loss of data
    dirName = get_random_string(10) + "/" 
    os.makedirs(saveDir + dirName, exist_ok=True)
    # write a fasta file for each gene
    filename_list = []
    for gene_id in id_list:
        records = Entrez.efetch(db="nucleotide", id=gene_id, rettype="fasta",
                                retmode="text")
        filename = (gene_id + '.fasta').format(records)
        filename_list.append(saveDir + dirName + filename)
        print('Writing:{}'.format(filename))
        time.sleep(1)
        with open(saveDir + dirName + filename, 'w') as f:
            f.write(records.read())
            f.close()

    # combine files in multifasta file
    with open(saveDir + dirName + 'multifasta.fasta', 'w') as outfile:
        for fname in filename_list:
            with open(fname) as infile:
                outfile.write(infile.read())
    return dirName


def clustal_alignment(infile, outfile):
    # create an alignment file with clustal omega
    
    clustal_exe = "C:/wamp64/www/Phylogenie/static/tools/Windows/clustal-omega-1.2.2-win64/clustalo.exe"

    cline = ClustalwCommandline(clustal_exe, infile= saveDir + dirName + infile,
                                outfile= saveDir + dirName + outfile)
    stdout, stderr = cline()


def muscle_alignment(infile, outfile):
    #create an alignment file with muscke

    muscle_exe = "C:/wamp64/www/Phylogenie/static/tools/Windows/muscle3.8.31_i86win32.exe"

    in_file = saveDir + dirName + infile
    out_file = saveDir + dirName + outfile
    muscle_cline = MuscleCommandline(muscle_exe, input=in_file, out=out_file)
    stdout, stderr = muscle_cline()


def NJ_tree(infile, file_type):
    #Tree creation with neighbor-joining
    filename = saveDir + dirName + infile
    #clustal si alignement clustal, fasta si alignement fasta
    aln = AlignIO.read(filename, file_type) 
    calculator = DistanceCalculator('identity')
    # nj ou UPGMA
    constructor = DistanceTreeConstructor(calculator, 'nj') 
    tree = constructor.build_tree(aln)
    # print(tree)
    #display a tree on terminal
    #Phylo.draw_ascii(tree)
    tree.ladderize()
    Phylo.draw(tree, do_show=False)
    Phylo.write(tree, saveDir + dirName + 'tree.txt', "newick")
    foo = current_path + saveDir + dirName + 'tree.png'
    plt.savefig(foo)


def ML_tree(infile, outfile, file_type):
    # Tree creation with maximum-likelihood algorithm (phyML)
    # input : infile = .fasta alignment file that the user can import or paste,
    # outfile = name of output file, file_type = clustal is the clustal too has been used,
    # fasta if muscle tool has been used
    # output : .newick file and .png picture to display
    # phylogeny page should allow to choose maximum likelihood method

    # convert file to phylip
    records = SeqIO.parse(saveDir + dirName + infile, file_type)  # clustal <-> fasta
    count = SeqIO.write(records, saveDir + dirName + outfile + ".phylip", "phylip")
    print("Converted %i records" % count)

    cmd = PhymlCommandline("C:/wamp64/www/Phylogenie/static/tools/Windows/PhyML-3.1/PhyML-3.1_win32.exe",
                               input= saveDir + dirName + outfile + '.phylip')

    out_log, err_log = cmd()
    tree = Phylo.read(saveDir + dirName + outfile + '.phylip_phyml_tree.txt', 'newick')
    Phylo.draw(tree, do_show=False)
    Phylo.write(tree, saveDir + dirName + 'tree.txt', "newick")
    foo = saveDir + dirName + 'tree.png'
    plt.savefig(foo)


##################################################################################################
################################# PROGRAMME PRINCIPAL ############################################
##################################################################################################
#Contact address
Entrez.email = "climat.web@gmail.com"

# list of genes
id_list = ["AY158636.1","AY158639.1","AY159811.1","AY159808.1","AY159809.1","AY158637.1",
           "AY159810.1"]
name_gene = ["Vipera berus Pla2Vb", "Vipera berus AmtI2", "Vipera berus AmtI1", 
             "Vipera aspis AmtI1", "Vipera aspis AmtI1", "Vipera aspis (AmtI2)",
             "Vipera aspis zinnikeri AmtI1"]

# Variables globales
dirName = " "
saveDir = "C:/wamp64/www/Phylogenie/static/data/sauvegardes/"

##################################################################################################
##################################################################################################
##################################################################################################

## Function calls to use the program in the terminal without the user interface
#dirName = get_fasta(id_list)
#clustal_alignment("multifasta.fasta","msa_clustal.fasta")
#muscle_alignment("multifasta.fasta","msa_muscle.fasta")
#NJ_tree("msa_clustal.fasta", "clustal")
#ML_tree("msa_clustal.fasta", "msa_muscle", "clustal")
