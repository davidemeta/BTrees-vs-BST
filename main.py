from test import run_test, plot_result

def main():
    sizes = [10, 100, 1000]
    t_values = [5, 10, 15]
    scelte = ["insert_sequenziale", "search_sequenziale", "insert_random", "search_random"]

    for size in sizes:
        for t in t_values:
            for scelta in scelte:
                abr_log, btree_log = run_test(size, scelta, t)
                plot_result(size, scelta, abr_log, btree_log, t)


if __name__ == "__main__":
    main()