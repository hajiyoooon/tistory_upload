HEADER = "#"
INDENT = ">"
NEW_LINE = "\n"

class Node:
    def __init__(self, char):
        self.char = char
        self.parent = None
        self.childs = list()

    def set_parent(self, node):
        self.parent = node

    def get_parent(self):
        return self.parent

    def add_child(self, child):
        child.set_parent(self)
        self.childs.append(child)

    def has_child(self):
        return len(self.childs) == 0

    def get_childs(self):
        return self.childs

    def get_char(self):
        return self.char

class MarkdownParser:
    def __init__(self):
        self.root = Node("")
        self.node = self.root

    def parse(self, lines):
        for ch in lines:
            child = Node(ch)
            self.node.add_child(child)
            
            if ch is HEADER:
                self.node = child
            elif ch is NEW_LINE:
                self.node = child.get_parent()

    def _to_string(self):
        to_string(self.root)

def to_string(node):
    childs = node.get_childs()
    print(node)

    for child in childs:
        print(child)
        # print(child.get_char(), end="")
        
        if(child.has_child()):
            to_string(child)


line = " # 안녕하세요\n"
parser = MarkdownParser()

parser.parse(line)
print()
parser._to_string()

