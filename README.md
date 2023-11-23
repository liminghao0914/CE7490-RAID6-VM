# RAID-6 Based Distributed Storage System

This project, part of CE7490 Advanced Topics in Distributed Systems, focuses on the implementation and analysis of a RAID-6 based distributed storage system.

# Introduction

In our implementation, we've utilized advanced coding techniques based on Vandermonde-RS code. 
The system is designed with six primary functions: distributing data storage, handling data updates, disk failure detection, data restoration, and data object retrieval.

<p align="left">
  <img width="460" src="/imgs/RAID_6.png">
</p>


## Overview
The project report includes various images that demonstrate the system's flow and architecture:

![RAID-6 Data Flow](/imgs/r6vm_sys.png)

# Installation

## Dependencies

- Flask==3.0.0
- numpy==1.22.4
- kademlia==2.2.2
- requests==2.28.0
- requests-oauthlib==1.3.1
- nest-asyncio==1.5.6

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install RAIDVM.

```bash
pip install poetry
poetry install
```

# Project Structure

The project is structured with clear separation of concerns, allowing for easy configuration, data management, and system testing.

```
.
├── data                    # Data objects used for testing and demonstration
│   ├── shakespeare.txt     # Text data example
│   └── img_test.png        # Image data example
├── src                     # Source code of the RAID-6 system
│   ├── RAID6.py            # Main RAID-6 logic
│   ├── GaloisField.py      # Galois Field arithmetic implementation
│   ├── config.py           # Configuration parameters for the system
│   ├── vm_app              # Virtual machine application for RAID-6 system
│   │   ├── app.py          # Flask application for HTTP I/O operations
│   │   ├── Dockerfile      # Dockerfile for creating containerized environment
│   │   └── ...             # Additional vm_app module files
│   └── utils.py            # Utility functions for RAID-6 operations
├── images                  # Images for README and report documentation
├── test.py                 # Script to run system tests and performance benchmarks
├── storage_default         # Default storage directory for RAID-6 data blocks
├── storage_rebuild         # Storage for reconstructed data after disk failure
├── data_retrieved          # Directory for data retrieved from the RAID-6 system
└── README.md               # Project documentation
```

# Running Experiments

To initiate the test experiments and observe the RAID-6 system in action, run:

```bash
bash test.sh
```

# Acknowledgement


