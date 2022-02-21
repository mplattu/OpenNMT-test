#!/usr/bin/python3

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

import tempfile
import os
import re

class PDFProcessor:
    def __init__ (self, pdf_filename, txt_filename):
        self.tempfile_path = None
        self.data = None

        print("--- %s to %s" % (pdf_filename, txt_filename))

        print("    Converting PDF to text")
        self.pdf_to_temp(pdf_filename)

        print("    Formatting text")
        self.temp_to_text(txt_filename)
        
        self.close()

    def pdf_to_temp (self, pdf_filename):
        tempfile_handle, self.tempfile_path = tempfile.mkstemp()
        f_temp = os.fdopen(tempfile_handle, "wb")

        rsrcmgr = PDFResourceManager(caching=False)
        device = TextConverter(rsrcmgr, f_temp, laparams=LAParams(), imagewriter=None)

        with open(pdf_filename, 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            #for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=False, check_extractable=True):
            for page in PDFPage.get_pages(fp, set()):
                interpreter.process_page(page)
        device.close()

        f_temp.close()

    def clean_one_line(self, line):
        # Remove •, FF, CR, LF
        line = re.sub(r'[\x95\x0C\n\x0A]', '', line)

        # Multiple dots into one
        line = re.sub(r'\.\.+', '.', line)

        # Multiple spaces and tabs into one
        line = re.sub(r'[ \t]+', ' ', line)

        # Remove leading spaces
        line = re.sub(r'^\s+', '', line)

        # Remove line with numbers, dots and spaces only
        line = re.sub(r'^[\s\.\d]+$', '', line)

        return line

    def readline(self):
        if self.data is None:
            if self.tempfile_path is None:
                self.pdf_to_temp()

            f = open(self.tempfile_path, 'r')
            data = ''

            line = f.readline()
            while line:
                line = self.clean_one_line(line)
                if line != '':
                    data += line
                line = f.readline()

            f.close()

            self.data = re.split(r'(?<!\smm|\sks|\(ks|\d\.\d|l\.a)\. ', data)

        if len(self.data) > 0:
            return self.data.pop(0) + '.\n'
        else:
            return None

    def temp_to_text (self, txt_filename):
        f_text = open(txt_filename, 'w')

        line = self.readline()

        while line:
            f_text.write(line)

            line = self.readline()

        f_text.close()

    def close(self):
        if self.tempfile_path:
            os.unlink(self.tempfile_path)
            self.tempfile_path = None
for n in range(1, 16):
    pdfprocessor = PDFProcessor('training-material/meb-pdf/%d-fi.pdf' % n, 'training-material/meb-pdf/%d-fi.raw-txt' % n)
    pdfprocessor = PDFProcessor('training-material/meb-pdf/%d-sv.pdf' % n, 'training-material/meb-pdf/%d-sv.raw-txt' % n)
