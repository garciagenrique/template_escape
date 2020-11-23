# ESCAPE metadata template

In the ESCAPE project we will be following the ***CodeMeta*** project and schema to describe metadata.

## Quickstart

 1. Go to the [CodeMeta generator](https://codemeta.github.io/codemeta-generator/). Create a `codemeta.json` file based on your library/repository.
    - Check in the same web application that the generate / your own file is valid !  
 2. Include the `codemeta.json` file in the root directory of your project.
 3. To automate the upload to the [ESCAPE repository](https://zenodo.org/communities/escape2020) through the GitLab-CI pipelines
    - Include the `.zenodoci` library in the root directory of your project.
    - Configure the pipeline (Quikstart and tutorials [here](https://escape2020.pages.in2p3.fr/wp3/ossr-pages/page/repository/publish_in_repository/)).
    
-----------------
-----------------
 
 
## Create a Zenodo metadata file from the CodeMeta schema

The zenodo repository does not accept codemeta metadata files yet. In the meanwhile, this library provides a simple tool
to create a native Zenodo metadata file (`.zenodo.json`) from a `codemeta.json` file. To do so;

 1. Include a `codemeta.json` file to the root directory of your project.
 2. Run the following command;
````bash
$ python codemeta_utils/codemeta_to_zenodo_json.py
````
 3. In case of doubts or problems, please [contact us](mailto:garcia@lapp.in2p3.fr).


## Metadata schema templates

Inside the `codemeta_utils` directory you will find two template files with **the all the terms of the corresponding metadata schema context** 
 for both the CodeMeta metadata file and the Zenodo metadata file.
 
Feel free to create and incorporate the metadata files starting from these templates. However, please note that  
the final filenames **MUST** be either `codemeta.json` or `.zenodo.json` (note the `.` !). In case you do not fill a key field, take it out of the file.

In case of doubts please also check;
  - The [CodeMeta terms description](https://codemeta.github.io/terms/) or,
  - the [`metadata representation`](https://developers.zenodo.org/#representation) allowed for the `.zenodo.json` metadata file.
  
  
### Extending the CodeMeta Context schema

In case you find that CodeMeta context does not describe deep enough your project, you can extend the metadata context 
and combine it with all the terms available in [https://schema.org](https://schema.org/docs/full.html).
For this purpose, and following the [CodeMeta's developer guide](https://codemeta.github.io/developer-guide/);

   1. Modify the `"@Context"` key of the `codemeta.json` as; 
    
    "@context": ["https://raw.githubusercontent.com/codemeta/codemeta/2.0-rc/codemeta.jsonld", "http://schema.org/"]
     
   2. Include the desired terms / properties following the `schema.org` context.
   3. Contact us for a likely implementation into the OSSR environment :-)


## Automate the metadata schema in the OSSR environment.

The `ZenodoCI` project contains a copy of the code in this library !


This means that if you have already configured the GitLabCI pipeline together with the Zenodo repository, the CI 
pipeline will take care of creating a `.zenodo.json` file automatically and incorporate it to the new upload/new 
version to Zenodo.