
import mmap
from PdfName import PdfName

class XrefParser():


    PdfObjects_Offsets = {}
    Root_Offset = None

    # @property
    # def PdfObjects_Offsets(self):
    #     return self.__PdfObjects_Offsets

    def __init__(self, mm_pdf):
        self.mm_pdf = mm_pdf

    # def __enter__(self):
    #     return self

    def GetStartXRef(self):               
        """
        Return xref offset
        
        Returns:
            int -- xref offset
        """        
        startxref_str = PdfName.START_XREF
        eof = self.mm_pdf.rfind(PdfName.EOF) 
        startxref = self.mm_pdf.rfind(startxref_str) 
        offset =  self.mm_pdf[startxref+len(startxref_str):eof]
        self.xref_offset = int(offset.decode("utf-8").strip())
        print(self.xref_offset)
        return self.xref_offset


    def  ParseXrefTable(self):    

        self.bFoundPrevTrailer = True

        while self.bFoundPrevTrailer == True:

            self.mm_pdf.seek(self.xref_offset)
            xrefobj = self.mm_pdf.readline()
            # if xrefobj.strip() == b'xref':
            #     print('xref')
            # else:
            #      print('xrefStrm')

            # check xref or xref stream object
            idx = xrefobj.find(PdfName.OBJ)
            if idx > -1:
                print('xrefStrm')
                raise Exception('PDF Not Supported')
            else:
                print('xref')


            self.ParseSubXrefTable()
            
            # check if xref ended
            pos = self.mm_pdf.tell()
            line = self.mm_pdf.readline()
            #line = line.decode("utf-8")
            idx = line.find(PdfName.TRAILER)
            #idx = line.find('trailer')
            if idx > -1:
                #found trailer
                self.ParseTrailer()
            else:
                self.mm_pdf.seek(pos)


    def ParseSubXrefTable(self):
        """
        0 5
        0000000000 65535 f 
        0000000018 00000 n 
        0000000077 00000 n 
        0000000178 00000 n 
        0000000457 00000 n 

        """
        line = self.mm_pdf.readline()
        line = line.decode("utf-8").strip()

        i = int(line[0])
        n = int(line[-1])

        while i < n:
            line = self.mm_pdf.readline()
            line = line.decode("utf-8").strip()
            
            # deleted object - offset = 0
            if line[-1] == 'f':
                value = 0
            else:    
                value = int(line[:10])
            
            if i not in self.PdfObjects_Offsets:
                self.PdfObjects_Offsets[i] = value

            i+=1

    def  ParseTrailer(self):
        """
        Parse pdf trailer 
        <<  /Root 1 0 R\n  /Size 5\n /Prev 1472 >>
        """                 
        pos = self.mm_pdf.tell()
        idx = self.mm_pdf.find(PdfName.GREATER_THAN) 
        trailer = self.mm_pdf[pos:idx+2]

        # find prev xref offset
        idx = trailer.find(PdfName.PREV)
            #idx = line.find('trailer')
        if idx > -1:
            self.bFoundPrevTrailer = True
            n1 = trailer.find(b'/',idx)
            n2 = trailer.find(PdfName.GREATER_THAN,idx)
            
            if n1 == -1:
                n = n2
            elif n2 == -1:
                n = n1
            else:    
                n = n1 if n1 < n2 else n2

        else:
            self.bFoundPrevTrailer = False


        # find root object
        idx = trailer.find(PdfName.ROOT)
        
        n = trailer.find(b'R',idx+len(PdfName.ROOT))
        
        root_str = trailer[idx+len(PdfName.ROOT):n]
        root_str = root_str.split()[0]
        self.Root_Offset = int(root_str)