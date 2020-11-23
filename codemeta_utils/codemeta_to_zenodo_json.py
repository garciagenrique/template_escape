# -*- coding: utf-8 -*-
#
# Enrique Garcia. Nov 2020.
# email: garcia 'at' lapp.in2p3.fr

import os
import sys
import json
from pathlib import Path
from distutils.util import strtobool


def parse_person_schema_property(person_property, contributor_field):
    """
    Parse the Person Schema property correctly

    Parameters:
    --------
    person_property: dict
        dictionary codemeta key with the a list or a single Person property item.
    contributor_field : str
        contributor type {'editor', 'producer', 'sponsor'} or publisher, although the last one can only happen if
        `upload_type` is publication (NOT SUPPORTED - contact E. Garcia by email).

    Returns:
    --------
    zenodo_person: dict
        dictionary with the correct zenodo syntax for all {author, contributor, maintainer}.
    """
    zenodo_person = {}
    special_contributor_cases = ['editor', 'producer', 'publisher', 'provider', 'sponsor']

    name = person_property['familyName']
    if 'givenName' in person_property:
        name += f', {person_property["givenName"]}'
    zenodo_person['name'] = name

    if "@id" in person_property:
        if 'orcid.org/' in person_property["@id"]:   # "https://orcid.org/0000-0002-5686-2078" format not accepted
            zenodo_person['orcid'] = person_property["@id"].split('orcid.org/')[-1]
        else:
            zenodo_person['orcid'] = person_property["@id"]

    if "affiliation" in person_property:
        zenodo_person['affiliation'] = person_property['affiliation']['name']

    # Parse correctly the contributors
    if contributor_field in special_contributor_cases:

        if contributor_field is 'provider' or contributor_field is 'publisher':
            zenodo_person['type'] = 'Other'
        else:
            try:
                zenodo_person['type'] = person_property["type"]
            except:
                zenodo_person['type'] = contributor_field

    return zenodo_person


def add_author_metadata(zenodo_file, codemt_file, field):
    """
    Aux function to parse correctly all the authors, contributors and maintainers that can be found at the
    codemeta.json file

    zenodo_file: dict
        metadata dictionary with the zenodo syntax
    codem_file: list or dict
        metadata dictionary key field with the codemeta syntax
    field: str
        codemeta key field specifying creator {author, contributor, maintainer, creator}, or
        contributors {editor, sponsor, producer, project manager...}

    """
    full_contacts = {}

    creators_fields = ['author', 'creator', 'maintainer', 'contributor']
    contributors_fields = ['editor', 'producer', 'publisher', 'provider', 'sponsor']

    # First create the full contact agenda by field
    if type(codemt_file[field]) is list:

        for person_property in codemt_file[field]:
            zenodo_person = parse_person_schema_property(person_property, field)
            # 'name' is the only key that MUST be contained in a person_property at least
            full_contacts[zenodo_person['name']] = zenodo_person

    else:
        zenodo_person = parse_person_schema_property(codemt_file[field], field)
        full_contacts[zenodo_person['name']] = zenodo_person

    # then save each person by field and avoid duplicates
    for i, person in enumerate(full_contacts):

        if field in creators_fields:

            # Contributors and maintainers in the same zenodo key
            if i == 0 and 'creators' not in zenodo_file:
                zenodo_file['creators'] = []
            elif person not in zenodo_file['creators']:
                zenodo_file['creators'].append(full_contacts[person])
            else:
                pass  # avoid duplicates

        elif field in contributors_fields:

            if i == 0 and 'contributors' not in zenodo_file:
                zenodo_file['contributors'] = []
            elif person not in zenodo_file['contributors']:
                zenodo_file['contributors'].append(full_contacts[person])
            else:
                pass  # avoid duplicates


def find_matching_metadata(codemeta_json):
    """
    Please note that the following fields are ASSUMED. If they are not correct, change them, or contact us otherwise.
        "access_right": "open"
        "language": "eng"

    param codemeta_json: dict
        already parsed dictionary containing the metadata of the codemeta.json file

    Returns:
    --------
    metadata_zenodo : dict
        dictionary cotaining the metadata information found at the codemeta.json file but written using the Zenodo
        syntax.
    """
    person_filed = ['author', 'creator', 'maintainer', 'contributor', 'editor', 'producer', 'publisher',
                    'provider', 'sponsor']

    metadata_zenodo = {'language': 'eng',
                       'access_right': 'open'}

    if codemeta_json["@type"] == "SoftwareSourceCode":
        metadata_zenodo['upload_type'] = 'software'
    else:
        metadata_zenodo['upload_type'] = ''
        print("\nCould not identify the type of schema in the `codemeta.json file`.\n"
              "Thus the 'upload_type' within the `.zenodo.json` file was left EMPTY.\n"
              "Please fill it up by yourself - otherwise zenodo will NOT be able to publish your entry.\n")

    if 'name' in codemeta_json:
        metadata_zenodo['title'] = codemeta_json['name']
    if 'description' in codemeta_json:
        metadata_zenodo['description'] = codemeta_json['description']

    if 'softwareVersion' in codemeta_json and 'version' not in codemeta_json:
        metadata_zenodo['version'] = codemeta_json['softwareVersion']
    elif 'version' in codemeta_json and 'softwareVersion' not in codemeta_json:
        metadata_zenodo['version'] = codemeta_json['version']
    else:
        metadata_zenodo['version'] = codemeta_json['version']

    if 'keywords' in codemeta_json:
        if type(codemeta_json['keywords']) == list:
            metadata_zenodo['keywords'] = codemeta_json['keywords']
        else:
            metadata_zenodo['keywords'] = [codemeta_json['keywords']]

    if 'license' in codemeta_json:
        metadata_zenodo['license'] = codemeta_json['license'].split('/')[-1]  # TODO to be improved
    if 'releaseNotes' in codemeta_json:
        metadata_zenodo['notes'] = "Release Notes: " + codemeta_json['releaseNotes']
    if 'citation' in codemeta_json:
        metadata_zenodo['references'] = codemeta_json['citation']
    if 'datePublished' in codemeta_json:
        metadata_zenodo['publication_date'] = codemeta_json['datePublished']

    for person in person_filed:
        if person in codemeta_json:
            add_author_metadata(metadata_zenodo, codemeta_json, field=person)

    # if 'author' in codemeta_json:
    #     add_author_metadata(metadata_zenodo, codemeta_json, field='author')
    # if 'creator' in codemeta_json:
    #     add_author_metadata(metadata_zenodo, codemeta_json, field='creator')
    # if 'maintainer' in codemeta_json:
    #     add_author_metadata(metadata_zenodo, codemeta_json, field='maintainer')
    # if 'contributor' in codemeta_json:
    #     add_author_metadata(metadata_zenodo, codemeta_json, field='contributor')
    # if '' in codemeta_json:
    #     metadata_zenodo[''] = codemeta_json['']

    return metadata_zenodo


def add_compulsory_escape_metadata(json_file):
    """
    Add compulsory information to the .zenodo.json file:
     * zenodo community : ESCAPE2020
     * ESCAPE grant ID (zenodo syntax)

    param json_file: dict
        dictionary containing the .zenodo.json metadata information
    """
    json_file["communities"] = [{"identifier": "escape2020"}]
    json_file["grants"] = [{"id": "10.13039/501100000780::824064"}]


def parse_codemeta_and_write_zenodo_metadata_file(codemeta_filename, zenodo_outname):
    """
    Reads the codemeta.json file and creates a new `.zenodo.json` file. This file will contain the SAME information
    that in the codemeta.json file but *** WITH THE ZENODO SYNTAX. ***

    codemeta_filename: str or Path
        path to the codemeta.json file
    zenodo_outname: str or Path
        path and name to the zenodo metada json file
        NOT TO BE CHANGED. The file must be named `.zenodo.json` and be stored in the root directory of the library.
    """
    with open(codemeta_filename) as infile:
        codemeta_json = json.load(infile)

    metadata_zenodo = find_matching_metadata(codemeta_json)
    add_compulsory_escape_metadata(metadata_zenodo)

    # Correct format for Zenodo
    data = {'metadata': metadata_zenodo}

    with open(zenodo_outname, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)


def query_yes_no(question, default="yes"):
    """
    Ask a yes/no question via raw_input() and return their answer.

    :param question: str
        question to the user
    :param default: str - "yes", "no" or None
        resumed answer if the user just hits <Enter>.
        "yes" or "no" will set a default answer for the user
        None will require a clear answer from the user

    :return: bool - True for "yes", False for "no"
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        else:
            try:
                return bool(strtobool(choice))
            except:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")


def query_continue(question, default="no"):
    """
    Ask a question and if the answer is no, exit the program.
    Calls `query_yes_no`.

    :param question: str
    :param default: str

    :return answer: bool - answer from query_yes_no
    """
    answer = query_yes_no(question, default=default)
    if not answer:
        sys.exit("Program stopped by user")
    else:
        return answer


def find_root_directory():
    """
     Find root directory of the project. This library MUST be added to the root directory of the same, i.e., MUST be
    a subdirectory of the root dir.

    :return root_directory: obj
        Path object with root directory
    """
    current_dir = os.path.abspath(os.path.dirname(__file__))
    current_dir_name = current_dir.split('/')[-1]
    root_directory = Path(str(current_dir.split(current_dir_name)[0]))

    return root_directory


if __name__ == "__main__":
    root_dir = find_root_directory()

    # Find all the .json files within the root directory of your library
    files_json = [file for file in os.listdir(root_dir) if file.endswith('.json')]

    # Filenames should no be changed
    zenodo_metadata_filename = root_dir / '.zenodo.json'
    codemeta_file = root_dir / 'codemeta.json'
    old_escape_metadata = root_dir / '.escape.yml'

    # check if it does exist the old `.escape.yml` metadata file
    if old_escape_metadata.exists():
        print(f"\n\tOld v0.1 ESCAPE metadata file found: '{old_escape_metadata.name}' -  PLEASE remove it ! \n")
        exit(-1)

    # Search for a codemeta.json file
    if codemeta_file.name not in files_json:
        print(f"\n\tNo {codemeta_file.name} found in the root directory of your project. Please add one.\n")
        exit(-1)

    # Check overwrite
    if zenodo_metadata_filename.name in files_json:
        query_continue(
            f"\nThe {zenodo_metadata_filename.name} file already exists."
            f"\nIf you continue you will overwrite the file with the metadata found in the {codemeta_file.name} file. "
            f"\n\nAre you sure ? ")

    # Parse the codemeta.json file and create the .zenodo.json file
    parse_codemeta_and_write_zenodo_metadata_file(codemeta_file, zenodo_metadata_filename)
    print("Done.")
