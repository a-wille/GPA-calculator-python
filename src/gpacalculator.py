# IMPORTANT: this program has been formatted so that it works specifically for UW LaCrosse transcripts.
# OTHER COLLEGE TRANSCRIPTS MAY BREAK THIS CODE because of their formatting. 
#
# The purpose of this simple program is to allow students to figure out
# what GPA they need in the future in order to maintain their goal GPA
# i.e. I can use this to see what GPA I need next semester to maintain a 3.5 GPA
# All that you need to do is input your unofficial transcript and goal GPA
# and the program will figure out the rest
#
# By: a-cretan
# May 26th, 2020
#
#running from terminal, these are what the args should be
#arg[0] = program name
#arg[1] = transcript pdf
#arg[2] = goal gpa

import sys
import os
from model.parsefile import parsedatafromtextfile
from model.convertpdf import convertpdftotext

def main():
    desiredgpa = sys.argv[2]
    transcript = sys.argv[1]

    #rudimentary error handling
    if os.path.exists(transcript) == False:
       print("Sorry, couldn't find the transcript.")
       print("Make sure that your transcript is in the same folder you run the program from.")
    dgpa = float(desiredgpa)
    if dgpa < 0.0 or dgpa > 4.0:
        print("Sorry, that's not a valid GPA.")
        print("Please enter a GPA between 0.0 and 4.0")
    
    convertpdftotext(transcript)
    creditsyetearned, creditearned, pointsearned, name, date = parsedatafromtextfile('output.txt')
    gpaneeded, highestgpapossible = calculategpaneeded(desiredgpa, creditsyetearned, pointsearned, creditearned)
    printresults(desiredgpa, gpaneeded, highestgpapossible, name, creditsyetearned)

#find both highest possible gpa if all A's in next credits
#and find the gpa needed based on goal GPA given
def calculategpaneeded(desiredgpa, creditsyetearned, pointsearned, creditearned):
    #calculate both possible highest gpa and gpa needed if possible
    futurepointspossible = 4.0 * float(creditsyetearned)
    highestgpapossible = (futurepointspossible + float(pointsearned))/(float(creditearned) + float(creditsyetearned))
    futurepointsearned = (float(desiredgpa)*(float(creditearned) + float(creditsyetearned)) - float(pointsearned))
    gpaneeded = futurepointsearned/creditsyetearned
    return gpaneeded, highestgpapossible

#simply print calculated values to the console in a readable format
def printresults(desiredgpa, gpaneeded, highestgpapossible, name, creditsyetearned):
    updatedname = checknamestring(name)
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
def checknamestring(name):
    updatedname = ""
    for a in range(0, len(name)):
        updatedname += name[a]
        if name[a].islower() and a <len(name)-1 and name[a+1].isupper():
            updatedname += " "
    return updatedname

main()