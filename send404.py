def send404(connection, headers):
  connection.send((headers["PROTOCOL"]+" 404 File not found\n").encode())
  connection.send("Content-Type: text/html\n".encode())
  connection.send("\n".encode())
  connection.send('''<html>
<head>
\t<title>404 Not Found</title>
</head>
<body bgcolor="white">
<center>
\t<h1>404 Not Found</h1>
</center>
</body>
</html>\n'''.encode())