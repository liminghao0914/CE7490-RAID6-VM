# RAID-6 Based Distributed Storage System

This project, part of CE7490 Advanced Topics in Distributed Systems, focuses on the implementation and analysis of a RAID-6 based distributed storage system.

<p align="center">
  <img width="460" src="/imgs/RAID_6.png">
</p>

# Introduction

In our implementation, we've utilized advanced coding techniques based on Vandermonde-RS code. 
The system is designed with six primary functions: distributing data storage, handling data updates, disk failure detection, data restoration, and data object retrieval.

<p align="center">
  <img width="100%" src="/imgs/r6vm_sys.png">
</p>


# Installation

## Dependencies

### VM 
- Docker version 24.0.2, build cb74dfc

### Python
- Flask==3.0.0
- numpy==1.22.4
- kademlia==2.2.2
- requests==2.28.0
- requests-oauthlib==1.3.1
- nest-asyncio==1.5.6

Before install RAID6VM, you need to build the docker image by
```bash
bash raidvm/vm_app/build.sh
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install RAID6VM.
```bash
pip install poetry
poetry install
```

# Running Experiments

To initiate the test experiments and observe the RAID-6 system in action, run:

```bash
bash test.sh
```

# Acknowledgement
Mnay thanks to Ruihang's code at https://github.com/RuihangWang/RAID6.
