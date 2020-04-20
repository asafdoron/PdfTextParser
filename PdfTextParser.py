import os
import mmap
import errno

from XrefParser import XrefParser
import PdfUtils
# from pdfutils import *


class PdfTextParser():

    PdfObjects_Offsets = {}
    Root_Object = None

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
        # self.pdfUtils = pdfutils.PdfUtils(self.mm_pdf)     
        return self


    def ParseXref(self):
       
       self.xrefparser.GetStartXRef()
       self.xrefparser.ParseXrefTable()
 

       self.PdfObjects_Offsets = self.xrefparser.PdfObjects_Offsets
       self.nRootIndObjNumber = self.xrefparser.nRootIndObjNumber

       self.GetPdfPages()
       
    def GetPdfPages(self):
        """
        Get list of pdf pages - indirect objects 
        
        read root object
        get pages indirect object     
        get kids list
        """        
        
        nrootOffset = self.PdfObjects_Offsets[self.nRootIndObjNumber]
        rootObject = PdfUtils.GetPdfObject(self.mm_pdf, nrootOffset)
        print(rootObject)

        #pagesIndObj = PdfUtils.GetIndirectPdfObject('Pages', root)   

    def GetText(self):
        pass

    
    def GetPagesNumber(self):
        pass
    
    def GetPageText(self, nPageNum):
        pass




    def __exit__(self, *args):
        self.mm_pdf.close()
        self.pdffile.close()
        