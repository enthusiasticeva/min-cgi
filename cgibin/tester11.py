import os
print("<p>{}</p>".format(os.environ["QUERY_STRING"]))
print("<p>{}</p>".format(os.environ["REMOTE_PORT"]))
print("<p>{}</p>".format(os.environ["SERVER_ADDR"]))
print("<p>{}</p>".format(os.environ["REQUEST_METHOD"]))
print("<p>{}</p>".format(os.environ["REQUEST_URI"]))
print("<p>{}</p>".format(os.environ["HTTP_USER_AGENT"]))
print("<p>{}</p>".format(os.environ["HTTP_ACCEPT"]))
