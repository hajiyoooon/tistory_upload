import os

def load_info(path):
    ret = []
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace("\n","")
            ret.append(line)
    return ret

def load_all_md(path = "\\"):
    markdowns = list()

    for currentPath, dirs, files in os.walk(path):
        for file in files:
            if file[-2:] == 'md':
                markdowns.append(currentPath+"\\"+file)

    return markdowns
    
def get_content(fpath):
    content = []
    category, title = fpath.split("\\")[-2:]
    
    with open(fpath, "r", encoding= "utf8") as f:
        content = f.readlines()
    
    return category, title, content