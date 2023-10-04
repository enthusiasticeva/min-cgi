import os

def get_included_files(dirname):
  if dirname == "":
    print("Missing Field From Configuration File")
    return None

  files = []
  files_to_check = os.listdir(dirname)

  for file in files_to_check:
    try:
      os.listdir(dirname + "/" + file)
      files += get_included_files(dirname + "/" + file)

    except NotADirectoryError:
      files.append(dirname + "/" + file)

  return files