class ShortestLinkPathRouter(object):
    def __init__(self):
        self.result = None
        self.filter = None
        self._tree = None
        self._cursor = None
        self._visit = None

    def _filter(self, nodes):
        return nodes

    def route(self, src, dst):
        self.src = src
        self.dst = dst
        if self.filter is None:
            self.filter = self._filter
        self.result = None
        self._tree = [-1]
        self._cursor = []
        self._visit = {}
        self.result = None
        self.src.tranverse_bfs(self._discovered, self.filter)
        self._visit = None
        self._cursor = None
        self._tree = None
        return self.result

    def _discovered(self, node):
        index = len(self._cursor)
        self._visit[id(node)] = -1
        for one in self.filter(node.nodes):
            if id(one) in self._visit:
                continue
            self._tree.append(index)
            self._visit[id(one)] = -1
        self._cursor.append(node)
        if node == self.dst:
            self.result = []
            while index != -1:
                self.result.append(self._cursor[index])
                index = self._tree[index]
            self.result.reverse()
            return True
