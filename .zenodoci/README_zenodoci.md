# .zenodoci

**PLEASE HAVE A LOOK TO THE LICENSING SECTION BELOW BEFORE IMPLEMENTING ANY PART OF THIS CODE INTO YOURS !!**

## Continuous Deployment to Zenodo

The source code contained in this folder is based on the  
[zenodo-python repository](https://github.com/SiLeBAT/zenodo-python).

The software (composed of the `zenodolib.py` script) provides a library to handle the upload of a 
specified file(s) to (sandbox)zenodo. Please **JUST** upload stable versions/releases of source code and/or images
 containers!

By using the `zenodolib` library, as well as the created Singularity container (check the `.gitlabci` directory), 
the second stage of the CI pipeline (see the `.gitlab-ci.yml` file) will:
 - Either upload the desired file(s) to the ESCAPE community in Zenodo.
 - Either upload a new version of an existing entry to Zenodo.
 
The `repository_information.json` file must be filled up before pushing to the project repository. Also, depending on 
the case, the corresponding python script (`upload_new_deposit.py` or `upload_new_version_of_deposit.py`) must be 
 adapted and included into the `.gitlab-ci.yml` file with its corresponding arguments.

### Zenodo token & GitLab CI environment variable

To connect the GitLab repository with Zenodo in an autonomous way, a personal access token must be created. This token 
is assign to a **single** Zenodo account, and it will allow to interact with (sandbox)zenodo through its 
API. To create the token:
 - Go to (sandbox)zenodo.org
 - Account --> Applications --> Personal access token --> New token. 
 
This token will be passed later in the continuous deployment stage of the CI/CD pipeline. For not sharing publicly 
your personal token, you should create an environment variable in your GitLab repository. This way, the token could be used as a variable without
 revealing its value. To create an an environment variable:
  - Go to your GitLab repository.
  - Settings --> CI/CD --> Variables --> Add variable --> Fill the fields --> Mask and protect the variable !

The environment variable will look like this:

```sh
    $ python .zenodoci/upload_new_deposit.py -i build/Singularity -t $ZENODO_TOKEN
```

## License of the repository

The license of the 'parent' repository is `GNU GENERAL PUBLIC LICENSE Version 3` ("GNU GPL v3" or "GPLv3"). Before 
implementing anything from the current or the original repository **please check that the license of the project 
in which you are going to implement these source files is compatible with the GPLv3 license**.

If this is the case: 
 - The whole resulting project must be distributed with the same license, i.e., `GPLv3` and contain the license
  and copyright notice (see the LICENSE file of the `template_project_repository`). GPLv3 is copyleft.
 - Changes must be stated (here is an example of the kind of text that must be included in each modified file): 
 
> This code is part of https://github.com/SiLeBAT/zenodo-python 
> 
> Copyright (c) 2015 Federal Institute for Risk Assessment (BfR), Germany
> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
>
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License
> along with this program.  If not, see <http://www.gnu.org/licenses/>.


### Specific case of the `template_project_repository`:
The `template_project_repository` contains code from different projects. This 'mixing' can be done because:
 - Both 'parent' projects are Open Source.
 - Both licenses, `BSD 3-Clause` and `GPLv3`, are [compatible](
 https://www.gnu.org/licenses/gpl-faq.html#WhatDoesCompatMean); this means that source code distributed with a BSD 
 3-Clause license can be included within a project with a GPLv3 license:
    - Note however that the GNU General Public License v3 is 'copyleft', meaning that the resulting project from the use
     of any code licensed with GPLv3, must be distributed with the same license, thus GPLv3.
 
This are the reasons why the  `template_project_repository` is distributed with the GNU General Public License Version 
3 and some files contain a BSD-3 Clause license.

**PLEASE TAKE THE TIME TO CHECK AND VERIFY LICENSES AND THEIR COMPATIBILITIES** 
 