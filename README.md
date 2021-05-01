# Quantifying the structural uncertainty of the aerosol mixing state representation in a modal model
[![DOI](https://zenodo.org/badge/363034210.svg)](https://zenodo.org/badge/latestdoi/363034210)

## Introduction

This repository is a supplementary to the manuscript **"Quantifying the structural uncertainty of the aerosol mixing state representation in a modal model"**.

## Scripts and Data

### Prerequisite

- If you do not have the **"[conda](https://docs.conda.io/en/latest/)"** system

```bash
# Download and install conda
$ wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ chmod +x Miniconda3-latest-Linux-x86_64.sh
$ ./Miniconda3-latest-Linux-x86_64.sh
# Edit .bash_profile or .bashrc
PATH=$PATH:$HOME/.local/bin:$HOME/bin:$HOME/miniconda3/bin
# Activate the conda system
$source .bash_profile
# OR source .bashrc
```

- Create and activate your own conda environment

```bash
# Create an environment "partmc" and install the necessary packages
conda env create -f environment.yml
# Activate the "partmc" environment
conda activate partmc_mam4
```

### Scripts

| Tasks                                   | Folders            | Fig or Tab in paper      |
| --------------------------------------- | ------------------ | ------------------------ |
| get the particle-resolved $\chi$        | 0_get_particle_chi | Tab 3                    |
| calculate the $\chi$ from a modal model | 1_get_modal_chi    |                          |
| processing the data                     | 2_preprocessing    |                          |
| data analysis                           | 3_analysis         | Fig 2 - Fig 5, Fig S1 - Fig S2 |

### Data

| Folders or Files    | Usage                                                |
| ------------------- | ---------------------------------------------------- |
| train.csv, test.csv | for 0_get_particle_chi                               |
| ml_chi              | mixing state indices estimated by 0_get_particle_chi |
| mam4_chi            | mixing state indices calculated by 1_get_modal_chi   |
| mam4_minus_ml_chi   | difference between ml_chi and mam4_chi               |
| comp_analysis       | composition analysis                                 |
| mask                | masks for the hatched areas                          |

## Acknowledgements

- We would like to acknowledge high-performance computing support from Cheyenne (doi:10.5065/D6RX99HX) provided by NCAR's Computational and Information Systems Laboratory, sponsored by the National Science Foundation. 
- The CESM project is supported primarily by the National Science Foundation. 
- This research is part of the Blue Waters sustained-petascale computing project, which is supported by the National Science Foundation (awards OCI-0725070 and ACI-1238993) the State of Illinois, and as of December, 2019, the National Geospatial-Intelligence Agency. Blue Waters is a joint effort of the University of Illinois at Urbana-Champaign and its National Center for Supercomputing Applications. 
- We also acknowledge funding from DOE grant DE-SC0019192 and NSF grant AGS-1254428. 
- P.-L. Ma and X. Liu were supported by the "Enabling Aerosol-cloud interactions at GLobal convection-permitting scalES (EAGLES)" project (74358), funded by the U.S. Department of Energy, Office of Science, Office of Biological and Environmental Research, Earth System Model Development program. The Pacific Northwest National Laboratory is operated for the U.S. Department of Energy by Battelle Memorial Institute under contract DE-AC05-76RL01830.
