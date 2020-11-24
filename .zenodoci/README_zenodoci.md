# .zenodoci

**PLEASE HAVE A LOOK TO THE LICENSING SECTION BELOW BEFORE IMPLEMENTING ANY PART OF THIS CODE INTO YOURS !!**

## Continuous Deployment to Zenodo

Library to manage an upload to Zenodo through its REST API.

The source code contained in this folder is based on the [ZenodoCI](https://gitlab.in2p3.fr/escape2020/wp3/zenodoci) 
project. The library was developed specifically to perform a deploy stage (to the Zenodo repository) in a GitLab CI 
pipeline that **could be implemented in any external project**. 
  

The library (composed of the scripts within the `.zenodoci` directory) provides a module to handle the upload of 
specified file(s) to (sandbox)zenodo. Please **JUST** upload stable versions/releases of source code and/or image
 containers!

The `deploy` stage in the CI pipeline (see the `.gitlab-ci.yml` file) will make use of the `zenodoapi` library and
 the built Singularity container created in the previous CI stage (check the `.gitlabci` directory too) to:
 - Either upload the desired file(s) to the ESCAPE community in Zenodo.
 - Either upload a new version of an existing entry to Zenodo.
 
A `codemeta.json` metadata file (see below) **MUST BE ADDED** before uploading an entry to Zenodo or triggering the GitLabCI pipeline. 
 
Also, depending on the case, the corresponding python script (`upload_new_deposit.py` or `upload_new_version_of_deposit.py`) 
must be adapted and included into the `.gitlab-ci.yml` file with its corresponding arguments (examples are shown in the yml file). 

#### **Use of new metadata context ! Please check the news !**

    We are no longer supporting the use of a `repository_information.json` file to provide metadata to Zenodo.

We are currently moving to a [CodeMeta metadata context](https://codemeta.github.io/).
 This metadata standard provides a complete metadata schema context supported by many other services and search engines.   

Adding a single `codemeta.json` file to the root directory of your project will be enough ! Please check out the
[ESCAPE metadata template](https://gitlab.in2p3.fr/escape2020/wp3/escape_metadata_template) project for a _quickstart_ on
how to easily create a `codemeta.json` file. 

Last but not least ! Please note that during the CI pipeline the `.zenodoci` module will search for a `codemeta.json` file
and will automatically create the equivalent file to provide metadata to the Zenodo repository. The `.zenodo.json` file
will contain the exactly same information that in the `codemeta.json` file but using the Zenodo syntax. 


## Zenodo token & GitLab CI environment variable

To connect the GitLab repository with Zenodo in an autonomous way, a personal access token must be created. This token 
is assigned to a **single** Zenodo account, and it will allow the interaction with
 (sandbox.)zenodo through its API. To create the token:
 - Go to (sandbox)zenodo.org
 - Account --> Applications --> Personal access token --> New token. 
 
This token will be passed later in the deployment stage of the CI pipeline. For not sharing publicly 
your personal token, you should create an environment variable in your GitLab repository. This way, the token could be
 used as a variable without revealing its value. To create an an environment variable:
  - Go to your GitLab repository.
  - Settings --> CI/CD --> Variables --> Add variable --> Fill the fields --> Mask your variable(s) !!

The environment variable will look like this:

```sh
    $ python .zenodoci/upload_new_deposit.py --input-directory build --token $ZENODO_TOKEN --sandbox_zenodo False
```

## License of the `template_project_repository`:
The `template_project_repository` contains code from different projects. This 'mixing' can be done because:
 - Both 'parent' projects are Open Source.
 - None of the original licenses are copy-left.
 - Both `BSD 3-Clause` and `MIT`, are permissive licenses. All of these points mean that source code distributed with 
 a BSD 3-Clause license can be included in a project with a MIT license - and of course be re-distributed under `MIT`:
    - Note however, that the **original licenses** must be included in the resulting project and mentioned in the 
    LICENSE/documentation files.  
     
     
**PLEASE TAKE THE TIME TO CHECK AND VERIFY LICENSES AND THEIR COMPATIBILITIES** 
 