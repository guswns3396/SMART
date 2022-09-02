class Level():
    """
    Level class that contains texts and number of branches
    """
    def __init__(self, lvl:int, numbranch:int, texts:list):
        """
        Instantiates Level class
        :param lvl: level number
        :param numbranch: number of branches following the level
        :param texts: list of texts corresponding to number of
        branches of previous level
        """
        assert isinstance(lvl, int)
        assert isinstance(numbranch, int)
        assert isinstance(texts, list)
        self.lvl = lvl
        self.numbranch = numbranch
        self.texts = texts

class Study():
    """
    Study class that contains the parameters
    and attributes for a particular study
    """
    def __init__(self, parameters:dict):
        """
        Instantiate Study class
        :param parameters: dict containing levels, text at each level,
        and number of branches at each level
        """
        # parse dict to instantiate levels
        lvls = [
            Level(
                lvl=int(lvl),
                numbranch=int(parameters[lvl]['numbranch']),
                texts=[parameters[lvl][scn] for scn in parameters[lvl] if scn != 'numbranch']
            ) for lvl in parameters
        ]
        # verify number of branches from previous level
        # matches number of texts at the current level
        for i in range(1,len(lvls)):
            assert len(lvls[i].texts) == lvls[i-1].numbranch
