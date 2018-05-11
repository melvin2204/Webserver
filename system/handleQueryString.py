import urllib.parse
def parse(query):
    query = urllib.parse.unquote(query)#decode ascii
    output = {}#output variable
    if "&" in query:#if there is more than one get item
        queries = query.split("&")#split all items
        for query in queries:
            if "=" in query:#if the key has a value
                key = query.split("=")[0]#get the key
                value = query.split("=")[1]#get the value
            else:#the key has no value
                key = query#get the key
                value = ""#give it an empty value
            output[key] = value#write it to the output dictonary
    else:#there is only one item
        if "=" in query:#if the key has a value
            key = query.split("=")[0]#get the key
            value = query.split("=")[1]#get the value
        else:#the key has no value
            key = query#get the key
            value = ""#give it an empty value
        output[key] = value#write it to the output dictonary
    return output#return the dictonary with all the GET items