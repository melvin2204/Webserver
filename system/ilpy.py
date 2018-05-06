#inline python parser
import os
import time
StartTag = False   #encountered a start tag
code = ""  #received code
output = ""  #final output
tempFileName = None  #name for the temp file

def work(line,arguments):
    global StartTag,code
    if line[:4] == "<?py":  #if the line is a start tag
        StartTag = True  #found a start tag
        return  #stop further execution
    if line[:2] == "?>":  #if the line is an end tag
        runCode(arguments)  #execute the collected code
        StartTag = False  #remove the start tag
        return
    code = code + line  #if it isnt a start or end tag, place the line to the final code to run

def runCode(arguments):
    global code,output, tempFileName
    tempFileName = int(round(time.time() * 1000))  #make a temp file name
    injectionCode = """\
def void(*args, **kwargs):
    return
def output(text,*args, **kwargs):
    file = open('""" + str(tempFileName) + """.ilpytemp',"a")
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
        for line in file.readlines():
            output = output + line  #add the output of the temp file to the final output
        file.close()

def run(runFile,arguments):
    global StartTag,output,code,tempFileName
    file = open(runFile, "r")  #open the requested ilpy file
    for line in file.readlines():  #read every line
        if line[:4] == "<?py" or line[:2] == "?>" or StartTag:  #if it is a start tag, end tag, or it already encountered a start tag
            work(line,arguments)  #analyise the line
        else:  #the line contains no code
            output = output + line  #write the line to the final output
    file.close()
    outputTemp = output  #store the output in a temp var
    output = ""  #clear all the variables
    code = ""
    StartTag = False
    try:
        os.remove(str(tempFileName) + ".ilpytemp")  #remove the temp file
    finally:
        return outputTemp  #return the final output