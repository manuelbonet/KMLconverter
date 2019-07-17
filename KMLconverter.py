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

def getInList(text, inputList, ignoreCase = False):
    if ignoreCase:
        while True:
            answer = input(text)
            if answer.lower() in list(map(lambda x: x.lower(), inputList)):
                return answer.lower()
    else:
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

if headersPresent:  #There are headers
    headers = re.split(separator + r" *", fileText[0])

    print("Here are the headers: " + ", ".join(headers))

    latitudeHeader = getInList("Which is your header for latitude: ", headers)
    longitudeHeader = getInList("Which is your header for longitude?: ", headers)
    altitudeHeader = getInList("Which is your header for altitude? You can leave it blank: ", headers + [""])

    if not altitudeHeader == "":
        altitudeMode = getInList("Is the altitude relative to [sea] level or to [ground]?: ", ("sea", "ground"), ignoreCase = True)
        extrude = getYesNo("Would you like to extrude the shape?: ")

    pointsOrLine = getInList("Would you like to get [points] or a [line]?: ", ("points", "line"), ignoreCase = True)

    if pointsOrLine == "points":    #There are points with headers
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
                    if extrude:
                        newFile.write("\n\t\t\t\t<extrude>1</extrude>")
                    else:
                        newFile.write("\n\t\t\t\t<extrude>0</extrude>")

                    if altitudeMode == "sea":
                        newFile.write("\n\t\t\t\t<altitudeMode>absolute</altitudeMode>")
                    else:
                        newFile.write("\n\t\t\t\t<altitudeMode>relativeToGround</altitudeMode>")

                if not altitudeHeader == "":
                    newFile.write("\n\t\t\t\t<coordinates>" + splittedPoint[headers.index(longitudeHeader)] + "," + splittedPoint[headers.index(latitudeHeader)] + "," + splittedPoint[headers.index(altitudeHeader)] + "</coordinates>")
                else:
                    newFile.write("\n\t\t\t\t<coordinates>" + splittedPoint[headers.index(longitudeHeader)] + "," + splittedPoint[headers.index(latitudeHeader)] + "</coordinates>")

                newFile.write("\n\t\t\t</Point>")
                
                newFile.write("\n\t\t</Placemark>")

        newFile.write("\n\t</Document>")
        newFile.write("\n</kml>")

        newFile.close()
        
    else:   #It's a LineString with headers
        
        newFile = open(re.sub(r"(?:\.[^.]*)?$", ".kml", fileAddress), "w+")

        newFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
        newFile.write("\n<kml xmlns=\"http://earth.google.com/kml/2.0\">")
        newFile.write("\n\t<Document>")
        newFile.write("\n\t\t<Placemark>")
        newFile.write("\n\t\t\t<Style><PolyStyle><color>7fffffff</color><colorMode>normal</colorMode><fill>1</fill></PolyStyle></Style>")
        newFile.write("\n\t\t\t<LineString>")

        
        if altitudeHeader == "":
            newFile.write("\n\t\t\t\t<altitudeMode>clampToGround</altitudeMode>")
        else:
            if extrude:
                newFile.write("\n\t\t\t\t<extrude>1</extrude>")
            else:
                newFile.write("\n\t\t\t\t<extrude>0</extrude>")

            if altitudeMode == "sea":
                newFile.write("\n\t\t\t\t<altitudeMode>absolute</altitudeMode>")
            else:
                newFile.write("\n\t\t\t\t<altitudeMode>relativeToGround</altitudeMode>")
        
        
        newFile.write("\n\t\t\t\t<coordinates>")

        for point in fileText[1:]:
            splittedPoint = re.split(separator + r" *", point)
            
            if not point == "":
                if not altitudeHeader == "":
                    newFile.write("\n\t\t\t\t\t" + splittedPoint[headers.index(longitudeHeader)] + "," + splittedPoint[headers.index(latitudeHeader)] + "," + splittedPoint[headers.index(altitudeHeader)])
                else:
                    newFile.write("\n\t\t\t\t\t" + splittedPoint[headers.index(longitudeHeader)] + "," + splittedPoint[headers.index(latitudeHeader)])

        newFile.write("\n\t\t\t\t</coordinates>")
        newFile.write("\n\t\t\t</LineString>")
        newFile.write("\n\t\t</Placemark>")
        newFile.write("\n\t</Document>")
        newFile.write("\n</kml>")

        newFile.close()  

else: #There are NOT headers
    anyLine = re.split(separator + r" *", fileText[math.floor(len(fileText)/2)])

    print("Here you have a line: " + ", ".join(anyLine))

    latitudeIndex = getNumber("Which is the column number for latitude? Start to count from 1: ", 1, len(anyLine)) - 1
    longitudeIndex = getNumber("Which is the column number for longitude? Start to count from 1: ", 1, len(anyLine)) - 1
    altitudeIndex = getNumber("Which is the column number for altitude? Start to count from 1 and type 0 to leave it blank: ", 0, len(anyLine)) - 1
    
    if not altitudeIndex == -1:
        altitudeMode = getInList("Is the altitude relative to [sea] level or to [ground]?: ", ("sea", "ground"), ignoreCase = True)
        extrude = getYesNo("Would you like to extrude shape?: ")

    pointsOrLine = getInList("Would you like to get [points] or a [line]?: ", ("points", "line"), ignoreCase = True)

    if pointsOrLine == "points":    #There are points without headers
        rawName = input("What name do you want to give to each point? You can use its values with [column] or leave it blank: ").replace(r"\n", "<br />")
        rawDescription = input("What description do you want to give to each point? You can use its values with [column] or leave it blank: ").replace(r"\n", "<br />")
        
        newFile = open(re.sub(r"(?:\.[^.]*)?$", ".kml", fileAddress), "w+")

        newFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
        newFile.write("\n<kml xmlns=\"http://www.opengis.net/kml/2.2\">")
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
                    if extrude:
                        newFile.write("\n\t\t\t\t<extrude>1</extrude>")
                    else:
                        newFile.write("\n\t\t\t\t<extrude>0</extrude>")

                    if altitudeMode == "sea":
                        newFile.write("\n\t\t\t\t<altitudeMode>absolute</altitudeMode>")
                    else:
                        newFile.write("\n\t\t\t\t<altitudeMode>relativeToGround</altitudeMode>")

                if not altitudeIndex == -1:
                    newFile.write("\n\t\t\t\t<coordinates>" + splittedPoint[longitudeIndex] + "," + splittedPoint[latitudeIndex] + "," + splittedPoint[altitudeIndex] + "</coordinates>")
                else:
                    newFile.write("\n\t\t\t\t<coordinates>" + splittedPoint[longitudeIndex] + "," + splittedPoint[latitudeIndex] + "</coordinates>")

                newFile.write("\n\t\t\t</Point>")
                
                newFile.write("\n\t\t</Placemark>")

        newFile.write("\n\t</Document>")
        newFile.write("\n</kml>")

        newFile.close()
        
    else:   #It's a LineString without headers
        newFile = open(re.sub(r"(?:\.[^.]*)?$", ".kml", fileAddress), "w+")

        newFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
        newFile.write("\n<kml xmlns=\"http://earth.google.com/kml/2.0\">")
        newFile.write("\n\t<Document>")
        newFile.write("\n\t\t<Placemark>")
        newFile.write("\n\t\t\t<Style><PolyStyle><color>7fffffff</color><colorMode>normal</colorMode><fill>1</fill></PolyStyle></Style>")
        newFile.write("\n\t\t\t<LineString>")

        
        if not altitudeIndex == -1:
            if extrude:
                newFile.write("\n\t\t\t\t<extrude>1</extrude>")
            else:
                newFile.write("\n\t\t\t\t<extrude>0</extrude>")

            if altitudeMode == "sea":
                newFile.write("\n\t\t\t\t<altitudeMode>absolute</altitudeMode>")
            else:
                newFile.write("\n\t\t\t\t<altitudeMode>relativeToGround</altitudeMode>")
        
        
        newFile.write("\n\t\t\t\t<coordinates>")

        for point in fileText[1:]:
            splittedPoint = re.split(separator + r" *", point)
            
            if not point == "":
                if not altitudeIndex == -1:
                    newFile.write("\n\t\t\t\t\t" + splittedPoint[longitudeIndex] + "," + splittedPoint[latitudeIndex] + "," + splittedPoint[altitudeIndex])
                else:
                    newFile.write("\n\t\t\t\t\t" + splittedPoint[longitudeIndex] + "," + splittedPoint[latitudeIndex])

        newFile.write("\n\t\t\t\t</coordinates>")
        newFile.write("\n\t\t\t</LineString>")
        newFile.write("\n\t\t</Placemark>")
        newFile.write("\n\t</Document>")
        newFile.write("\n</kml>")

        newFile.close()  
        
