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


def Run_GRoot(census_directory, groot_executable, logs_folder):
    i = 0
    logs_folder.mkdir(exist_ok=True)

    for domain in census_directory.iterdir():
        i += 1
        subprocess.run([groot_executable, domain, "-l"])
        pathlib.Path("log.txt").rename(domain.name + '.txt')
        shutil.move(domain.name + '.txt', logs_folder)


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
    attributes.sort(key=lambda x: x[2], reverse=True)
    attributes.insert(0, ["Domain", "Total RRs", "Total Interpretation Graphs", "Graph building (s)", "Property Checking (s)",
                          "Total time (s)", "Label Graph ", "Interpretation Graph Vertices", "Interpretation Graph Edges"])
    with open(pathlib.Path.cwd().parent / "shared" / "Attributes.csv", "w", newline='') as filex:
        writer = csv.writer(filex)
        for a in attributes:
            writer.writerow(a)
    return attributes


def Generate_Plot(attributes):

    bucket = {}
    for row in attributes[1:]:
        bucket.setdefault(int(row[2]/1000), list()).append(row)

    total_graphs = []
    graph_building = []
    property_checking = []
    total_time = []
    for (_, elems) in bucket.items():
        _, _, total_graphs_b, graph_building_b, property_checking_b, total_time_b, _, _, _ = zip(
            *elems)
        total_graphs.append(mean(total_graphs_b))
        graph_building.append(mean(graph_building_b))
        property_checking.append(mean(property_checking_b))
        total_time.append(mean(total_time_b))

    total_graphs, graph_building, property_checking, total_time = zip(
        *sorted(zip(total_graphs, graph_building, property_checking, total_time), key=lambda t: t[0]))

    p = plt.figure(1, figsize=(12, 7))
    plot = p.add_subplot(1, 1, 1)

    plot.scatter(total_graphs, total_time, s=90, alpha=0.9,
                 label="Total time", marker="x", c='purple')

    plot.plot(total_graphs, graph_building, label="Label graph building")
    plot.plot(total_graphs, property_checking, label="Property checking")

    plot.set_xlabel('Number of interpretation graphs built', fontsize=30)
    plot.set_ylabel('Time (s)', fontsize=30)
    plot.set_yscale('log')
    plot.set_xscale('log', basex=10)
    plot.tick_params(labelsize=30)
    plot.legend(fontsize=30)
    plt.savefig(pathlib.Path.cwd().parent / "shared" / "Figure8.pdf", bbox_inches='tight')


if __name__ == "__main__":
    # Assumes that the census_larger folder is present in the shared folder.
    parent = pathlib.Path.cwd().parent
    census_dataset = parent / "shared" / "census_larger"
    if not census_dataset.exists():
        print("census_larger folder doesn't exist")
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
