# IMPORTANT: this program has been formatted so that it works specifically for UW LaCrosse transcripts.
# OTHER COLLEGE TRANSCRIPTS MAY BREAK THIS CODE because of their formatting. 
#
# The purpose of this simple program is to allow students to figure out
# what GPA they need in the future in order to maintain their goal GPA
# i.e. I can use this to see what GPA I need next semester to maintain a 3.5 GPA
# All that you need to do is input your unofficial transcript and goal GPA
# and the program will figure out the rest
#
# By: a-wille
# May 26th, 2020
#
#running from terminal, these are what the args should be
#arg[0] = program name
#arg[1] = transcript pdf
#arg[2] = goal gpa

import PyPDF2
import sys
import os
import string
import datetime


class term:
    termfinished = False
    startindex = 0
    endindex = 0
    gpa = 0.0
    credits = 0.0

    #method that finds start, end, and end date for each term
    #based on when open ( chars are found in the rest of the document
    def __init__(self, startingindex, ogfilelist, accessdate):
        self.startindex = startingindex
        termdatecheck(self, startingindex, ogfilelist, accessdate)        

def main():
    global desiredgpa
    desiredgpa = sys.argv[2]
    transcript = sys.argv[1]

    #error handling
    if os.path.exists(transcript) == False:
       print("Sorry, couldn't find the transcript.")
       print("Make sure that your transcript is in the same folder you run the program from.")
    dgpa = float(desiredgpa)
    if dgpa < 0.0 or dgpa > 4.0:
        print("Sorry, that's not a valid GPA.")
        print("Please enter a GPA between 0.0 and 4.0")
    
    convertpdftotext()
    parsedatafromtextfile('output.txt')
    calculategpaneeded()
    printresults()

def convertpdftotext():
#openPDF file and read, open output file
    pdfFileObj = open(sys.argv[1], 'rb')
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

#method that gets data necessary to calculate desired grades from transcript
def parsedatafromtextfile(textfile):
    #opening and reading old file to get header info
    global creditsyetearned
    global lastcompletedtermindex
    texttranscriptfile = open(textfile, 'r+')
    lines = texttranscriptfile.readlines()
    ogfilelines = assignlines(lines)
    beginindex = fixheaderinfo(ogfilelines)
    
    #creating term objects
    termlist = []
    listcounter = 0
    #loop that parses out lines for each term based on parenthesis
    #found that are followed by term dates
    for counter in range(beginindex, len(ogfilelines)):
        index = ogfilelines[counter].find("(")
        if "(" in ogfilelines[counter] and ogfilelines[counter][index+1].isdigit() == True:
            termlist.append(term(counter+1, ogfilelines, date))
            if listcounter != 0:
                termlist[listcounter - 1].endindex = counter
            listcounter += 1
    lastcompletedtermindex = 0
    newcounter = 1
    while lastcompletedtermindex == 0:
        if termlist[newcounter].termfinished == False:
            lastcompletedtermindex = newcounter
        newcounter += 1
    for c in range(newcounter-1, len(termlist)):
        parseGPA(termlist[c], ogfilelines)
        lastcompletedterm = newcounter - 2

    parsecumGPA(termlist[lastcompletedterm], ogfilelines)
    creditsyetearned = getcreditsyetearned(termlist)

#simple function to assign each line in the file to an index in an array for later use           
def assignlines(originalfilelines):
    counter = 0
    global ogfilelines
    ogfilelines = ["" for x in range(len(originalfilelines))]
    for line in originalfilelines:
        ogfilelines[counter] = line
        counter += 1
    return ogfilelines

def fixheaderinfo(ogfilelines):
    global name
    name = ""
    global date
    foundtitle = 0
    foundid = 0
    begin = 0
    counter = 1
    while begin == 0:
        if "Name:" in ogfilelines[counter] and foundtitle == 0:
            breakpoint = ogfilelines[counter].find("Name:")
            foundtitle = counter
        if "Student" in ogfilelines[counter] and foundid == 0:
            for newcheckpoint in range(foundtitle+1, counter):
                if ogfilelines[newcheckpoint].strip() != "":
                    name += ogfilelines[newcheckpoint].strip()
            breakpoint = ogfilelines[counter].find("Student")
            name += " " + ogfilelines[counter][:breakpoint]
            foundid = 1
        if "Date:" in ogfilelines[counter]:
            date = ogfilelines[counter + 1].strip()
        if "Beginning" in ogfilelines[counter]:
            begin = counter
        counter += 1
    return begin

#find and parse out GPA and credits of a term
def parseGPA(self, ogfilelist):
    foundGPA = 0
    counter = self.startindex
    while foundGPA == 0:
        if "Term" in ogfilelist[counter] and "GPA" in ogfilelist[counter+1]:
            foundGPA = 1
        counter += 1
    gpastring = ogfilelist[counter+1]
    gpas = gpastring[:5]
    self.gpa = float(gpas)
    gpastring = gpastring[5:]
    indexlist = gpastring.index('.')
    creditsattempted = int(gpastring[:indexlist])
    self.credits = creditsattempted

#method to parse out cumulative GPA from transcript
def parsecumGPA(self, ogfilelist):
    foundGPA = 0
    global cumulativegpa
    global creditearned
    global pointsearned
    counter = self.startindex
    while foundGPA == 0:
        if "Cum" in ogfilelist[counter] and "GPA" in ogfilelist[counter+1]:
            foundGPA = 1
        counter += 1
    s = ogfilelist[counter+1][:5]
    cumulativegpa = float(s)
    indexlist = [i for i, ltr in enumerate(ogfilelist[counter + 1]) if ltr == '.']
    for a in range(0, len(indexlist)):
        indexlist[a] = indexlist[a]+4
        if a == 0:
            cumulativegpa = ogfilelist[counter+1][:indexlist[a]]
        if a == 2:
            creditearned = float(ogfilelist[counter+1][indexlist[a-1]:indexlist[a]])
        if a == 4:
            pointsearned = ogfilelist[counter+1][indexlist[a-1]:indexlist[a]]

#find total number of credits earned in a term
def getcreditsyetearned(termlist):
    credits = 0
    for counter in range(0, len(termlist)):
        if termlist[counter].termfinished == False:
            credits += termlist[counter].credits
    return credits



#quick method to split a string of a date and return values for the month, day and year
def splitdates(stringdate):
    datelist = stringdate.split('/')
    month = int(datelist[0])
    day = int(datelist[1])
    year = int(datelist[2])
    return month, day, year

#check if the term has finished or not
def termdatecheck(self, startingindex, ogfilelist, accessdate):
        #splitting string by losing bracket and splitting at '/' to get month date and year
        stringdate = ogfilelist[self.startindex + 1]
        index = stringdate.find(")")
        stringdate = stringdate[:index]
        month, day, year = splitdates(stringdate)
        accessmonth, accessday, accessyear = splitdates(date)

        #comparing dates to see if the term ended before the transcript was downloaded
        dateaccess = datetime.date(accessyear, accessmonth, accessday)
        datetermended = datetime.date(year, month, day)
        wasaccessdatebefore = dateaccess < datetermended
        if (wasaccessdatebefore == False):
            self.termfinished = True

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
    
#find both highest possible gpa if all A's in next credits
#and find the gpa needed based on goal GPA given
def calculategpaneeded():
    global gpaneeded
    global highestgpapossible

    #calculate both possible highest gpa and gpa needed if possible
    futurepointspossible = 4.0 * float(creditsyetearned)
    highestgpapossible = (futurepointspossible + float(pointsearned))/(float(creditearned) + float(creditsyetearned))
    futurepointsearned = (float(desiredgpa)*(float(creditearned) + float(creditsyetearned)) - float(pointsearned))
    gpaneeded = futurepointsearned/creditsyetearned

# i feel like this method is pretty self explanatory, just printing the calculated results in case you were confused. 
def printresults():
    checknamestring()
    if gpaneeded > 4.0:
        highestpossiblegpa = highestgpapossible
        high = str(highestpossiblegpa)
        high = high[:4]
        print("I'm sorry, " + updatedname + "that GPA is not possible given the current number of credits scheduled.")
        print("The highest GPA you can acheive based on the credits you are taking is " + high)
    else:
        gpaneededstring = str(gpaneeded)
        gpaneededstring = gpaneededstring[:4]
        print(updatedname + "to maintain a " + desiredgpa + " GPA you need to earn a GPA of " + gpaneededstring + " over the next " + str(creditsyetearned) + " credits you have scheduled already.")

#make sure name has proper spacing
def checknamestring():
    global updatedname
    updatedname = ""
    for a in range(0, len(name)):
        updatedname += name[a]
        if name[a].islower() and a <len(name)-1 and name[a+1].isupper():
            updatedname += " "

main()
