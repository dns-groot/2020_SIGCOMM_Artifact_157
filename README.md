SIGCOMM'20 Artifact for Paper 157
<a href='https://zenodo.org/record/3905968'><img align='right' src='https://img.shields.io/badge/DOI-10.5281%2Fzenodo.3905968-blue.svg'/></a>
=============================

This repository contains the code to reproduce the claims made in our SIGCOMM paper titled "GRoot: Proactive Verification of DNS Configurations". More specifically, we provide the working code for generating the equivalence classes, constructing the interpretation graphs, and for checking various properties over the constructed interpretation graphs.

**NOTE:** Please refer to the maintained [`GRoot`](https://github.com/dns-groot/groot) repository to learn how to use the tool to check various properties and also to make pull requests or to create issues. This repository is only for archival purposes. 

### Claims Supported by The Artifact
- Full dataset (zone files) created from the CSV files of the publicly available [DNS Census 2013](https://dnscensus2013.neocities.org/index.html)
- Census Dataset statistics as shown in _Figure 7(b)_
- Performance claims made in _&sect;7.3_ on DNS Census dataset and the corresponding plot shown in _Figure 8_  
    
### Claims NOT Supported by The Artifact
- Functionality claims made in _&sect;7.2_ (related to _Figure 7(a)_ and _Table 4_)  
  _Reason_: The zone files used for these experiments are confidential  and proprietary.

## Census Dataset Organization
The created Census data is available from UCLA box:  [Census Dataset](https://ucla.box.com/s/tod4z48cb66hjgto2dg7fel7gj21bt4s)

Download and unzip the dataset. Let the `census` folder be placed in a folder named `data`.  
The compressed dataset is _~3&hairsp;GB_ and consists of _~8.1&hairsp;M_ files. 

:rotating_light: **Linux:** When decompressed the folder consumes  _~38&hairsp;GB_ on Linux due to the default _4&hairsp;KB_ block size on ext4. One of the plot generation scripts also generates _~1.3&hairsp;M_ files. The Linux system might give the error message `No space left on device` when decompressing even if there is plenty of disk place. [This happens when the filesystem runs out of inodes.](https://scoutapm.com/blog/understanding-disk-inodes) The Census dataset and the plot generation scripts together require at least  _~45&hairsp;GB_ of unused disk space and also _~10.7&hairsp;M_ free inodes (can be checked using `df -ih`).

:warning: **Windows:** When decompressed the folder consumes only _~4&hairsp;GB_ on Windows [since the majority of the files are less than _1&hairsp;KB_.](https://superuser.com/questions/1030800/how-can-a-files-size-on-disk-be-0-bytes-when-theres-data-in-it)

## Installation

### Using `docker` (strongly recommended)

_**Note:** The docker image may consume  ~&hairsp;1.2&hairsp;GB of disk space._

0. [Get `docker` for your OS](https://docs.docker.com/install).
1. Pull our docker image<sup>[#](#note_1)</sup>: `docker pull dnsgt/2020_sigcomm_artifact_157`.
2. Docker containers are isolated from the host system.
Therefore, to run Groot on zones files residing on the host system,
you must first [bind mount] them while running the container:
    ```bash
    docker run -v <absolute path to the above data folder>:/home/groot/groot/shared -it dnsgt/2020_sigcomm_artifact_157
    ```
    This would give you a `bash` shell within groot directory.
 

<a name="note_1"><sup>#</sup></a> Alternatively, you could also build the Docker image locally:

```bash
docker build -t dnsgt/2020_sigcomm_artifact_157 github.com/dns-groot/2020_sigcomm_artifact_157
```

The `data` folder on the host system would then be accessible within the container at `~/groot/shared` (with read+write permissions). 

### Manual Installation for Windows

<details>

<summary><kbd>CLICK</kbd> to reveal instructions</summary>

1. Install [`vcpkg`](https://docs.microsoft.com/en-us/cpp/build/vcpkg?view=vs-2019) package manager to install dependecies. 
2. Install the C++ libraries (64 bit versions) using:
    - .\vcpkg.exe install boost-serialization:x64-windows boost-flyweight:x64-windows boost-dynamic-bitset:x64-windows boost-graph:x64-windows  boost-accumulators:x64-windows docopt:x64-windows nlohmann-json:x64-windows spdlog:x64-windows
    - .\vcpkg.exe integrate install 
3. Clone the repository (with  `--recurse-submodules`) and open the solution (groot.sln) using Visual Studio. Set the platform to x64 and mode to Release.
4. Configure the project properties to use ISO C++17 Standard (std:c++17) for C++ language standard.
5. Set `groot` as `Set as Startup Project` using the solution explorer in the Visual Studio. Build the project using visual studio to generate the executable. The executable would be located at `~\groot\x64\Release\`.
6. Install python3 and `matplotlib` library.
7. Move the `data` folder to the top of this repository and rename the folder to `shared`.
</details>


## Verification of Claims:

All commands must be run within `~/groot/scripts/` directory.  

### Figure 7(b)

- To generate the plot shown in _Figure 7(b)_ run the script `Figure7.py`.
     ```bash
     python3 Figure7.py
     ```
- _Est. Time:_ 5 min, generates the plot `Figure7.pdf` directly in the `shared` folder.

### Figure 8

- To generate the plot shown in _Figure 8_ run the script `Figure8.py`.
     ```bash
     python3 Figure8.py <path_to_the_groot_executable>
     ```
     - The script requires as input the path to the groot executable.
     - If the script is run from a docker container, then the script can be run as follows:
          ```bash
          python3 Figure8.py ../build/bin/groot
          ```
     - If the script is run on Windows then the script can be run as follows:
          ```bash
          python3 Figure8.py ..\x64\Release\groot.exe
          ```
     - The script dumps the log for each domain into the `shared/logs/` subdirectory and in the end generates a summary file `Attributes.csv` in the `shared` folder.
     - `Attributes.csv` contains the following information for each domain:
        - _Number of resource records_ (_RRs_)
        - Number of interpretation graphs built
        - Time taken to parse zone files and build the label graph (Label graph building)
        - Time taken to construct the interpretation graphs and check properties on them (Property checking)
        - _Total execution time_ (_T_)
        - Label graph size (number of vertices and edges)
        - Statistics across interpretation graphs (mean, median, min and max of vertices and edges)  
     - **NOTE:** After running GRoot on all the _~1.3&hairsp;M_ domains, the script calculates the median _T_ for each distinct value of _RRs_ and plots the median _T_ vs the _RRs_. 
- _Est. Time:_ 10 hours, generates the plot `Figure8.pdf` from `Attributes.csv` in the `shared` folder.

## LICENSE

The code in this repository, GRoot are all licensed under the [MIT License](LICENSE).
