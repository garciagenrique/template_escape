# .gitlabci

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3834833.svg)](https://doi.org/10.5281/zenodo.3834833)

**PLEASE HAVE A LOOK TO THE LICENSING SECTION BELOW BEFORE IMPLEMENTING ANY PART OF THIS CODE INTO YOURS !!**

## Building Singularity Containers using the continuous integration in GitLab 

The source code contained in this folder is based on the following 
[GitLab-CI repository](https://gitlab.com/singularityhub/gitlab-ci). You can  find a very didactic **tutorial** of how 
to implement this code [here](https://vsoch.github.io/2018/gitlab-singularity-ci/).

This software (composed of the files within this directory **AND** part of the the `.gitlab-ci.yml` file in the
root directory - the `build_image` stage) provide the necessary tools to:
 - Use a container image stored in the DockerHub site to create a Singularity container of your repository 
 (thus no need of having installed the Singularity source code), and upload it directly to your GitLab repository.
 - The Singularity recipe must be provided, of course.
 - In case the container is too large (10 Gb total storage limit for a single GitLab project), you must pass 
 through a cloud service (various examples of different services are shown in the tutorial and the original repository). 

## License of the `template_project_repository`:
The `template_project_repository` contains code from different projects. This 'mixing' can be done because:
 - Both 'parent' projects are Open Source.
 - None of the original licenses are copy-left.
 - Both `BSD 3-Clause` and `MIT`, are permissive licenses. All of these points mean that source code distributed with 
 a BSD 3-Clause license can be included in a project with a MIT license - and of course be re-distributed under `MIT`:
    - Note however, that the **original licenses** must be included in the resulting project and mentioned in the 
    LICENSE/documentation files.  

**PLEASE TAKE THE TIME TO CHECK AND VERIFY LICENSES AND THEIR COMPATIBILITIES** 
 