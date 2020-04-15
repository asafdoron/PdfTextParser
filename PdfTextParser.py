import os
import mmap
import errno


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
            PdfReader

        """        
        
        if not os.path.exists(self.pdffilename):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), pdffilename)

        self.pdffile = open(self.pdffilename, 'r+b')
        self.mm_pdf = mmap.mmap(self.pdffile.fileno(), 0)
        print(self.mm_pdf.readline())
        return self


    
    def GetStartXRef(self):               
        """
        Return xref offset
        
        Returns:
            int -- xref offset
        """        
        startxref_str = b'startxref'
        eof = self.mm_pdf.rfind(b'%%EOF') 
        startxref = self.mm_pdf.rfind(startxref_str) 
        offset =  self.mm_pdf[startxref+len(startxref_str):eof]
        self.xref_offset = int(offset.decode("utf-8").strip())
        print(self.xref_offset)
        return self.xref_offset

    def  GetTrailer(self):
        """
        Return pdf trailer 
        """                 
        self.mm_pdf.seek(self.xref_offset)
        xrefobj = self.mm_pdf.readline()
        # if xrefobj.strip() == b'xref':
        #     print('xref')
        # else:
        #      print('xrefStrm')

        # check xref or xref stream object
        n = xrefobj.find(b'obj')
        if n > -1:
            print('xref')
        else:
            print('xrefStrm')

    def __exit__(self, *args):
        self.mm_pdf.close()
        self.pdffile.close()
        