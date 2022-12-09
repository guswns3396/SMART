from uuid import uuid4
from scipy.stats import bernoulli


class Question:
    def __init__(self, q: str, a: dict):
        self.q = q
        self.a = a


class Level:
    def __init__(self, scna: str, scnb: str, qset: list):
        self.scna = scna
        self.scnb = scnb
        self.qset = qset


class Node:
    def __init__(self):
        self.a = None
        self.b = None
        self.count = 0


class YNode(Node):
    def __init__(self):
        super().__init__()

    def __getitem__(self, item):
        if item == -1:
            return self.a
        elif item == 1:
            return self.b
        else:
            raise ValueError('key must be 1 or -1')


class XNode(Node):
    def __init__(self, txt: str, qset: list):
        super().__init__()
        self.txt = txt
        self.qset = qset

    def __getitem__(self, item):
        if item == 0:
            return self.a
        elif item == 1:
            return self.b
        else:
            raise ValueError('key must be 0 or 1')


class Study:
    """
    Study class that contains the parameters
    and attributes for a particular study
    """

    @staticmethod
    def verify_params(parameters: 'ImmutableMultiDict'):
        """
        Verify parameters are in correct format
        :param parameters:
        :return:
        """
        # make sure key in parameters
        for key in ['scn-a', 'scn-b', 'prim_q', 'p', 'num_lvls']:
            if key not in parameters:
                raise ValueError(key + ' key not in parameters')
        # make sure each level has 2 scenarios
        if len(parameters.getlist('scn-a')) != len(parameters.getlist('scn-b')):
            raise ValueError('each level must have 2 scenarios')
        # make sure number of scenarios matches number of levels
        if len(parameters.getlist('scn-a')) != int(parameters['num_lvls']):
            print(len(parameters.getlist('scn-a')), parameters['num_lvls'])
            raise ValueError('number of scenarios does not match number of levels:')

    @staticmethod
    def make_levels(parameters: 'ImmutableMultiDict'):
        lvls = []
        alist = parameters.getlist('scn-a')
        blist = parameters.getlist('scn-b')
        qlist = []
        pas = [
            'Strongly disagree',
            'Disagree',
            'Somewhat disagree',
            'Neutral',
            'Somewhat agree',
            'Agree',
            'Strongly agree'
        ]
        pa = {a: i + 1 for a, i in zip(pas, range(7))}
        pq = Question(parameters['prim_q'], pa)
        qlist.append(pq)
        for scna, scnb in zip(alist, blist):
            lvls.append(Level(scna, scnb, qlist))
        return lvls

    def __init__(self, root: 'YNode', numlvls: int, p: float):
        """
        Instantiate Study class
        """
        # root node
        self.root = root
        # number of levels
        self.numlvls = numlvls
        # probability
        self.p = p
        # generate id for the study
        self.id = str(uuid4())

    @staticmethod
    def make_tree(levels):
        root = YNode()
        currnodes = [root]
        for i in range(len(levels) * 2):
            nxtnodes = []
            if i % 2 == 0:
                for node in currnodes:
                    node.a = XNode(levels[i // 2].scna, levels[i // 2].qset)
                    node.b = XNode(levels[i // 2].scnb, levels[i // 2].qset)
                    nxtnodes.extend([node.a, node.b])
            else:
                for node in currnodes:
                    node.a = YNode()
                    node.b = YNode()
                    nxtnodes.extend([node.a, node.b])
            currnodes = nxtnodes
        return root

    def get_node(self, config):
        node = self.root
        for i in config:
            node = node[i]
        return node

    def randomize(self, config):
        node = self.get_node(config)
        # only randomize if next level
        if node.a and node.b:
            n1 = node.a.count
            n2 = node.b.count
            # if first randomization p = 0.5
            if not config:
                p = 0.5
            # else biased coin
            else:
                if n1 > n2:
                    p = self.p
                elif n1 < n2:
                    p = 1 - self.p
                else:
                    p = 0.5
            x = bernoulli.rvs(p) * 2 - 1
            # add to count
            newconfig = config + [x]
            node = self.get_node(newconfig)
            node.count += 1
            return x
        else:
            raise RuntimeError('cannot randomize further')

    def get_vignette_params(self, config):
        node = self.get_node(config)
        if not isinstance(node, XNode):
            raise RuntimeError('must be an x node to get parameters')
        params = {
            'txt': node.txt,
            'qset': node.qset
        }
        return params

    def get_answers(self, answers: 'ImmutableMultiDict', config: list):
        # parse answers
        # store answers
        # update config based on answer to primary question
        ans = int(answers['prim_q'])
        if ans > 4:
            y = 1
        else:
            y = 0
        newconfig = config + [y]
        # update node count
        node = self.get_node(newconfig)
        node.count += 1
        return newconfig

    def enroll(self):
        self.root.count += 1

    def print(self):
        l = [[self.root.count]]
        currnodes = [self.root]
        for i in range(self.numlvls * 2):
            counts = []
            nxtnodes = []
            for node in currnodes:
                counts.extend([node.a.count, node.b.count])
                nxtnodes.extend([node.a, node.b])
            currnodes = nxtnodes
            l.append(counts)
        print(l)
