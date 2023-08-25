# Table of Contents

- [Table of Contents](#table-of-contents)
- [Development notes](#development-notes)
- [STA Pipeline description](#sta-pipeline-description)
  - [Installation (Linux-based system)](#installation-linux-based-system)
  - [Directory structure](#directory-structure)
  - [Example commands](#example-commands)
  - [Software requirements\*](#software-requirements)
  - [Software versions](#software-versions)
- [Outline of the pipeline](#outline-of-the-pipeline)
  - [I. Preprocessing](#i-preprocessing)
  - [II. Particle picking](#ii-particle-picking)
  - [III. Refinement](#iii-refinement)
- [Helpful references](#helpful-references)
    - [Segmenting filaments in 3dmod](#segmenting-filaments-in-3dmod)
    - [IMOD](#imod)
    - [IsoNet](#isonet)
    - [EMAN2](#eman2)
    - [RELION-4.0](#relion-40)
    - [Dynamo](#dynamo)
    - [Visualiziation software](#visualiziation-software)
    - [Misc.](#misc)
    - [Potentially useful tools](#potentially-useful-tools)

# Development notes

For now, add a new file and command for each new function. Later, this can be cleaned up.
 
# STA Pipeline description

Scripts and procedures for a subtomogram averaging (STA) pipeline.

## Installation (Linux-based system)

Open a command-line terminal in the folder you wish to create a directory containing this package. Run the code below to clone the repository. 

`git clone https://git.lobos.nih.gov/dmichalak/sta-pipeline.git`

 Create a new virtual Python environment for using the pipeline and install the package with ``pip``.

`pip install -e sta-pipeline`

## Directory structure

data/
    batch001/
        frames/
        mdoc/

``frames/`` contains all tilt movies in the data batch.
``mdoc/`` contains all of the mdoc files for each tilt series dataset.

After running ``alignframes``, the structure within ``data/batch001`` will be
    frames/
    mdoc/
    ts001/
    ts002/
    ...

where ``ts###`` will refer to each tilt series found in ``mdoc/``.

## Example commands
``sta_pipeline alignframes``\
``sta_pipeline batchruntomo``\
``sta_pipeline ctfplotter``\
``sta_pipeline isonet_setup``\
``sta_pipeline isonet_mask``

...
## Software requirements*

- ``Python 3+``
- [``IMOD``](https://bio3d.colorado.edu/imod/)
- [``IsoNet``](https://github.com/IsoNet-cryoET/IsoNet)
- [``EMAN2``](https://blake.bcm.edu/emanwiki/EMAN2)
- [``RELION``](https://relion.readthedocs.io/en/release-4.0/)

*Scripts and the above software have only been tested on a Linux-based system so far

## Software versions

-- nvidia-driver = 535.86.10
-- CUDA = 12.2
-- RELION = 4.0.1-commmit-0b03a6
# Outline of the pipeline


## I. Preprocessing

Software: ``IMOD``

- Align and sum tilt movies to generate a tilt stack.
- Calculate CTF parameters for each tilt image
- Reconstruct tomograms with a SIRT-like filter
- Reconstruct tomograms with R-weighting (after particle picking)

## II. Particle picking

Software: ``dynamo``, ``IsoNet``, ``EMAN2``, ``RELION`` 

- After initial alignment in ``dynamo``, ``sta-pipeline convert_tbl2star`` to convert ``dynamo`` tables to ``RELION`` star files
- Import into ``RELION``

- Classification with alignment in ``RELION``


- Prepare tomograms for particle picking via denoising and modeling the missing wedge (``IsoNet``)
- Train a neural network to automatically locate densities of interest in tomograms (``EMAN2``)
- Sample subtomogram positions from the trained model predictions
- Clean the subtomogram dataset by removing duplicates, alignment, classification, etc. (``RELION``)

## III. Refinement

Software: ``RELION``

- Extract subtomograms using the cleaned dataset
- Iteratively
    - Refine alignments
    - Classify
    - Refine CTF parameters
    - Refine tilt series alignments
- Postprocessing

# Helpful references


### Segmenting filaments in 3dmod

### IMOD
- [List of programs](https://bio3d.colorado.edu/imod/doc/program_listing.html)
- [alignframes help page](https://bio3d.colorado.edu/imod/doc/man/alignframes.html)
- [batchruntomo help page](https://bio3d.colorado.edu/imod/doc/man/batchruntomo.html)

### IsoNet
- [IsoNet Github](https://github.com/IsoNet-cryoET/IsoNet)

### EMAN2
- [List of programs](https://blake.bcm.edu/doxygen/programs_help_html/)
- [Neural network tutorial](https://blake.bcm.edu/emanwiki/EMAN2/Programs/tomoseg)
- [Computationally friendly box-sizes](https://blake.bcm.edu/emanwiki/EMAN2/BoxSize) \
24, 32, 36, 40, 44, 48, 52, 56, 60, 64, 72, 84, 96, 100, 104, 112, 120, 128, 132, 140, 168, 180, 192, 196, 208, 216, 220, 224, 240, 256, 260, 288, 300, 320, 352, 360, 384, 416, 440, 448, 480, 512, 540, 560, 576, 588, 600, 630, 640, 648, 672, 686, 700, 720, 750, 756, 768, 784, 800, 810, 840, 864, 882, 896, 900, 960, 972, 980, 1000, 1008, 1024

### RELION-4.0
- [Subtomogram tutorial](https://relion.readthedocs.io/en/release-4.0/STA_tutorial/index.html)
- [Reference pages](https://relion.readthedocs.io/en/release-4.0/Reference/index.html)

### Dynamo
- [Standalone installation](https://wiki.dynamo.biozentrum.unibas.ch/w/index.php/Standalone)

### Visualiziation software 
- [Napari](https://napari.org/) - Python-based image viewer
- [ChimeraX Tutorials](https://www.cgl.ucsf.edu/chimerax/tutorials.html)
### Misc.
- [TeamTomo website](https://teamtomo.org/)
- [TeamTomo Github](https://github.com/teamtomo)

### Potentially useful tools

- (**untested**) [imod2relion](https://github.com/ZhenHuangLab/imod2relion) - A tool reading IMOD points, obtaining particles' info and generating .star file for RELION.
- [dynamo2relion](https://github.com/EuanPyle/dynamo2relion) - Converts Dynamo tables to star files for coordinate import into RELION 4.0 
- [relion2dynamo](https://github.com/EuanPyle/relion2dynamo) - Simple package to convert star files to Dynamo tables.
- (**untested**) [membrain-seg](https://github.com/teamtomo/membrain-seg) - membrane segmentation in 3D for cryo-ET
- [mdocfile](https://github.com/teamtomo/mdocfile) - SerielEM mdoc files as pandas dataframes
- [yet-another-imod-wrapper](https://github.com/teamtomo/yet-another-imod-wrapper) - Simple API for automated tilt-series alignment in IMOD