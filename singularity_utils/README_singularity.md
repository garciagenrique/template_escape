# Singularity container
 
This directory contains all what you need to create a singularity image of the current repository.
 
1. Install singularity on your computer:
    - [Install Singularity on Linux.](https://sylabs.io/guides/3.5/admin-guide/installation.html#installation-on-linux)
    - [Install Singularity on Mac or Windows.](https://sylabs.io/guides/3.5/admin-guide/installation.html#installation-on-windows-or-mac)

2. Run the script that creates the Singularity image:

```console
  $ cd singularity
  $ ./create_singularity_image.sh
``` 

The script will build an image of the repository by using an easy home-made Singularity recipe (`*.recipe`).  

Staring from an [Ubuntu container from the dockerhub](https://hub.docker.com/_/ubuntu):
 - It will download and install miniconda3.
 - It will create, configure and activate a conda environment based on the dependencies of the repository.
 - It will clone and install the latest tag of the current git repository.   
 
 ## Feel free to copy / base on this recipe !
  - You can also find in the [Singularity user guide](https://sylabs.io/guides/3.5/user-guide/) a tutorial of the program.
