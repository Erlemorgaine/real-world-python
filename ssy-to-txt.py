import PyPDF2

# Convert a pdf book to plaintext file

pdfFileObj = open('SSY-complete.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

plaintext = ''

for page in range(pdfReader.numPages):
    pageObj = pdfReader.getPage(page)
    plaintext += pageObj.extractText() + ' '


text_file = open("./shinsekai-yori.txt", "w")
text_file.write(plaintext)
text_file.close()