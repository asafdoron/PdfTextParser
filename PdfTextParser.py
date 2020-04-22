import os
import mmap
import errno

from XrefParser import XrefParser
import PdfUtils
from PdfName import PdfName


class PdfTextParser():

    PdfObjects_Offsets = {}
    Pages_Objects = {}
    PageCounter = 1

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

        pagesIndObj = PdfUtils.GetIndirectPdfObject(PdfName.PAGES_STR, rootObject.decode("utf-8"))  

        nPagesOffset = self.PdfObjects_Offsets[pagesIndObj]
        PagesObject = PdfUtils.GetPdfObject(self.mm_pdf, nPagesOffset)
        print(PagesObject) 

        
        self.GetPagesList(PagesObject)
        print(self.Pages_Objects)
        print(len(self.Pages_Objects))

    def GetPagesList(self, PagesObject):
        """
        Get Pages Objects list 
        
        Arguments:
            sKidsArray {string} -- Kids [3 0 R 11 0 R]
        """        
        lkids = PdfUtils.GetIndirectPdfArray(PdfName.KIDS_STR, PagesObject.decode("utf-8"))
        print(lkids)

        npagesCount = PdfUtils.GetPdfNumber(PdfName.COUNT_STR, PagesObject.decode("utf-8"))
        print(npagesCount)

        if len(lkids) == npagesCount:
            for p in lkids:
                self.Pages_Objects[self.PageCounter] = p
                self.PageCounter += 1
            # return
        else:
            for p in lkids:
                Pages = PdfUtils.GetPdfObject(self.mm_pdf, self.PdfObjects_Offsets[p])
                # return self.GetPagesList(Pages)
                self.GetPagesList(Pages)

    def GetText(self):
        pass

    
    def GetPagesNumber(self):
        pass
    
    def GetPageText(self, nPageNum):
        pass




    def __exit__(self, *args):
        self.mm_pdf.close()
        self.pdffile.close()
        