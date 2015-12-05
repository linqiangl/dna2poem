import random

class GraphNode(object):
    def __init__(self):
        self.type = 0
        self.data = None
        self.index = {}
        self.hole = []
        self.nodes = []

    def contains(self, node):
        return id(node) in self.index

    def strip(self):
        if len(self.hole) == 0:
            return self
        link_strip = []
        self.index = {}
        self.hole = []
        n = 0
        for one in link:
            if one is None:
                continue
            i = id(one)
            self.index[i] = n
            link_strip.append(one)
            n += 1
        self.nodes = link_strip
        return self

    def link(self, node):
        if self.contains(node):
            return self
        i = -1
        if len(self.hole) > 0:
            i = self.hole.pop()
            self.nodes[i] = node
        else:
            i = len(self.nodes)
            self.nodes.append(node)
        self.index[id(node)] = i
        return self

    def unlink(self, node):
        if not self.contains(node):
            return self
        i = self.index[id(node)]
        self.nodes[i] = None
        self.hole.append(i)
        del self.index[id(node)]
        return self

    def random_walk(self):
        node = None
        self.strip()
        n = len(self.nodes) - 1
        while node is None:
            i = random.randint(-1, n)
            if i < 0:
                return self
            node = self.nodes[i]
        return node
