import sys

'''
ReadConfig Function
This function takes in a filename of a config file, and parses it into a dictionary which it then returns.
Parameters: String filename
Returns: False if the file was unable to be parsed
         Dictionary if the file was able to be parsed
'''
def readConfig(filename):
  # Gets the contents from the file (and checks it exists)
  try:
    with open(filename, "r") as f:
      fileLines = f.readlines()
  except FileNotFoundError:
    print("Unable To Load Configuration File.",file=sys.stdout)
    return False

  # As the configuration can be in any order, each line is split by "=", then compared to the config fields required.
  for line in fileLines:
    line_parts = line.strip().split("=")

    # If there aren't two fields once split, we know thw config file was improperly formatted.
    try:
      field = line_parts[0]
      value = line_parts[1]
    except IndexError:
      print("Unable To Load Configuration File.",file=sys.stdout)
      return False

    if field == "staticfiles":
      static_files = value

    elif field == "cgibin":
      cgi_bin = value

    elif field == "port":
      try:
        port = int(value)
      except ValueError:
        print("Unable To Load Configuration File.",file=sys.stdout)
        return False

    elif field == "exec":
      exec_path = value

  # If not all fields were found at some point, putting them into the dictionary will cause a Name Error.
  try:
    config_info = {"staticfiles" : static_files, "cgibin" : cgi_bin, "port": port, "exec": exec_path}
  except NameError:
    print("Missing Field From Configuration File",file=sys.stdout)
    return False

  return config_info