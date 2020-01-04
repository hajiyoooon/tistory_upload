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

def get_depth(line, deli):
    i = 0
    for ch in line:
        if deli == ch:
            i+=1
        else:
            break
            
    return i
    
def mdToHtml(content, idx, depth = 0):
    # TODO : inline 코드일 경우 <> 를 &lt 같은 것으로 바꾸어주어야 함
    # TODO : 
    
    # inline element
    TITLE_REGEX = re.compile("^[#].* ")
    INLINE_LINK_REGEX = re.compile("\[[가-힣A-Za-z].*\]\(.*\)")
    HREF_REGEX = re.compile("http:\/\/[가-힣A-Za-z].*[A-Za-z]")
    LINK_INFO_REGEX = re.compile("\[[가-힣A-Za-z].\]")
    ITALIC_REGEX = re.compile("\*.*\*")
    BOLD_REGEX = re.compile("\*\*.*\*\*")
    INLINE_CODE_REGEX = re.compile("\`.*\`")
    HIGHLIGHT_REGEX = re.compile("==.*==")
    IMAGE_REGEX = re.compile("!\[.*\]\(.*\)")
    IMAGE_INFO_REGEX = re.compile("\[.*\]")
    IMAGE_URI_REGEX = re.compile("\(.*\)")

    # recursive element
    ORDERED_LIST_REGEX = re.compile("^[0-9]*[.]")
    UNORDERED_LIST_REGEX = re.compile("^[-]")
    BLOCKQUOTE_REGEX = re.compile("^>[>]* .*")

    

    tree = [] # sentence / depth / mode /
    cur_depth = depth
    
    while True:
        idx += 1
        if idx == len(content):
            break
        line = content[idx]
        # for line in content:
        line_info = []
        #line = line.replace("\n","<br/>")

        
        g = IMAGE_REGEX.search(line)

        if type(g) != type(None):
            print(IMAGE_INFO_REGEX.search(g.group()))
            info = IMAGE_INFO_REGEX.search(g.group()).group()[1:-1]
            link = IMAGE_URI_REGEX.search(g.group()).group()[1:-1]
            line = line.replace(g.group(), '<img src="{}" alt="{}">'.format(link, info))
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
            
        g = ITALIC_REGEX.search(line)

        if type(g) != type(None):
            repl = "<em>" + g.group()[1:-1] + "</em>"
            line = line.replace(g.group(), repl)
        
        g = INLINE_CODE_REGEX.search(line)

        if type(g) != type(None):
            repl = "<pre><code>" + g.group()[1:-1] + "</code></pre>"
            line = line.replace(g.group(), repl)
            
        g = HIGHLIGHT_REGEX.search(line)

        if type(g) != type(None):
            repl = "<mark>" + g.group()[2:-2] + "</mark>"
            line = line.replace(g.group(), repl)
        
        g = TITLE_REGEX.search(line.lstrip())

        # parse headings
        if type(g) != type(None):
            processed = to_heading(line, g)
            line_info.append(processed)
            tree.append(line_info)
            continue
            
            
        ## recursive elemnet
        
        # list
        g = ORDERED_LIST_REGEX.search(line)
        if type(g) != type(None):
            line = line.replace(g.group(), "<li>").lstrip() + "</li>"
            ret, idx = mdToHtml(content[idx:],-1)
            line_info.append(ret)
            tree.append(line_info)
            continue
            
        g = UNORDERED_LIST_REGEX.search(line)

        if type(g) != type(None):
            cur_depth = get_depth(line, " ")
            line = line.replace(g.group(), "<li>").lstrip() + "</li>"
            line_info.append(line)
            line_info.append(cur_depth)
            line_info.append("ul")
            tree.append(line_info)
            continue
        
        g = BLOCKQUOTE_REGEX.search(line)
        if type(g) != type(None): 
            # ret, idx = mdToHtml(content[idx:],-1, depth+1)
            cur_depth = get_depth(line, ">")
            line = "<p>" + line.replace(">", "").lstrip()+ "</p>"
            line_info.append(line)
            line_info.append(cur_depth)
            line_info.append(">")
            tree.append(line_info)
            
            continue

        # code block
        
        # block quote
        
        line_info.append(line)
        tree.append(line_info)
        
    return tree, idx