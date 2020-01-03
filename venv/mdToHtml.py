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

def mdToHtml(content):
    TITLE_REGEX = re.compile("^[#].* ")
    INLINE_LINK_REGEX = re.compile("\[[가-힣A-Za-z].*\]")
    HREF_REGEX = re.compile("http://[가-힣A-Za-z].*[A-Za-z]")
    LINK_INFO_REGEX = re.compile("\[[가-힣A-Za-z].\]")
    ORDERED_LIST_REGEX = re.compile("^[0-9]*[.]")
    UNORDERED_LIST_REGEX = re.compile("^[-]")
    TILD_REGEX = re.compile("\*.*\*")
    BOLD_REGEX = re.compile("\*\*.*\*\*")
    

    tree = {}
    
    for line in content:


        # parse inline link
        g = INLINE_LINK_REGEX.search(line)

        if type(g) != type(None):
            info = LINK_INFO_REGEX.search(g.group())
            link = HREF_REGEX.search(g.group())
            line = line.replace(g.group(), '<a href="{}">{}</a>'.format(link.group(), info.group()[1:-1]))
        
        g = BOLD_REGEX.search(line)

        if type(g) != type(None):
            repl = "<strong>" + g.group()[2:-2] + "</strong>"
            line = line.replace(g.group(), repl)
            
        g = TILD_REGEX.search(line)

        if type(g) != type(None):
            repl = "<em>" + g.group()[2:-2] + "</em>"
            line = line.replace(g.group(), repl)
        
        
        print(line)
        g = TITLE_REGEX.search(line.lstrip())

        # parse headings
        if type(g) != type(None):
            processed = to_heading(line, g)
            print(processed)
            continue
            
            
        g = ORDERED_LIST_REGEX.search(line)
        if type(g) != type(None):
            line = line.replace(g.group(), "<ol>").lstrip() + "</ol>"
            print(line)
            continue
            
        g = UNORDERED_LIST_REGEX.search(line)

        if type(g) != type(None):
            line = line.replace(g.group(), "<li>").lstrip() + "</li>"
            print(line)
            continue


