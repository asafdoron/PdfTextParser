
from PdfTextParser import PdfTextParser
import os
import mmap
import traceback

def main():

    n = None
    startxref = None

    pdfbytes = b'%PDF-1.1\n%\xc2\xa5\xc2\xb1\xc3\xab\n\n1 0 obj\n  << /Type /Catalog\n     /Pages 2 0 R\n  >>\nendobj\n\n2 0 obj\n  << /Type /Pages\n     /Kids [3 0 R]\n     /Count 1\n     /MediaBox [0 0 300 144]\n  >>\nendobj\n\n3 0 obj\n  <<  /Type /Page\n      /Parent 2 0 R\n      /Resources\n       << /Font\n           << /F1\n               << /Type /Font\n                  /Subtype /Type1\n                  /BaseFont /Times-Roman\n               >>\n           >>\n       >>\n      /Contents 4 0 R\n  >>\nendobj\n\n4 0 obj\n  << /Length 55 >>\nstream\n  BT\n    /F1 18 Tf\n    0 0 Td\n    (Hello World) Tj\n  ET\nendstream\nendobj\n\nxref\n0 5\n0000000000 65535 f \n0000000018 00000 n \n0000000077 00000 n \n0000000178 00000 n \n0000000457 00000 n \ntrailer\n  <<  /Root 1 0 R\n      /Size 5\n  >>\nstartxref\n565\n%%EOF\n'
    

    # map = mmap.mmap(
    #             -1,
    #             len(pdfbytes),
    #             flags=(mmap.MAP_SHARED),
    #             prot=(mmap.PROT_READ | mmap.PROT_WRITE)
    #             )

    
    # map = mmap.mmap(
    #             -1,
    #             len(pdfbytes),
    #             access=mmap.ACCESS_READ|mmap.ACCESS_WRITE)
                

    # map.write(pdfbytes)        
    # map.seek(0)   
    # print(map.readline())

    # with open("c:/minimal.pdf", "rb") as binary_file:
    #     #  Read the whole file at once
    #     data = binary_file.read()
    #     print(data)

    # with open('c:/11.pdf', 'r') as file:
    #         n = file.fileno()
    
    with PdfTextParser('c:/minimal.pdf') as pdftextparser:
        pdftextparser.Parse()

if __name__ == "__main__":
    try:
        main()
    except Exception:
         traceback.print_exc()
    