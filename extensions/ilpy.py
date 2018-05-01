#inline python
import os
import time
StartTag = False
code = ""
output = ""
tempFileName = None

def work(line):
    global StartTag,code
    if line[:4] == "<?py":
        StartTag = True
        return
    if line[:2] == "?>":
        runCode()
        StartTag = False
        return
    code = code + line

def runCode():
    global code,output, tempFileName
    tempFileName = int(round(time.time() * 1000))
    injectionCode = """\
def void(*args, **kwargs):
    return
def output(text,*args, **kwargs):
    file = open('""" + str(tempFileName) + """.ilpytemp',"a")
    file.write(str(text) + "\\n")
    file.close()
input = void
print = output

"""
    code = injectionCode + code
    try:
        file = open(str(tempFileName) + ".ilpytemp","w+")
        file.close()
        exec(code)
    except Exception as e:
        file = open(str(tempFileName) + ".ilpytemp","a")
        file.write(str(e) + "\n")
        file.close()
    finally:
        file = open(str(tempFileName) + ".ilpytemp", "r")
        for line in file.readlines():
            output = output + line
        file.close()

def run(runFile):
    global StartTag,output,code,tempFileName
    file = open(runFile, "r")
    for line in file.readlines():
        if line[:4] == "<?py" or line[:2] == "?>" or StartTag:
            work(line)
        else:
            output = output + line
    file.close()
    outputTemp = output
    output = ""
    code = ""
    StartTag = False
    os.remove(str(tempFileName) + ".ilpytemp")
    return outputTemp