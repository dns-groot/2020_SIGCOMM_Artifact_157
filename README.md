# SIGCOMM'20 Artifact for Paper 157

This repository contains the code to reproduce the claims made in our SIGCOMM paper titled "GRoot: Proactive Verification of DNS Configurations". More specifically, we provide the working code for generating the equivalence classes, constructing the interpretation graphs, and for checking various properties over the constructed interpretation graphs.

**NOTE:** Please refer to the maintained [`GRoot`](https://github.com/dns-groot/groot) repository to learn how to use the tool to check various properties and also to make pull requests or to create issues. This repository is only for archival purposes. 

### Claims Supported by The Artifact
- Full dataset created from the DNS Census data
- Census Dataset statistics as shown in _Figure 7(b)_
- Performance claims made in _&sect;7.3_ for DNS Census and the corresponding plot shown in _Figure 8_  
    
### Claims NOT Supported by The Artifact
- Functionality claims made in _&sect;7.2_ (related to _Figure 7(a)_ and _Table 4_)  
  _Reason_: The zone files used for these experiments are confidental and proprietary.

## Census Dataset Organization
The Census data is divided into two parts and are available at:
- [Census_larger](https://ucla.box.com/s/4uf4w6lkwp3ul3788f3kpkyg5j43ap87)
- [Census_smaller](https://ucla.box.com/s/l4e7jvwixunjettonhwbj8lw625gtlb0)

Download and unzip the two datasets. Let the two folders be placed in a folder named `data`.  

## Installation

### Using `docker` (strongly recommended)

_**Note:** The docker image may consume  ~&hairsp;1.2&hairsp;GB of disk space._

0. [Get `docker` for your OS](https://docs.docker.com/install).
1. Pull our docker image<sup>[#](#note_1)</sup>: `docker pull dnsgt/2020_sigcomm_artifact_157`.
2. Docker containers are isolated from the host system.
Therefore, to run Groot on zones files residing on the host system,
you must first [bind mount] them while running the container:
    ```bash
    docker run -v <path to the above data folder>:/home/groot/groot/shared -it dnsgt/groot
    ```
    This would give you a `bash` shell within groot directory.
 

<a name="note_1"><sup>#</sup></a> Alternatively, you could also build the Docker image locally:

```bash
docker build -t dnsgt/groot github.com/dns-groot/groot
```

The `data` folder on the host system would then be accessible within the container at `~/groot/shared` (with read+write permissions). 

### Manual Installation for Windows

<details>

<summary><kbd>CLICK</kbd> to reveal instructions</summary>

1. Install [`vcpkg`](https://docs.microsoft.com/en-us/cpp/build/vcpkg?view=vs-2019) package manager to install dependecies. 
2. Install the C++ libraries (64 bit versions) using:
    - .\vcpkg.exe install boost-serialization:x64-windows boost-flyweight:x64-windows boost-dynamic-bitset:x64-windows boost-graph:x64-windows  boost-accumulators:x64-windows docopt:x64-windows nlohmann-json:x64-windows spdlog:x64-windows
    - .\vcpkg.exe integrate install 
3. Clone the repository (with  `--recurse-submodules`) and open the solution (groot.sln) using Visual studio. Set the platform to x64 and mode to Release.
4. Configure the project properties to use ISO C++17 Standard (std:c++17) for C++ language standard.
5. Build the project using visual studio to generate the executable. The executable would be located at `~\groot\x64\Release\`.
6. Install python3 and `matplotlib` library.
7. Move the `data` folder to the top of this repository and rename the folder to `shared`.
</details>


## Verification of Claims:

All commands must be run within `~/groot/scripts/` directory.  

### Figure 7(b)

- To generate the plot shown in _Figure 7(b)_ run the script `Figure5.py`.
     ```bash
     python3 Figure7.py
     ```
- _Est. Time:_ 5 min, generates the plot `Figure7.pdf` directly

### Figure 8

- This plot is based on only the `census_larger` dataset
     - We used a threshold of at least 5000 interpretation graphs and all the domains in `census_smaller` generate less than 5000 interpretation graphs.
     - One can run the same following steps on the `census_smaller` by slightly modifying the `Figure8.py` if required.  
- To generate the plot shown in _Figure 8_ run the script `Figure8.py`.
     ```bash
     python Figure8.py <path_to_the_groot_executable>
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
     - The script dumps the log for each domain into the `logs/` subdirectory and in the end generates a summary file `Attributes.csv`.
     - `Attributes.csv` contains the following information for each domain:
        - Number of resource records
        - _Number of interpretation graphs built_
        - Time taken to parse zone files and build the label graph (_Label graph building_)
        - Time taken to construct the interpretation graphs and check properties on them (_Property checking_)
        - _Total execution time_
        - Label graph size (number of vertices and edges)
        - Statistics across interpretation graphs (mean, median, min and max of vertices and edges)  
     - **NOTE:** After running the tool on all the 270 domains of the `census_larger` dataset, the script groups the domains into buckets of size 1000 based on the number of interpretation graphs and considers the mean value from each bucket to make the visualization more comfortable to understand.
- _Est. Time:_ 4 hours, generates the plot `Figure8.pdf` from `Attributes.csv`

## LICENSE

The code in this repository, GRoot are all licensed under the [MIT License](LICENSE).