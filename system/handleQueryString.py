import urllib.parse
def GET(query):
    query = urllib.parse.unquote(query)
    output = {}
    if "&" in query:
        queries = query.split("&")
        for query in queries:
            if "=" in query:
                key = query.split("=")[0]
                value = query.split("=")[1]
            else:
                key = query
                value = ""
            output[key] = value
    else:
        if "=" in query:
            key = query.split("=")[0]
            value = query.split("=")[1]
        else:
            key = query
            value = ""
        output[key] = value
    return output