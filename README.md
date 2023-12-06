# Table of Contents

- [Table of Contents](#table-of-contents)
- [STA Pipeline description](#sta-pipeline-description)
  - [Installation (Linux-based system)](#installation-linux-based-system)
  - [Directory structure](#directory-structure)
  - [Software requirements\*](#software-requirements)
- [Outline of the pipeline](#outline-of-the-pipeline)
  - [I. Preprocessing](#i-preprocessing)
  - [II. Particle picking](#ii-particle-picking)
  - [III. Refinement](#iii-refinement)

 
# STA Pipeline description

Scripts and procedures for a subtomogram averaging (STA) pipeline.

## Installation (Linux-based system)

Open a command-line terminal in the folder you wish to create a directory containing this package. Run the code below to clone the repository. 

`git clone https://git.lobos.nih.gov/dmichalak/sta-pipeline.git`

 Create a new virtual Python environment for using the pipeline and install the package with ``pip``.

`pip install -e sta-pipeline`

## Directory structure

data/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;batch001/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;frames/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mdoc/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;batch002/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...

``frames/`` contains all tilt movies in the data batch.
``mdoc/`` contains all of the mdoc files for each tilt series in the batch directory.

After running "``sta-pipeline alignframes_mp``", the structure within ``data/batch001`` will be\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;frames/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mdoc/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ts_001/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ts_002/\
    ...

where ``ts_###`` will refer to a tilt series found in ``mdoc/``.

## Software requirements*

- ``Python 3+``
- [``IMOD``](https://bio3d.colorado.edu/imod/)
- [``IsoNet``](https://github.com/IsoNet-cryoET/IsoNet)
- [``EMAN2``](https://blake.bcm.edu/emanwiki/EMAN2)
- [``RELION``](https://relion.readthedocs.io/en/release-4.0/)

*Scripts and the above software have only been tested on a Linux-based system so far
# Outline of the pipeline


## I. Preprocessing

Software: ``IMOD``

- Align and sum tilt movies to generate a tilt stack.
- Fiducial-based tilt series alignment
- CTF correction
- Reconstruct tomograms with R-weighting

## II. Particle picking

Software: ``IsoNet``, ``EMAN2``, ``RELION`` 

- Prepare tomograms for particle picking via denoising and modeling the missing wedge
- Train a neural network to automatically locate densities of interest in tomograms
- Sample subtomogram positions from the trained model predictions
- Clean the subtomogram dataset by removing duplicates, alignment, classification, etc.

## III. Refinement

Software: ``RELION``

- Extract subtomograms using the cleaned dataset
- Iteratively
    - Refine alignments
    - Classify
    - Refine CTF parameters
    - Refine tilt series alignments
- Postprocessing