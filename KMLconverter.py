#It can process CSV, TSV or similar file formats

import re
import math

def getFile(text):
    while True:
        fileAddress = input(text)
        try:
            file = open(fileAddress, "r")
            file.close()
            return fileAddress
        except FileNotFoundError:
            pass

def getInList(text, inputList):
    while True:
        answer = input(text)
        if answer in inputList:
            return answer

def getNumber(text, minimum, maximum):
    while True:
        try:
            answer = int(input(text))
            if answer < maximum and answer >= minimum:
                return answer
        except ValueError:
            pass

def getYesNo(text):
    while True:
        answer = input(text)
        if answer.lower()[0] == "n":
            return False
        if answer.lower()[0] in ("s", "y"):
            return True
    

fileAddress = getFile("Type the file address: ")

file = open(fileAddress, "r")
fileText = list(map(lambda x: x.replace("\n",""), file.readlines()))
file.close()

if re.search(r"(?:\.[^.]*)?$", fileAddress).group(0).lower() == ".csv":
    separator = ","
elif re.search(r"(?:\.[^.]*)?$", fileAddress).group(0).lower() == ".tsv":
    separator = "\t"
else:
    separator = input("What separator does the file use?: ")

headersPresent = getYesNo("Are there headers?: ")

if headersPresent:
    headers = re.split(separator + r" *", fileText[0])

    print("Here are the headers: " + ", ".join(headers))

    latitudeHeader = getInList("Which is your header for latitude: ", headers)
    longitudeHeader = getInList("Which is your header for longitude?: ", headers)
    altitudeHeader = getInList("Which is your header for altitude? You can leave it blank: ", headers + [""])

    rawName = input("What name do you want to give to each point? You can use its values with [header] or leave it blank: ").replace(r"\n", "<br />")
    rawDescription = input("What description do you want to give to each point? You can use its values with [header] or leave it blank: ").replace(r"\n", "<br />")

    newFile = open(re.sub(r"(?:\.[^.]*)?$", ".kml", fileAddress), "w+")

    newFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    newFile.write("\n<kml xmlns=\"http://earth.google.com/kml/2.0\">")
    newFile.write("\n\t<Document>")

    for point in fileText[1:]:
        
        if not point == "":
            splittedPoint = re.split(separator + r" *", point)
            
            newFile.write("\n\t\t<Placemark>")
            
            if not rawName == "":
                name = rawName
                
                for header in headers:
                    name = name.replace("[" + header + "]", splittedPoint[headers.index(header)])
                    
                newFile.write("\n\t\t\t<name>" + name + "</name>")
            
            if not rawDescription == "":
                description = rawDescription
                
                for header in headers:
                    description = description.replace("[" + header + "]", splittedPoint[headers.index(header)])
                    
                newFile.write("\n\t\t\t<description>" + description + "</description>")

            newFile.write("\n\t\t\t<Point>")

            if not altitudeHeader == "":
                newFile.write("\n\t\t\t\t<coordinates>" + splittedPoint[headers.index(longitudeHeader)] + "," + splittedPoint[headers.index(latitudeHeader)] + "," + splittedPoint[headers.index(altitudeHeader)] + "</coordinates>")
            else:
                newFile.write("\n\t\t\t\t<coordinates>" + splittedPoint[headers.index(longitudeHeader)] + "," + splittedPoint[headers.index(latitudeHeader)] + "," + "</coordinates>")

            newFile.write("\n\t\t\t</Point>")
            
            newFile.write("\n\t\t</Placemark>")

    newFile.write("\n\t</Document>")
    newFile.write("\n</kml>")

    newFile.close()

else:
    anyLine = re.split(separator + r" *", fileText[math.floor(len(fileText)/2)])

    print("Here you have a line: " + ", ".join(anyLine))

    latitudeIndex = getNumber("Which is the column number for latitude? Start to count from 1: ", 1, len(anyLine)) - 1
    longitudeIndex = getNumber("Which is the column number for longitude? Start to count from 1: ", 1, len(anyLine)) - 1
    altitudeIndex = getNumber("Which is the column number for altitude? Start to count from 1 and type 0 to leave it blank: ", 0, len(anyLine)) - 1

    rawName = input("What name do you want to give to each point? You can use its values with [column] or leave it blank: ").replace(r"\n", "<br />")
    rawDescription = input("What description do you want to give to each point? You can use its values with [column] or leave it blank: ").replace(r"\n", "<br />")

    newFile = open(re.sub(r"(?:\.[^.]*)?$", ".kml", fileAddress), "w+")

    newFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    newFile.write("\n<kml xmlns=\"http://earth.google.com/kml/2.0\">")
    newFile.write("\n\t<Document>")

    for point in fileText:
        
        if not point == "":
            splittedPoint = re.split(separator + r" *", point)
            
            newFile.write("\n\t\t<Placemark>")
            
            if not rawName == "":
                name = rawName
                
                for i in range(len(anyLine)):
                    name = name.replace("[" + str(i+1) + "]", splittedPoint[i])
                    
                newFile.write("\n\t\t\t<name>" + name + "</name>")
            
            if not rawDescription == "":
                description = rawDescription
                
                for i in range(len(anyLine)):
                    description = description.replace("[" + str(i+1) + "]", splittedPoint[i])
                    
                newFile.write("\n\t\t\t<description>" + description + "</description>")

            newFile.write("\n\t\t\t<Point>")

            if not altitudeIndex == -1:
                newFile.write("\n\t\t\t\t<coordinates>" + splittedPoint[longitudeIndex] + "," + splittedPoint[latitudeIndex] + "," + splittedPoint[altitudeIndex] + "</coordinates>")
            else:
                newFile.write("\n\t\t\t\t<coordinates>" + splittedPoint[longitudeIndex] + "," + splittedPoint[latitudeIndex] + "," + "</coordinates>")

            newFile.write("\n\t\t\t</Point>")
            
            newFile.write("\n\t\t</Placemark>")

    newFile.write("\n\t</Document>")
    newFile.write("\n</kml>")

    newFile.close()
