import os
import mmap
import errno
from XrefParser import XrefParser


class PdfTextParser():



    def __init__(self, pdffilename):
        """ 
        
        Arguments:
            pdffilename {[string]} -- path to pdf file
        """         
        self.pdffilename = pdffilename;
        
    def __enter__(self):
        """
        open pdf file, init mmap

        Raises:
            FileNotFoundError: if pdf file not found
        
        Returns:
            PdfTextParser

        """        
        
        if not os.path.exists(self.pdffilename):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), pdffilename)

        self.pdffile = open(self.pdffilename, 'r+b')
        self.mm_pdf = mmap.mmap(self.pdffile.fileno(), 0)
        print(self.mm_pdf.readline())
        self.xrefparser = XrefParser(self.mm_pdf)     
        return self


    def Parse(self):
       
       self.xrefparser.GetStartXRef()
       self.xrefparser.ParseXrefTable()
 

    def __exit__(self, *args):
        self.mm_pdf.close()
        self.pdffile.close()
        