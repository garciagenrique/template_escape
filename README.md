# template_project_escape 
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3884963.svg)](https://doi.org/10.5281/zenodo.3884963) 
[![pipeline status](https://gitlab.in2p3.fr/escape2020/escape/template_project_escape/badges/master/pipeline.svg)](
https://gitlab.in2p3.fr/escape2020/escape/template_project_escape/-/commits/master)
[![Build Status](https://travis-ci.com/garciagenrique/template_project_escape.svg?branch=master)](
https://travis-ci.com/garciagenrique/template_project_escape)
[![License: MIT](https://img.shields.io/badge/License-MIT-indigo.svg)](https://opensource.org/licenses/MIT)


<p align="center">
   <img src="https://cdn.eso.org/images/large/ann18084a.jpg" width="640" height="453"/>
</p>

A simple template project to provide software to ESCAPE.

The repository shows the **basic documentation** that should be included within the project (following the 
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

Take few minutes to check the [ESCAPE repository's guidelines](https://gitlab.in2p3.fr/escape2020/guidelines) too.

# Contributing guidelines for the ESCAPE repository

If you wish to provide software to the ESCAPE repository: 

 - You should ask developer access through the Gitlab interface and send an email to vuillaume [at] lapp.in2p3.fr with
  your institution email.

 - You will then be able to open a new project and transfer code.

 - All the code provided should be uploaded from the [Zenodo ESCAPE community](https://zenodo.org/communities/escape2020/). 

 - For a detailed explanation of how to submit a contribution to a project / repository (Fork, create a branch, make
  a pull request...), please check the [opensource guide](https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution) 
  and/or the [git's documentation](https://git-scm.com/doc).

 - Once you are granted with developer access, you will be able to add a new blank project / import it (from other
  common repository managers, i.e., GitHub, GitLab, Bitbucket, Fogbugz...) to the
   [GitLab/ESCAPE](https://gitlab.in2p3.fr/escape2020) main page.

***PLEASE NOTE*** that if you have login GitLab by using the `[Shibbolenth]` service (eduGAIN, Fédération d'Identités 
RENATER), you will need to [add a SSH key](https://gitlab.in2p3.fr/help/ssh/README#generating-a-new-ssh-key-pair) to 
your GitLab profile if you want to 'push' your changes to the server. 

# Singularity image container and CI/CD to Zenodo

An example of how to; 
 1. create a Singularity image / container of your code, 
 2. make it available as a downloadable artifact within your project and 
 3. add it to the ESCAPE community in the [Zenodo repository](https://zenodo.org/communities/escape2020), 
 
can be found in the `.gitlabci`, `.zenodoci` directories and in the `.gitlab-ci.yml` file. Please read carefully 
all the README files.  

For an easy example of how to create a Singularity receipt from scratch (and its corresponding container when executed),
please have a look to the `singularity_utils` directory. 

# Installation

```sh
  $ git clone https://gitlab.in2p3.fr/escape2020/escape/template_project_escape.git
  $ cd template_project_escape
  $ python setup.py install
``` 

This is an easy method to install the current project. 
You can also check other more elaborated ways - generally for bigger repositories - here (e.g.,
 [cta-observatory/cta-lstchain](https://github.com/cta-observatory/cta-lstchain), 
 [cta-observatory/ctapipe](https://github.com/cta-observatory/ctapipe)).

# Citing 
In case of citing this repository, use the following DOI:
 - v2.0 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3884963.svg)](https://doi.org/10.5281/zenodo.3884963)

Do not forget to include your code / container into the [Zenodo ESCAPE community](https://zenodo.org/communities/escape2020/). 
 - ***Note that*** you will be able to assign a DOI in the moment you include your code/repository to Zenodo. 
 
Please check the licenses of the code within in the `.gitlabci`, `.zenodoci` directories before adding this template 
to your project.

# Report an issue / Ask a question
Use the [GitLab repository Issues](https://gitlab.in2p3.fr/escape2020/escape/template_project_escape/-/issues).

# Contact
Email to vuillaume [at] lapp.in2p3.fr / garcia [at] lapp.in2p3.fr.
