import re

def to_heading(line, g):
    i = 0
    for ch in line.lstrip():
        if ch == '#':
            i+=1
        else:
            break

    line = line.replace(g.group(),"").lstrip()
    processed = "<h{}>{}</h{}>".format(i, line, i)
    
    return processed

def mdToHtml():
    TITLE_REGEX = re.compile("^[#].* ")
    
    tree = {}
    
    for line in content:
        g = TITLE_REGEX.search(line.lstrip())

        if type(g) != type(None):
            processed = to_heading(line, g)
