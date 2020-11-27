# README _gitlabci_generator_ library

# `.gitlab-ci.yml` automatic generator

## 1 - Create the `.gitlab-ci.yml` file

1 - Incorporate the `gitlabci_generator` [directory](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/tree/reorganize_repo/gitlabci_generator)
 to the root directory of your project.
  - Or download it by clicking [here (zip)](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/archive/reorganize_repo/template_project_escape-reorganize_repo.zip?path=gitlabci_generator), 
  [here (tar)](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/archive/reorganize_repo/template_project_escape-reorganize_repo.tar?path=gitlabci_generator),
  or [here (tar.gz)](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/archive/reorganize_repo/template_project_escape-reorganize_repo.tar.gz?path=gitlabci_generator). 

2 - Go to the `gitlabci_generator` folder,
```sh
  $ cd gitlabci_generator
```

3 - **READ** and edit the `ci-config.yml` file 
 - only 8 entries to edit/modify.

4 - run;

```sh
  $ python generator_gitlab_ci_files.py
```  


## 2 - Make the gitlab CI pipeline work

By running the above commands you will have created the `.gitlab-ci.yml` file. You will still need to;

1 - [***OPTIONAL***] If you want to create a Singularity container of your project using the gitlab CI pipeline;
   - Include the [`.gitlabci` directory](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/tree/master/.gitlabci) 
   into the root directory of your project. 
     * Or download it by clicking [here (zip)](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/archive/master/template_project_escape-master.zip?path=.gitlabci),
     [here (tar)](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/archive/master/template_project_escape-master.tar?path=.gitlabci),
   or [here (tar.gz)](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/archive/master/template_project_escape-master.tar.gz?path=.gitlabci)).
   

2 - Include the [`.zenodoci` directory](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/tree/reorganize_repo/.zenodoci) into the root directory of your project. 
  - Or download it by clicking 
  [here (zip)](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/archive/reorganize_repo/template_project_escape-reorganize_repo.zip?path=.zenodoci), 
  [here (tar)](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/archive/reorganize_repo/template_project_escape-reorganize_repo.tar?path=.zenodoci), 
  or [here (tar.gz)](https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape/-/archive/reorganize_repo/template_project_escape-reorganize_repo.tar.gz?path=.zenodoci). 
 -  Adapt / modify the `./zenodoci/repository_information.json` file with the metadata of your repository.

3 - Allow the gitlab CI pipeline communicate with the (sandbox)Zenodo API. To do so;
   - 3.1. Create a personal access token;
   
     *  Go to (sandbox)zenodo.org
     * `Account` --> `Applications` --> `Personal access token` --> `New token`.
   - 3.2. Include this token into your project. This token will be passed later in the `deploy` stage of the CI pipeline. 
   For not sharing publicly your personal token, you *MUST* create an environment variable. This way, the token will be
   used as a variable without revealing its value. To create an an environment variable:
     * Go to your GitLab project.
     * `Settings` --> `CI/CD` --> `Variables` --> `Add variable` --> Fill the fields --> Mask your variable(s) !!
     * To avoid modifying the `.gitlab-ci.yml` file, we encourage to use environment variable names such as;
        * `ZENODO_TOKEN`
        * `SANDBOX_ZENODO_TOKEN`
        * `ZENODO_PROJECT_ID`  
     
## Last step
 - Now you can push all the changes to your git instance.   
 
 ------------
 
 ![gitlabCI diagram](https://escape2020.pages.in2p3.fr/wp3/ossr-pages/img/ESCAPE_OSSR_diagram.png 
 "Schema showing the CI gitlab pipeline. ")