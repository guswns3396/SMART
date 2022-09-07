from uuid import uuid4


class Node:
    """
    Node class that stores information
    of a particular configuration in the study tree
    """
    idx = 0
    def __init__(self, txt: str):
        assert isinstance(txt, str)
        self.idx = Node.idx
        self.txt = txt
        self.left = None
        self.right = None
        self.count = 0
        Node.idx += 1

    def __getitem__(self, key):
        if key == -1:
            return self.left
        elif key == 1:
            return self.right
        else:
            raise ValueError

    def set_left(self, node: 'Node'):
        self.left = node

    def set_right(self, node: 'Node'):
        self.right = node

    def print(self):
        print(self.idx, self.txt)
        if self.left:
            self.left.print()
        if self.right:
            self.right.print()


class Study:
    """
    Study class that contains the parameters
    and attributes for a particular study
    """

    def __init__(self, parameters: dict):
        """
        Instantiate Study class
        :param parameters: dict containing levels, text at each level,
        and probability of the biased coin
        """
        # parse dict to create study tree
        self.root = Node(parameters['lvls'][0][0])
        currnodes = [self.root]
        for i in range(len(parameters['lvls'])):
            nxtnodes = []
            if i == 0:
                continue
            for node in currnodes:
                left = Node(parameters['lvls'][i][0])
                right = Node(parameters['lvls'][i][1])
                node.set_left(left)
                node.set_right(right)
                nxtnodes.extend([left, right])
            currnodes = nxtnodes

        # probability
        self.p = float(parameters['p'])

        # generate id for the study
        self.id = str(uuid4())

    def get_count(self, config):
        node = self.root
        for rand in config:
            node = node[rand]
        return node.count
