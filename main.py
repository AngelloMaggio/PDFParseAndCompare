# Developed by Angello Maggio
# 13th April 2017
# Some code used from the pdfminer documentation

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from difflib import SequenceMatcher


# Uses pdfminer to translate PDF to text
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()

    output.close
    return text


# Cleans text converted from pdf and writes it nicely to file
# gets rid of all non utf-8 characters
def convertPDFtoText(filename, outfile):
    out_file = open(outfile, 'w')
    text = convert(filename)
    text = text.decode('utf-8', 'ignore').encode("utf-8")
    for line in text.split('\n'):
        out_file.write(line)
        out_file.write('\n')

# Returns a percentage of similarity between two strings
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Compares two text files and returns a third one with the lines that are appear in both
# files based on a similarity ratio. Takes quadratic time.
def compare_two(file1, file2, ratio, out=None):

    if not out:
        out_file = open('out_similarity_'+str(ratio)+'.csv', 'w')
    list_one = open(file1, 'r')
    list_two = open(file2, 'r')
    count = 0

    list_one = [line.rstrip() for line in list_one.readlines() if line != '\n']
    list_two = [line.rstrip() for line in list_two.readlines() if line != '\n']

    for i in list_one:
        for j in list_two:
            sim = similar(i, j)
            if sim > ratio:
                count+=1
                print "FOUND MATCH"
                print i
                print j
                print count
                print similar(i, j)
                print "--------------"
                out_file.write(i + ',' + j + ',' + str(sim) + '\n')

    print "Total matches: ", count

# Example use, imagine we have a list of clients and a pdf of Forune 2000 companies, in which names are formatted differently
# Companies such as The Coca-Cola Company are in one list, whilst in the other they're listed as Coca-Cola
# Problem: How many of our clients are in Fortune 2000?
def main():
    # Open pdf with names of companies in Fortune 2000
    convertPDFtoText('2015Forbes2000List.pdf', 'sample_pdf_to_text.txt')
    compare_two('sample_pdf_to_text.txt', 'sample_client_list.txt', .8)






if __name__ == '__main__':
    main()