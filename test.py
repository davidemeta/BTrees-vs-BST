import random
import matplotlib.pyplot as plt
import os
from ABR import ABR
from BTree import BTree

def run_test(size, scelta, t):
    numbers = list(range(size))
    if scelta in ["insert_sequenziale", "search_sequenziale"]:
        sequenza = numbers
    elif scelta in ["insert_random", "search_random"]:
        sequenza = numbers[:]
        random.shuffle(sequenza)

    b_tree = BTree(t)
    abr_tree = ABR()
    
    # BTree
    if "insert" in scelta:
        for key in sequenza:
            b_tree.insert(key)
    else:
        for key in numbers:
            b_tree.insert(key)
        
        b_tree.disk_accesses = 0
        b_tree.disk_access_log = []
        
        for key in sequenza:
            b_tree.search(key)

    # ABR
    if "insert" in scelta:
        for key in sequenza:
            abr_tree.insert(key)
    else:
        for key in numbers:
            abr_tree.insert(key)
        
        abr_tree.disk_accesses = 0
        abr_tree.disk_access_log = []
        
        for key in sequenza:
            abr_tree.search(key)

    return abr_tree.disk_access_log, b_tree.disk_access_log


def plot_result(size, scelta, abr_log, btree_log, t):
    plt.figure()
    plt.plot(abr_log, label="ABR", linewidth=2)
    plt.plot(btree_log, label="B-Tree", linewidth=2)
    
    plt.xlabel("Numero operazioni")
    plt.ylabel("Accessi a disco")
    labels = {
        "insert_sequenziale": "Inserimento sequenziale",
        "search_sequenziale": "Ricerca sequenziale",
        "insert_random": "Inserimento random",
        "search_random": "Ricerca random"
    }
    plt.title(f"{labels[scelta]} (size={size})")
    
    plt.legend()
    plt.grid(False)

    output_dir = "plots"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"plot_{scelta}_size{size}_t{t}.png")
    plt.savefig(filename, dpi=300, bbox_inches="tight")

    plt.show()