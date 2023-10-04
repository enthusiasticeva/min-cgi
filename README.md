# MinCGI
In this project, I built a web server that could handle multiple connections and execute applications that are compliant with a subset of the Common Gateway Interface specification

The server accepts HTTP requests through a port specified in [config.cfg](/config.cfg)

It can load files (stored in the files folder), including HTML/JS/CSS web pages, python files, javascript files etc.
It can also execute python files, if the `/cgibin` route is specified.

## How to run
- To run the server, run `python3 ./webserv.py ./config.cfg &`
- Now, your web server is running in the background (note, make sure to kill the process after you are done.)
- To interact with the web server, use `curl`, here are some examples
  - `curl 127.0.0.1:8070/`
  - `curl 127.0.0.1:8070/index.html`
  - `curl 127.0.0.1:8070/greetings.html`
  - `curl 127.0.0.1:8070/cgibin/tester8.py`
  - `curl 127.0.0.1:8070/cgibin/tester9.py`
  - `curl 127.0.0.1:8070/cgibin/tester10.py`
  - `curl "127.0.0.1:8070/cgibin/tester11.py?name=Adam&age=18"`


- You can also interact with the server by entering the URIs into your browser. Note however that an error MAY occur if your browser makes any extra requests (trying to get a favicon etc.)


## Tests
- Tests are located in the [myTests](/mytests/) folder, and an explantation of what each one is testing is [here](/Tests.md).
- To run the tests, use `sh runTests.sh`