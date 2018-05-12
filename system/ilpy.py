#inline python parser
import os
import time
import string
import random
StartTag = False   #encountered a start tag
code = ""  #received code
output = ""  #final output
tempFileName = None  #name for the temp file
idCode = None
idCodes = []

def work(line,arguments):
    global StartTag,code,output,idCode
    if line.lstrip()[:4] == "<?py":  #if the line is a start tag
        StartTag = True  #found a start tag
        addBreaker()
        return  #stop further execution
    if line.lstrip()[:2] == "?>":  #if the line is an end tag
        #runCode(arguments)  #execute the collected code
        output = output + "ilpy" + idCode
        StartTag = False  #remove the start tag
        return
    code = code + line  #if it isnt a start or end tag, place the line to the final code to run

def id(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def addBreaker():
    global code,idCode
    idCode = id(size=100)
    idCodes.append(idCode)
    injection = """\

ilpySegmentCode = '""" + idCode + """'

"""
    code = code + injection


def runCode(arguments):
    global code,output, tempFileName
    tempFileName = int(round(time.time() * 1000))  #make a temp file name
    injectionCode = """\
ilpyCurrentSegment = ""
def void(*args, **kwargs):
    return
def output(text,*args, **kwargs):
    global ilpyCurrentSegment,ilpySegmentCode
    file = open('""" + str(tempFileName) + """.ilpytemp',"a")
    if ilpyCurrentSegment != ilpySegmentCode and ilpyCurrentSegment != "":
        file.write(ilpyCurrentSegment)
        ilpyCurrentSegment = ""
    if ilpyCurrentSegment == "":
        ilpyCurrentSegment = ilpySegmentCode
    if not ilpySegmentCode == "end":
        file.write(str(text) + "\\n")
    file.close()
input = void
print = output

"""  #code to inject to collect the output
    code = injectionCode + code  #add it to the code
    try:
        file = open(str(tempFileName) + ".ilpytemp","w+")  #make a temp file
        file.close()
        exec(code,arguments)  #run the code with the arguments from the server
    except Exception as e:
        file = open(str(tempFileName) + ".ilpytemp","a")  #write any errors to the temp file
        file.write(str(e) + "\n")
        file.close()
    finally:
        file = open(str(tempFileName) + ".ilpytemp", "r")  #read the temp file
        result = file.read()
        for id in idCodes:
            codeOutput = result.split(id)[0]
            output = output.replace("ilpy"+id,codeOutput)
            result = result.replace(codeOutput + id,"")
        file.close()

def run(runFile,arguments):
    global StartTag,output,code,tempFileName
    file = open(runFile, "r")  #open the requested ilpy file
    for line in file.readlines():  #read every line
        if line.lstrip()[:4] == "<?py" or (line.lstrip()[:2] == "?>" and StartTag ) or StartTag:  #if it is a start tag, end tag, or it already encountered a start tag
            work(line,arguments)  #analyise the line
        else:  #the line contains no code
            output = output + line  #write the line to the final output
    file.close()
    code = code + "\n\n\nilpySegmentCode = 'end'\noutput('')"
    runCode(arguments)
    outputTemp = output  #store the output in a temp var
    output = ""  #clear all the variables
    code = ""
    StartTag = False
    try:
        os.remove(str(tempFileName) + ".ilpytemp")  #remove the temp file
    finally:
        return outputTemp  #return the final output