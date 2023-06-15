# STA Pipeline

Scripts and procedures for a subtomogram averaging (STA) pipeline used in the CZI-funded project "Correlative cryo-electron tomography pipeline of plasma membrane complexes."

![tomogram example](images/tomo_image_cropped.png)
(placeholder image)

## Software requirements*

- ``Python 3+``
- [``IMOD``](https://bio3d.colorado.edu/imod/)
- [``fidder``](https://github.com/teamtomo/fidder)
- [``IsoNet``](https://github.com/IsoNet-cryoET/IsoNet)
- [``EMAN2``](https://blake.bcm.edu/emanwiki/EMAN2)
- [``Dynamo``](https://wiki.dynamo.biozentrum.unibas.ch/w/index.php/Main_Page)
- [``RELION``](https://relion.readthedocs.io/en/release-4.0/)

*Scripts and the above software have only been tested on a Linux-based system so far

## I. Preprocessing

Software: ``IMOD``, ``fidder``

- Align and sum tilt movies to generate a tilt stack.
- Fiducial-based tilt series alignment
- CTF correction
- Mask and erase fiducials prior to reconstruction
- Reconstruct tomograms with R-weighting

## II. Particle picking

Software: ``IsoNet``, ``EMAN2``, ``Dynamo``, ``RELION`` 

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

***
<!---
## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.
