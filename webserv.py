import sys
import socket
import os
from readConfig import readConfig
from parseRequest import parseRequest
from getIncludedFiles import get_included_files
from send404 import send404

content_types = {"txt":"text/plain","html":"text/html","js":"application/javascript","css":"text/css","png":"image/png",
                 "jpeg":"image/jpeg","xml":"text/xml"}


def main():
  HOST = "127.0.0.1"
  newenv = {}

  # Check the config file has been provided, then read it in and chech the read was successful
  try:
    config = readConfig(sys.argv[1])

  except IndexError:
    print("Missing Configuration Argument",file=sys.stdout)
    config = False

  if config == False:
    sys.exit()

  # Take invertory of all files (recusively) inside the static files and cgi bin directories
  static_files = get_included_files(config["staticfiles"])
  cgi_files = get_included_files(config["cgibin"])

  # Create and connect the socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
  sock.bind((HOST, config["port"]))


  while True:
    # Wait for a connection
    sock.listen()

    # store information about the connection made
    connection, address = sock.accept()

    # forking allows the sending back of data to be done separately, 
    # so as not to delay the server from receiving new connections.
    process_id = os.fork()

    if process_id == 0:
      #In the child, store environmanet variables, check for ststic/cgi response 
      
      # Store info about the connection to pass as env variables
      newenv["REMOTE_ADDR"] = connection.getsockname()[0]
      newenv["REMOTE_PORT"] = str(connection.getsockname()[1])
      newenv["SERVER_ADDR"] = "127.0.0.1"
      newenv["SERVER_PORT"] = str(config["port"])

      request = connection.recv(1024)
      env = parseRequest(request, newenv)
      newenv.update(env)


      # Check if the request is a cgi request
      if env['REQUEST_URI'].startswith("/cgibin/"):

        # Create a pipe
        read_end, write_end = os.pipe()

        # Get the filename needing to be run
        fname = config["cgibin"] + env['REQUEST_URI'][len("cgibin/"):]
        if "?" in fname:
          fname = fname.split("?")[0]
        
        # If there is a query string, the filename needs to be isolated from it.
        if fname not in cgi_files:
          send404(connection, env)

        else:
          # Get the absolute path, fork and exec
          fpath = os.path.abspath(fname)
          retVal = os.fork()
          if retVal == 0:
            try:
              # redirect from stdout to the pipe
              os.dup2(write_end, 1)
              os.execle(config["exec"],config["exec"], fpath, newenv)

            except Exception as e:
              send404(connection,env)
            
            connection.close()
          else:
            # In the parent, wait for a signal, then send the contents of the pipe to the client.
            code = os.wait()
            bytes_from_pipe = os.read(read_end, 1024).decode()

            # If the output doesn't have a status but does have a content type, the status must be added, with one newline
            if not bytes_from_pipe.startswith("HTTP") and "Content-Type" in bytes_from_pipe:
              connection.send((env["PROTOCOL"]+" 200 OK\r\n").encode())

            # If neither are included, the status code must be added with two newlines
            elif not bytes_from_pipe.startswith("HTTP"):
              connection.send((env["PROTOCOL"]+" 200 OK\r\n\r\n").encode())
            
            connection.send(bytes_from_pipe.encode())

      else:
      # Static files  
        # If no filename  is given, load index.html
        if env['REQUEST_URI'] == "/":
          fname = config["staticfiles"] + "/index.html"
        else:
          fname = config["staticfiles"] + env['REQUEST_URI']

        # Get the file extension to establish the content type
        extension = fname[1:].split(".")[1]
        if extension not in content_types:
          send404(connection,env)
        ctype = content_types[extension]


        if fname not in static_files:
          send404(connection,env)

        else:
          # Send status code and content ype headers
          connection.send((env["PROTOCOL"]+" 200 OK\n").encode())
          connection.send("Content-Type: {}\n".format(ctype).encode())
          connection.send("\n".encode())

          # If an image is ebing sent, it does not need to be encoded, as it already is.
          if "image" in ctype:
            with open(fname, "rb") as f:
              connection.send(f.read())
          
          # Other media types must be encoded before sending.
          else:
            with open(fname, "r") as f:
                connection.send(f.read().encode())
        
      connection.close()
      sys.exit()

    else:
      ret = os.wait()
      connection.close()
  sock.close()


if __name__ == '__main__':
  main()


