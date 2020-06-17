import PyPDF2

def convertpdftotext(transcript):
#openPDF file and read, open output file
    pdfFileObj = open(transcript, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pages = pdfReader.numPages
    texttranscript = open('output.txt', 'w')

    #check data in each page
    for i in range(pages):
        #store page data in a list that splits elements at spaces
        pageObj = pdfReader.getPage(i)
        text = pageObj.extractText().split(" ")
    
        #begin looping through each item in the list
        for i in range(len(text)):
            numsafterwords = 0
            wordsafternums = 0
            startpoint = 0
            lines = ["" for x in range(len(text))]
        #make sure something is stored in the list at the element
            if text[i]: 
                for a in range(len(text[i])):
                    numsafterwords = splitnums(text, numsafterwords, lines, i, a, startpoint)
                    wordsafternums = splitafternums(text, wordsafternums, lines, i, a, startpoint)
                    addspace = splitwords(text, i, a)
                    lines[i] += text[i][a]
                    if addspace:
                        lines[i] += " "

                    #change "starting point" of each line in case more than one word or number is in it
                    if numsafterwords == 1 or wordsafternums == 1:
                        startpoint = a
                        numsafterwords = 0
                        wordsafternums = 0
            texttranscript.writelines(lines[i])
            texttranscript.writelines("\n")
    texttranscript.close()
    pdfFileObj.close()

#if the first item is a char, enter the line before the number is added to it 
def splitnums(textlist, checker, linelist, indexi, indexa, start):
    if textlist[indexi][start].isalpha() == True:
        if checker == 0 and textlist[indexi][indexa].isdigit():
            linelist[indexi] += '\n'
            checker = 1
    return checker

#if the first item is a num, split after all other numbers have been listed
def splitafternums(textlist, checker, linelist, indexi, indexa, start):
    if textlist[indexi][start].isdigit() and checker == 0: 
        if textlist[indexi][indexa].isalpha() == True:
            linelist[indexi] += '\n'
            checker = 1
    return checker

#function that puts spaces between words in the pdf
def splitwords(t, ii, ia):
    #check if letter is lower case and followed by an uppercase letter
    #indicating the end of the word is after this letter
    if (ia+1) < len(t[ii]) and t[ii][ia+1] and t[ii][ia].islower():
        if t[ii][ia+1].isupper():
            #return 1 if there needs to be a space added after letter
            return 1
        else:
            return 
    