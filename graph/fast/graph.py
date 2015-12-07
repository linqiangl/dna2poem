class GraphNode(object):
    def __init__(self):
        self.reset()

    def __str__(self):
        if self._strcache is None:
            self._strcache = "<GraphNode %s>" % str(self.data)
        return self._strcache

    def __repr__(self):
        return self.__str__()

    def reset(self):
        self.type = 0
        self.data = None
        self.index = {}
        self.hole = []
        self.nodes = []
        self._strcache = None
        return self

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
        return self

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
        return self

    def debug_data_encode(self, data):
        if data is None:
            return ""
        return data

    def debug_data_decode(self, data):
        if len(data) == 0:
            return None
        return data

    """
    line := id type data | id links
    data := <b64encode>data
    links := id id id ...
    e.g
    0 0 aJwov2wP03nJ==
    1 0 ovq9A0fwT3aqf1

    0 1
    1 0
    """
    def debug_load(self, filename, data_decode=None):
        import base64
        self.reset()
        if data_decode is None:
            data_decode = self.debug_data_decode
        id_node_map = {}
        f = open(filename, "r")
        for line in f:
            line = line[:-1]
            if len(line) == 0:
                break
            line = line.split(' ')
            node_id = int(line[0])
            node = GraphNode()
            node.type = int(line[1])
            node.data = data_decode(base64.b64decode(line[2]))
            self.link(node)
            id_node_map[node_id] = node
        for line in f:
            line = line.split(' ')
            node_id = int(line[0])
            node = id_node_map[node_id]
            line = line[1:]
            for one_id in line:
                node.link(id_node_map[int(one_id)])
        f.close()
        return self

    def debug_save(self, filename, data_encode=None):
        import base64
        if data_encode is None:
            data_encode = self.debug_data_encode
        f = open(filename, "w+")
        for node in self.nodes:
            f.write("%d %d %s\n" % (
                self.index[id(node)],
                node.type,
                base64.b64encode(data_encode(node.data)),
            ))
        for node in self.nodes:
            if len(node.nodes) == 0:
                continue
            f.write("\n%d %s" % (
                self.index[id(node)],
                " ".join([str(self.index[id(one)]) for one in node.nodes]),
            ))
        f.close()
        return self

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
