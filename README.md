# template_project_escape 
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4790629.svg)](https://doi.org/10.5281/zenodo.4790629) 
[![pipeline status](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/badges/master/pipeline.svg)](
https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/commits/master)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)


<p align="center">
   <img src="https://cdn.eso.org/images/large/ann18084a.jpg" width="640" height="453"/>
</p>

A simple template project to provide software to ESCAPE.

This repository shows the **basic content** that should be included in a project (following the 
[opensource guide](https://opensource.guide/starting-a-project/)):

* An [open source](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/licensing-a-repository#where-does-the-license-live-on-my-repository)
 **license**.
* A [**README** file](https://help.github.com/en/github/getting-started-with-github/create-a-repo#commit-your-first-change),
 similar to this one. 
* Contributing guidelines. 
    - See below the general guidelines for the ESCAPE repository.
* A [code of conduct](https://opensource.guide/code-of-conduct/).
    - Check why is a good idea to add one.
* The repository itself.

It would be highly suitable to include too:
   - A setup file as well as the basic commands to install the library (see below).
   - A `.gitignore` file.
   - Unitary and integration tests, and ideally a CI pipeline.
   
**Please feel free to clone / fork / template this project!** (For example, look to left of the 
`Clone or download` button in the [GitHub](https://github.com/garciagenrique/template_project_escape) site).

  - For a detailed explanation of how to submit a contribution to a project / repository (Fork, create a branch, make
  a pull request...), you can have a look to the [opensource guide](https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution) 
  and/or the [git's documentation](https://git-scm.com/doc).
  - Not that if you have login GitLab by using the `[Shibbolenth]` service (eduGAIN, Fédération d'Identités 
  RENATER), you will need to [add a SSH key](https://gitlab.in2p3.fr/help/ssh/README#generating-a-new-ssh-key-pair) to 
  your GitLab profile if you want to 'push' your changes to the server. 

# Contribute to the ESCAPE OSSR

If you want to provide software to the ESCAPE repository: 

 - Check the [ESCAPE OSSR guidelines](https://escape2020.pages.in2p3.fr/wp3/ossr-pages/page/contribute/contribute_ossr/).
    - For ESCAPE members, follow the steps detailed in [the onboarding project](https://gitlab.in2p3.fr/escape2020/wp3/onboarding)
    to finalise your contribution and the same onboarding process.

 - All the code provided should be uploaded to the [Zenodo ESCAPE community](https://zenodo.org/communities/escape2020/).
 
 - Check the following [tutorial on how to publish content in Zenodo](https://escape2020.pages.in2p3.fr/wp3/ossr-pages/page/contribute/publish_tutorial/), 
   and how to automatise the upload of each new release of your project. 

# This project also includes

## 1. How to automatise the building of a Singularity image and upload it to Zenodo using the GitLab-CI

A working example of how to automatise the GitLab-CI to; 
 1. create a Singularity image / container of your code, 
 2. make it available as a downloadable artifact within your project and 
 3. upload it to the [ESCAPE OSSR](https://zenodo.org/communities/escape2020), 
 
can be found in the `.singularityci`, and `Singularity` directories and in the `.gitlab-ci.yml` file - the 
`build_singularity_image` stage. Please read carefully all the README files.  

For an easy example of how to create a Singularity receipt from scratch (and its corresponding container when executed),
please have a look to the `singularity_utils` directory.

## 2. How to automatise the building of a Docker container and upload it to the GitLab Container Registry

An example can be found in the `Docker` directory and in the `.gitlab-ci.yml` file -  the 
`build_docker_image` stage. 

# Install
Example of how to show installing instructions (and indeed the way to install this project).

```sh
  $ git clone https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape.git
  $ cd template_project_escape
  $ pip install .
``` 

# Citing 
Example of citing (as well as the DOI to cite this project),

In case of citing this repository, use the following DOI:
 - v2.1 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4790629.svg)](https://doi.org/10.5281/zenodo.4790629)
 - v2.0 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3884963.svg)](https://doi.org/10.5281/zenodo.3884963)
 - v1.1 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3743490.svg)](https://doi.org/10.5281/zenodo.3743490)
 - v1.0 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3572655.svg)](https://doi.org/10.5281/zenodo.3572655) 

Do not forget to include your code / container into the [Zenodo ESCAPE community](https://zenodo.org/communities/escape2020/). 
 - ***Note that*** a DOI will be assigned in the moment create a new record/entry in Zenodo. 
 
# License 

Please check the licenses of the code within the `.singularityci` directory before adding this template 
to your project.

# Report an issue / Ask a question
Use the [GitLab repository Issues](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/issues).

# Contact
Email to vuillaume [at] lapp.in2p3.fr / garcia [at] lapp.in2p3.fr.
