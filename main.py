import sys
import os
import numpy as np
from optparse   import OptionParser
import pandas as pd
import itertools

import logging
logging.basicConfig(level=logging.INFO,format='%(levelname)-5s @ %(asctime)s: %(message)s ',stream=sys.stderr)


class MaxSubGroup(object):
    def __init__(self, mis, infile):
        self.mismatch = mis
        self.infile   = infile
        
    def load_file(self):
        self.l_seq = []
        f_infile = open(self.infile, "r")
        for line in f_infile:
            line = line.strip()
            f    = line.split()
            seq  = "%s%s" % (f[1], f[3])
            self.l_seq.append(seq)
        f_infile.close()
    
    def cal_mis_mat(self):
        self.np_mis = np.zeros([ len(self.l_seq), len(self.l_seq) ])
        for i, seq1 in enumerate(self.l_seq):
            for j, seq2 in enumerate(self.l_seq):
                mismatch = self.__cal_mis(seq1, seq2)
                self.np_mis[i, j] += mismatch
    
    def output_mat(self):
        self.df_mis = pd.DataFrame(self.np_mis,columns=self.l_seq, index=self.l_seq)
        self.df_mis.to_csv( "mismatch.xls",sep="\t" )
        
        self.df_mis2 = pd.DataFrame(np.ones([len(self.l_seq),len(self.l_seq)]),columns=self.l_seq, index=self.l_seq)
        self.df_mis2[ self.df_mis < self.mismatch ] = 0
        
        
        self.df_mis2.to_csv( "is_pass.xls",sep="\t" )
        
        
        self.__build_hash()
        
        self.hash_stat = []
        self.hash_next = []
        self.__init_stat()
        
        tmp_pre = self.hash_stat
        logging.info( 'Lever 2 is initiated.' )
        tmp = self.__next_stat2()
        logging.info( 'Lever 3 processing done.')
        
#        print "NEW!!", tmp
        N = 3
        while tmp.shape[0] > 0:
            self.hash_stat = tmp
            tmp = self.__next_stat2()
            N+=1
            print "%d" % N
            logging.info( 'Lever %d processing done.' % ( N ) )
            print tmp
            if tmp.shape[0] > 0:
                tmp_pre = tmp
        
#        print tmp_pre
        for idx in tmp_pre:
            np_seq = np.array(self.l_seq, dtype="string")
            idx = np.array(idx, dtype="int")
#            print idx, len(self.l_seq), self.l_seq
#            print np_seq[idx]
            print ",".join( np_seq[idx] )
    
    def __build_hash(self):
        self.hash_l2h = {}  # low to high, in order
        self.hash_h2l = {}  # high to low, in reverse
        for l in xrange(len(self.l_seq)):
            for h in xrange(l, len(self.l_seq)):
                if l not in self.hash_l2h:
                    self.hash_l2h[l] = []
                if h not in self.hash_h2l:
                    self.hash_h2l[h] = []

                if self.df_mis2.values[l][h] == 1:
                    self.hash_l2h[l].append(h)
                    self.hash_h2l[h].append(l)
        
    def __init_stat(self):
        self.hash_stat = []
        for k, v in self.hash_h2l.iteritems():
            for vv in v:
                self.hash_stat.append([k, vv])
    
    def __next_stat(self):
        
        l_out = []
        for l_elem in self.hash_stat:
            l_tmp = []
            for i in l_elem:
                if i in self.hash_h2l:
                    l_tmp.append(self.hash_h2l[i])
                else:
                    l_tmp.append([])
            
            tmp = np.array(l_tmp)
            elem_new = reduce(np.intersect1d, tmp)
#            print tmp, elem_new, l_elem
            if elem_new.shape[0] > 0:
                for new in elem_new:
                    l_new = list(l_elem) + list([new])
#                    print sorted(l_new), l_elem, new
                    l_out.append(sorted(l_new))
        
        if len(l_out) > 0:
            l_out = np.array(l_out)
            b = np.ascontiguousarray(l_out).view(np.dtype((np.void, l_out.dtype.itemsize * l_out.shape[1])))
            _, idx = np.unique(b, return_index=True)

        return np.array(l_out)


    def __f(self, l_elem):
        out = []
        l_tmp = []
        for i in l_elem:
            if i in self.hash_h2l:
                l_tmp.append(self.hash_h2l[i])
            else:
                l_tmp.append([])
        
        tmp = np.array(l_tmp)
        elem_new = reduce(np.intersect1d, tmp)
#        print tmp, elem_new, l_elem
        if elem_new.shape[0] > 0:
            for new in elem_new:
                l_new = list(l_elem) + list([new])
                out = sorted(l_new)
#                print sorted(l_new), l_elem, new

        return out
        

    def __next_stat2(self):
        
        l_out = map( self.__f, self.hash_stat )
        l_out = filter(len, l_out)
        return np.array(l_out)




    
    def __cal_mis(self, seq1, seq2):
        """same length, Manhattan distance"""
        dist = 0
        for i in xrange(len(seq1)):
            if seq1[i] != seq2[i]:
                dist += 1
        
        return dist

    def __cal_sum(self, mat, idx):
        return np.sum(mat.values[idx,:][:,idx])

def prepare_optparser():
    usage ="""usage: %s [options] 
    
    Using -h or --help for more information
    
Example:
    python  %s -m 4 seq.xls
    
    """ % (sys.argv[0],sys.argv[0])

    description = " Maximun subgroup with at least m mismatch for a series of sequences. "
    
    optparser = OptionParser(version="%s v0.2 20150809" % (sys.argv[0]),description=description,usage=usage,add_help_option=False)
    optparser.add_option("-m","--mismatch",  default=4    , help="\nMismatches. [default: %default]")
    optparser.add_option("-h","--help",      action="help",       help="\nShow this help message and exit.")
    return optparser
    

def main():
    prepare_optparser()
    (options, args) = prepare_optparser().parse_args()
    try:
        infile      = args[0]
        mis         = int(options.mismatch)
        
    except IndexError:
        prepare_optparser().print_help()
        sys.exit(1)
    
    m_mis = MaxSubGroup(mis, infile)
    m_mis.load_file()
    m_mis.cal_mis_mat()
    m_mis.output_mat()
    
if __name__ == '__main__':
    main()