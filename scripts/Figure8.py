#!/usr/bin/python3

import csv
import math
import os
import pathlib
import shutil
import subprocess
import sys
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np


def Run_GRoot(census_directory, groot_executable, logs_folder):
    i = 0
    logs_folder.mkdir(exist_ok=True)
    k = 0
    for domain in census_directory.iterdir():
        i += 1
        subprocess.run([groot_executable, domain, "-l"])
        pathlib.Path("log.txt").rename(domain.name + '.txt')
        shutil.move(domain.name + '.txt', logs_folder)
        if i >= 100000*k:
            print(f'> Finished {i} domains')
            k += 1


def Generate_CSV(logs_directory):
    attributes = []
    for f in logs_directory.iterdir():
        with open(f, "r") as logfile:
            total_rrs = 0
            for line in logfile:
                if "Total number of RRs parsed across all zone files: " in line:
                    total_rrs = line.split(
                        "Total number of RRs parsed across all zone files: ")[-1][:-1]
                elif "Time to build label graph and zone graphs: " in line:
                    graph = line.split(
                        "Time to build label graph and zone graphs: ")[-1][:-2]
                elif "Time to check all user jobs: " in line:
                    checking = line.split(
                        "Time to check all user jobs: ")[-1][:-2]
                elif "Total number of ECs across all jobs: " in line:
                    ecs = line.split(
                        "Total number of ECs across all jobs: ")[-1][:-1]
                elif "Label Graph: " in line:
                    label = line.split("Label Graph: ")[-1][:-1]
                elif "Interpretation Graph Vertices: " in line:
                    vertices = line.split(
                        "Interpretation Graph Vertices: ")[-1][:-1]
                elif "Interpretation Graph Edges: " in line:
                    edges = line.split("Interpretation Graph Edges: ")[-1][:-1]
            attributes.append([f.with_suffix('').name, int(total_rrs), int(ecs),
                               float(graph), float(checking), float(graph) + float(checking), label, vertices, edges])
    attributes.sort(key=lambda x: x[1], reverse=True)
    attributes.insert(0, ["Domain", "Total RRs", "Total Interpretation Graphs", "Graph building (s)", "Property Checking (s)",
                          "Total time (s)", "Label Graph ", "Interpretation Graph Vertices", "Interpretation Graph Edges"])
    with open(pathlib.Path.cwd().parent / "shared" / "Attributes.csv", "w", newline='') as filex:
        writer = csv.writer(filex)
        for a in attributes:
            writer.writerow(a)
    print(f'> Finished generation of Attributes.csv')
    return attributes


def Generate_Plot(attributes):

    rrs_time = {}
    for row in attributes[1:]:
        rrs_time.setdefault(int(row[1]), list()).append(float(row[5]))

    rrs = []
    median_time = []

    for (x, times) in sorted(rrs_time.items()):
        rrs.append(x)
        median_time.append(np.median(times))

    p = plt.figure(1, figsize=(18, 8))
    plot = p.add_subplot(1, 1, 1)

    plot.yaxis.grid(ls='dotted', alpha=0.6, zorder=0)
    plot.xaxis.grid(ls='dotted', alpha=0.6, zorder=0)
    plot.set_xlabel('Number of resource records', fontsize=40)
    plot.set_ylabel('Time (s)', fontsize=40)
    plot.set_yscale('log')
    plot.set_xscale('log')
    plot.scatter(rrs, median_time, s=95, alpha=0.6,
                 marker=".", c='purple', zorder=3)
    plot.set_yticks([0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000])
    plot.tick_params(labelsize=35)
    plot.set_xlim(xmin=1, xmax=31000000)

    plt.savefig(pathlib.Path.cwd().parent / "shared" /
                "Figure8.pdf", bbox_inches='tight')
    print(f'> Plot saved to: shared/Figure8.pdf')
    # plt.show()


if __name__ == "__main__":
    # Assumes that the census folder is present in the shared folder.

    parent = pathlib.Path.cwd().parent
    census_dataset = parent / "shared" / "census"
    if not census_dataset.exists():
        print("census folder doesn't exist")
        exit()
    if len(sys.argv) < 2:
        print("Path to the GRoot exectuable is not provided")
        exit()
    groot = pathlib.Path(sys.argv[1])
    if groot.exists() and os.access(groot, os.X_OK):
        Run_GRoot(census_dataset, sys.argv[1],
                  pathlib.Path(parent / "shared" / "logs"))
        attributes = Generate_CSV(pathlib.Path(parent / "shared" / "logs"))
        Generate_Plot(attributes)
    else:
        print("Please check the path provided for GRoot executable.")
