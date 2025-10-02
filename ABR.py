class ABRNode:
    def __init__(self, key): 
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class ABR:
    def __init__(self):
        self.root = None
        self.disk_accesses = 0
        self.disk_access_log = []

    def insert(self, key):
        node = ABRNode(key)
        y = None
        x = self.root
        # cerca la posizione giusta per l'inserimento
        while x is not None:
            self.disk_accesses += 1
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right
        node.parent = y
        # collega il nuovo nodo al padre
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        self.disk_access_log.append(self.disk_accesses)

    def search(self, key):
        x = self.root
        # scorri l'albero fino a trovare la chiave o arrivare a None
        while x is not None:
            self.disk_accesses += 1
            if key == x.key:
                self.disk_access_log.append(self.disk_accesses)
                return True
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        self.disk_access_log.append(self.disk_accesses)
        return False