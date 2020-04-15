
import mmap
import PdfName

class XrefParser():


    PdfObjects_Offsets = {}


    def __init__(self, mm_pdf):
        self.mm_pdf = mm_pdf


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
        
        self.mm_pdf.seek(self.xref_offset)
        xrefobj = self.mm_pdf.readline()
        # if xrefobj.strip() == b'xref':
        #     print('xref')
        # else:
        #      print('xrefStrm')

        # check xref or xref stream object
        n = xrefobj.find(PdfName.OBJ)
        if n > -1:
            print('xref')
        else:
            print('xrefStrm')



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
        line.strip()

        i = int(line[1])
        n = int(line[-1])

        while i < n:
            line = self.mm_pdf.readline()
            line.strip()
            if line[-1] == 'f':
                continue
            value = int(line[10])
            self.PdfObjects_Offsets[i] = value
            i+=1

    def  ParseTrailer(self):
        """
        Return pdf trailer 
        """                 
        pass