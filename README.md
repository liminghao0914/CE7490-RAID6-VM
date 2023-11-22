# RAID-6 Based Distributed Storage System

This project, part of CE7490 Advanced Topics in Distributed Systems, focuses on the implementation and analysis of a RAID-6 based distributed storage system.

# Introduction

RAID-6, also referred to as double-parity RAID, enhances data storage reliability by distributing data and parity across multiple disks. This configuration allows for two disk failures within the array without any data loss. It's a step above RAID-5 by adding an additional layer of redundancy.

In our implementation, we've utilized advanced coding techniques based on Vandermonde-RS code. By leveraging Python 3.7 and libraries such as `numpy`, we've been able to implement efficient Galois Field arithmetic and matrix operations which are critical for RAID-6 functionality.

The system is designed with six primary functions: distributing data storage, handling data updates, disk failure detection, data restoration, and data object retrieval.

![RAID-6 System Architecture](/images/system_architecture.png) *// Image showing the system architecture.*


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
python test.py 
```

Upon execution, the system will demonstrate the RAID-6 operations, and the performance metrics will be displayed:

```
Read time: 0.08199000358581543 seconds
Write time: 3.647477149963379 seconds
Rebuild time: 8.104788064956665 seconds
```

These metrics offer insight into the system's performance, highlighting the efficiency of data reading, writing, and rebuilding processes.

# Visualization

The project report includes various images that demonstrate the system's flow and architecture:

![RAID-6 Data Flow](/images/flow.png) *// Image illustrating the data flow within the RAID-6 system.*

For more detailed visualizations and explanations, refer to the project report `RAID_6_Based_Distributed_Storage_System.pdf`.

# Further Work and Contributions

The project is open for further development and contributions. Future work may include:

- Enhancing the efficiency of Galois Field computations.
- Expanding the system to support more complex data operations.
- Improving the user interface for managing and monitoring the RAID-6 system.
- Integrating additional machine learning algorithms for predictive disk failure analysis.

Contributors can fork the repository, make their changes, and submit a pull request for review.


