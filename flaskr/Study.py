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
    def parse_param(parameters: 'ImmutableMultiDict'):
        lvls = []
        alist = parameters.getlist('scn-a')
        blist = parameters.getlist('scn-b')
        qlist = []
        pa = {'a' + str(i + 1): i + 1 for i in range(7)}
        pq = Question(parameters['prim_q'], pa)
        qlist.append(pq)
        for scna, scnb in zip(alist, blist):
            lvls.append(Level(scna, scnb, qlist))
        return lvls

    def __init__(self, parameters: 'ImmutableMultiDict'):
        """
        Instantiate Study class
        :param parameters: dict containing levels, text at each level,
        and probability of the biased coin
        """
        # verify parameters
        self.verify_params(parameters)
        # parse dict to create study levels
        self.lvls = self.parse_param(parameters)
        # create tree
        self.root = self.make_tree()
        # probability
        self.p = float(parameters['p'])
        # generate id for the study
        self.id = str(uuid4())

    def make_tree(self):
        root = Node()
        currnodes = [root]
        for i in range(len(self.lvls)*2):
            nxtnodes = []
            if i % 2 == 0:
                for node in currnodes:
                    node.a = XNode(self.lvls[i//2].scna, self.lvls[i//2].qset)
                    node.b = XNode(self.lvls[i//2].scnb, self.lvls[i//2].qset)
                    nxtnodes.extend([node.a, node.b])
            else:
                for node in currnodes:
                    node.a = Node()
                    node.b = Node()
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
                    p = 1 - self.p
                elif n1 < n2:
                    p = self.p
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
        for i in range(len(self.lvls)*2):
            counts = []
            nxtnodes = []
            for node in currnodes:
                counts.extend([node.a.count, node.b.count])
                nxtnodes.extend([node.a, node.b])
            currnodes = nxtnodes
            l.append(counts)
        print(l)
