# RAID6VM: Implement RAID-6 distributed storage system on multiple virtual machines

We implement _RAID6VM: Implement RAID-6 distributed storage system on multiple virtual machines._ for CE7490 project 2.

Code contriutors: [Minghao LI](https://github.com/liminghao0914), [Tianwen ZHU](https://github.com/tianwen1209).

<p align="center">
  <img width="460" src="/imgs/RAID_6.png">
</p>

# Introduction

The system is designed with six primary functions: storage, update, failure detection, restoration, and retrieval. 
Instead of using folders to emulate nodes, extend the implementation to work across multiple virtual machines (VM) to realize a peer-to-peer RAIN. 
We use the OS-level virtualization techniques to start the VMs.

<p align="center">
  <img width="100%" src="/imgs/r6vm_sys.png">
</p>


# Installation
### VM 
- Docker version 24.0.2, build cb74dfc

### Python
- python==3.9.0

  
## Dependencies
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
