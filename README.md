# template_project_escape
<p align="center">
   <img src="https://cdn.eso.org/images/large/ann18084a.jpg" width="640" height="453"/>
</p>

A simple template project to provide software to ESCAPE.

It shows the **basic documentation** a project should include, following the [opensource guide](https://opensource.guide/starting-a-project/):

* An [open source](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/licensing-a-repository#where-does-the-license-live-on-my-repository) **license**.
* A [**README** file](https://help.github.com/en/github/getting-started-with-github/create-a-repo#commit-your-first-change), similar to this one. 
* Contributing guidelines. 
    - See below the general guidelines for the ESCAPE repository.
* A [code of conduct](https://opensource.guide/code-of-conduct/).
    - Check why is a good idea to add one.
* The structure of the repository.



- It would be highly suitable to include too:
   - A setup file as well as the basic commands to install the library (see below).
   - A .gitignore file.
   - Unitary and integration tests.
   
**Please feel free to copy / base on / template this project!** (Look to left of the `Clone or download` button in the [GitHub](https://github.com/garciagenrique/template_project_escape) site).

Take few minutes to check the [ESCAPE repository's guidelines](https://gitlab.in2p3.fr/escape2020/guidelines) too.

# Contributing guidelines for the ESCAPE repository

If you wish to provide software to the ESCAPE repository, you should ask developer access through the Gitlab interface and send an email to vuillaume [at] lapp.in2p3.fr with your institution email.

You will then be able to open a new project and transfer code.

All the code provided should be uploaded from the [zenodo ESCAPE community](https://zenodo.org/communities/escape2020/). 

For a detailed explanation of how to submit a contribution to a project / repository (Fork, create a branch, make a pull request...), please check the [opensource guide](https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution) and/or the [git's documentation](https://git-scm.com/doc).

Once you are granted with developer access, you will be able to add a new blank project / import it (from other common repository managers, i.e., GitHub, GitLab, Bitbucket, Fogbugz...) to the [GitLab/ESCAPE](https://gitlab.in2p3.fr/escape2020) main page.

-  ***PLEASE NOTE*** that if you have login GitLab by using the `[Shibbolenth]` service (eduGAIN, Fédération d'Identités RENATER), you will need to [add a SSH key](https://gitlab.in2p3.fr/help/ssh/README#generating-a-new-ssh-key-pair) to your GitLab profile if you want to 'push' your changes to the server. 

# Installation

```sh
  $ git clone https://gitlab.in2p3.fr/escape2020/escape/template_project_escape.git
  $ cd template_project_escape
  $ python setup.py install
``` 

This is an easy method to install the library. 
You can also check other more elaborated ways - generally for bigger repositories - here (e.g., [cta-observatory/cta-lstchain](https://github.com/cta-observatory/cta-lstchain), [cta-observatory/ctapipe](https://github.com/cta-observatory/ctapipe)).

# Citing 
Please do not forget to cite the ESCAPE repository ! 
<p align="center">ESCAPE DOI will be available soon !</p>

# Report an issue / Ask a question
Use [GitLab Issues](https://gitlab.in2p3.fr/groups/escape2020/-/issues).

# Contact
Email to vuillaume [at] lapp.in2p3.fr / garcia [at] lapp.in2p3.fr.
