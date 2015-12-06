class GraphNode(object):
    def __init__(self):
        self.type = 0
        self.data = None
        self.index = {}
        self.hole = []
        self.nodes = []
        self._strcache = None

    def __str__(self):
        if self._strcache is None:
            self._strcache = str(self.data)
        return self._strcache

    def __repr__(self):
        return self.__str__()

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

    def _filter(self, nodes):
        return nodes

    def tranverse_bfs(self, callback=None, filter=None):
        if filter is None:
            filter = self._filter
        visit = {}
        queue = [self]
        next_level = []
        while len(queue) > 0:
            for node in queue:
                if node is None:
                    continue
                visit[id(node)] = -1
                for one in filter(node.nodes):
                    if one is None:
                        continue
                    if id(one) in visit:
                        continue
                    next_level.append(one)
                    visit[id(one)] = -1
                if callback is not None:
                    callback(node)
            queue = next_level
            next_level = []

    def tranverse_dfs(self, callback=None, filter=None):
        if filter is None:
            filter = self._filter
        visit = {}
        queue = [self]
        next_level = []
        visit[id(self)] = 0
        while len(queue) > 0:
            node = queue.pop()
            if node is None:
                continue
            visit[id(node)] = -1
            n = len(queue)
            for one in filter(node.nodes):
                if one is None:
                    continue
                if id(one) in visit:
                    i = visit[id(one)]
                    if i < 0 or i >= n:
                        continue
                    queue[i] = None
                visit[id(one)] = n + len(next_level)
                next_level.append(one)
            if callback is not None:
                callback(node)
            next_level.reverse()
            m = len(next_level)
            for i, one in enumerate(next_level):
                k = id(one)
                visit[k] = (n + m) - (visit[k] - n) - 1
            queue = queue + next_level
            next_level = []

    def debug_random_walk(self):
        import random
        node = None
        self.strip()
        n = len(self.nodes) - 1
        while node is None:
            i = random.randint(-1, n)
            if i < 0:
                return self
            node = self.nodes[i]
        return node
