#!/usr/bin/python3

import pathlib
import time
from collections import Counter
from threading import Lock, Thread

import matplotlib.pyplot as plt

THREADS = 8
MUTEX = Lock()
subzones_count = []


class ThreadFun(Thread):
    def __init__(self, domains_set, index, parent_path):
        Thread.__init__(self)
        self.index = index
        self.domains_set = domains_set
        self.parent = parent_path

    def run(self):
        subzones_count_thread = []
        for domain in self.domains_set:
            subzones_count_thread.append(
                len(list((self.parent / domain).iterdir())) - 2)
        MUTEX.acquire()
        subzones_count.extend(subzones_count_thread)
        MUTEX.release()


def RRCountSubZonesCalculator():
    data = pathlib.Path.cwd().parent / "shared" / "census"
    domains = list(data.iterdir())
    chunk = int(len(domains)/THREADS) + 1
    i, tid = 0, 0
    threadPool = []
    while tid < THREADS:
        threadPool.append(ThreadFun(domains[i:i+chunk], tid, data))
        i = i + chunk
        tid += 1
    for t in threadPool:
        t.start()
    for t in threadPool:
        t.join()


def ScatterPlot():
    cnt = Counter(subzones_count)
    x_axis = []
    y_axis = []
    for k, v in cnt.items():
        x_axis.append(k)
        y_axis.append(v)

    p = plt.figure(2, figsize=(20, 14))
    plot = p.add_subplot(1, 1, 1)
    plot.scatter(x_axis, y_axis, s=125,
                 alpha=0.9, facecolors='none', edgecolors='b')
    plot.set_xlabel('Number of subzones', fontsize=75)
    plot.set_ylabel('# of 2nd level domains', fontsize=75)
    plot.set_yscale('log')
    plot.set_xscale('log')
    plot.tick_params(labelsize=75)
    plt.subplots_adjust(hspace=1.6)
    plt.savefig(pathlib.Path.cwd().parent / 'shared' /
                'Figure7.pdf', bbox_inches='tight', dpi=300)
    print(f'> Plot saved to: shared/Figure7.pdf')
    # plt.show()


if __name__ == "__main__":
    # Assumes that the census folder is present in the shared folder.
    data = pathlib.Path.cwd().parent / "shared"
    if not (data / "census").exists():
        print("census folder doesn't exist")
        exit()
    RRCountSubZonesCalculator()
    ScatterPlot()
