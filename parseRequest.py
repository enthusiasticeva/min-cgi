

'''
ParseRequest Function
This function takes in a HTTP request (in binray form) and an environment dictionary to add to.
Parameters: byte string request, dictionary newenv
Returns: 
                 Dictionary if the file was able to be parsed
'''

def parseRequest(request,newenv):
    request = request.decode()
    header = request.split("\n\n\n")[0]
    try:
        request_body = request.split("\n\n\n")[1]
    except IndexError:
        pass

    headerLines = request.split('\n')

    

    first_line = headerLines[0]

    first_line = first_line.split()
    newenv["REQUEST_METHOD"] = first_line[0]
    newenv["PROTOCOL"] = first_line[2]


    resource = first_line[1]
    newenv["REQUEST_URI"] = resource

    if "?" in resource:
        resource = resource.split("?")

        newenv["QUERY_STRING"] = resource[1]

        resource = resource[1]
        
        resource = resource.split("&")


    for line in headerLines:
        line = line.strip()

        if line.startswith("Accept: "):
            
            newenv["HTTP_ACCEPT"] = line[len("Accept: "):]

        elif line.startswith("Host: "):
            
            newenv["HTTP_HOST"] = line[len("Host: "):]

        elif line.startswith("User-Agent: "):
            
            newenv["HTTP_USER_AGENT"] = line[len("User-Agent: "):]
        
        elif line.startswith("Accept-Encoding: "):
            
            newenv["HTTP_ACCEPT_ENCODING"] = line[len("Accept-Encoding: "):]

        elif line.startswith("Content-Type: "):
            
            newenv["CONTENT_TYPE"] = line[len("Content-Type: "):]

        elif line.startswith("Content-Length: "):
            
            newenv["CONTENT_LENGTH"] = line[len("Content-Length: "):]

    return newenv
        