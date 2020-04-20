
import mmap

from PdfName import PdfName


def GetIndirectPdfArray(sIndirectPdfArray):
    """
    Return list of Indirect Objects
    
    Arguments:
        sIndirectPdfArray {string} -- [3 0 R 11 0 R]
    """    
    lIndObjs = []
    sIndirectPdfArray = sIndirectPdfArray.strip()
    # remove []
    sIndirectPdfArray = sIndirectPdfArray[1:-1]

    sIndirectPdfArray = sIndirectPdfArray.strip()
    # remove last 'R'
    sIndirectPdfArray = sIndirectPdfArray[:-1]

    # array of Indirect Object
    arIndObjs = sIndirectPdfArray.split('R')

    # Get Only Object Number
    for obj in arIndObjs:
        obj = obj.strip()
        arObj = obj.split()
        lIndObjs.append(int(arObj[0]))

    return lIndObjs


def GetIndirectPdfObject(sPdfObjectToSearch, sPdfObject):
    """
        Return Indirect Object

    Arguments:
        sPdfObjectToSearch {string} -- Indirect Pdf Object to search
        sPdfObject {string} -- pdf object
        
        e.g
        Root,    <<  /Root 1 0 R\n  /Size 5\n /Prev 1472 >>
        
    """        
    
        # find root object
    idx = sPdfObject.find(sPdfObjectToSearch)
    if idx == -1:
        return -1
    
    n = sPdfObject.find('R',idx+len(sPdfObjectToSearch))
    if n == -1:
        return -1

    obj_str = sPdfObject[idx+len(sPdfObjectToSearch):n]
    obj_str = obj_str.strip()
    obj_str = obj_str.split()[0]
    objNumber = int(obj_str)

    return objNumber


def GetPdfNumber(sPdfObjectToSearch, sPdfObject):
    """
        Return Indirect Object

    Arguments:
        sPdfObjectToSearch {string} -- Object to search
        sPdfObject {string} -- pdf object
        
        e.g
        Size,    <<  /Root 1 0 R\n  /Size 5\n /Prev 1472 >>
        
    """        
    
        
    idx = sPdfObject.find(sPdfObjectToSearch)
    
    if idx == -1:
        return idx

    n1 = sPdfObject.find('/',idx)
    n2 = sPdfObject.find('>>',idx)
    
    if n1 == -1:
        n = n2
    elif n2 == -1:
        n = n1
    else:    
        n = n1 if n1 < n2 else n2

    obj_str = sPdfObject[idx+len(sPdfObjectToSearch):n]    
    obj_str = obj_str.strip()
    # obj_str = obj_str.split()[0]
    objNumber = int(obj_str)

    return objNumber


def GetPdfObject(mm_pdf, nObjectOffset):
    
        """
        Return pdf object

        Arguments:
            mm_pdf {mmap} -- [description]
            nObjectOffset {int} -- object offset

        e.g
        1 0 obj\n  << /Type /Catalog\n     /Pages 2 0 R\n  >>\nendobj   
        """        
        mm_pdf.seek(nObjectOffset)
        pos = mm_pdf.tell()
        idx = mm_pdf.find(PdfName.ENDOBJ)          
        pdfObject  =  mm_pdf[pos:idx + len(PdfName.ENDOBJ)]       

        return pdfObject




    # class PdfUtils():

    #     def __init__(self, mm_pdf):
    #         self.mm_pdf = mm_pdf

    #     # def GetPdfObject(mm_pdf, nObjectOffset):
    #     def GetPdfObject(self, nObjectOffset):
    #         """
    #         Return pdf object

    #         Arguments:
    #             mm_pdf {mmap} -- [description]
    #             nObjectOffset {int} -- object offset

    #         e.g
    #         1 0 obj\n  << /Type /Catalog\n     /Pages 2 0 R\n  >>\nendobj   
    #         """        
    #         pass
            
    #         # mm_pdf.seek(nObjectOffset)
    #         # pos = mm_pdf.tell()
    #         # idx = mm_pdf.find(PdfName.ENDOBJ)          
    #         # pdfObject  =  mm_pdf[pos:idx + len(PdfName.ENDOBJ)]       

    #         # return pdfObject


   