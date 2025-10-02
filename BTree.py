class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t                       # grado minimo
        self.keys = []                   # chiavi del nodo
        self.children = []
        self.leaf = leaf

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, leaf=True)
        self.t = t
        self.disk_accesses = 0
        self.disk_access_log = []
    
    def insert(self, key):
        root = self.root
        # se la radice è piena va divisa
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, leaf=False)
            self.root = new_root
            new_root.children.append(root)
            self.split_node(new_root, 0)
            self.insert_in_node(new_root, key)
        else:
            self.insert_in_node(root, key)
        self.disk_access_log.append(self.disk_accesses)
    
    def search(self, key, node=None):
        if node is None:
            node = self.root
        i = 0
        # trova la posizione giusta nel nodo
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            self.disk_access_log.append(self.disk_accesses)
            return True
        elif node.leaf:
            self.disk_access_log.append(self.disk_accesses)
            return False
        else:
            self.disk_accesses += 1
            return self.search(key, node.children[i])

    def insert_in_node(self, node:"BTreeNode", key):
        i = len(node.keys) - 1
        if node.leaf:
            # inserimento in una foglia
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
            self.disk_accesses += 1
        else:
            # scendo fino al figlio corretto
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            self.disk_accesses += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                # se il figlio è pieno va diviso prima di scendere
                self.split_node(node, i)
                if key > node.keys[i]:
                    i += 1
            self.insert_in_node(node.children[i], key)
            
    def split_node(self, parent:"BTreeNode", i):
        # divide un nodo pieno in due e sposta la chiave in mezzo nel padre
        t = self.t
        self.disk_accesses += 3
        child = parent.children[i]
        new_child = BTreeNode(t, leaf=child.leaf)

        mid_key = child.keys[t - 1]
        new_child.keys = child.keys[t:(2 * t - 1)]
        child.keys = child.keys[0:t - 1]

        if not child.leaf:
            new_child.children = child.children[t:(2 * t)]
            child.children = child.children[0:t]

        parent.children.insert(i + 1, new_child)
        parent.keys.insert(i, mid_key)
