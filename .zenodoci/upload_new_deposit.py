# -*- coding: utf-8 -*-
import os
import json
import argparse
from distutils.util import strtobool
from zenodoapi import ZenodoAPI
from utils_zenodoci import (parse_codemeta_and_write_zenodo_metadata_file,
                            find_root_directory
                            )


def create_zenodo_metadata(metadata_filename):
    """
    Checks for a zenodo metadata file, otherwise it looks for a codemeta.json file to create a the .zenodo.json file

    param metadata_filename: str
        path and name to the zenodo metada json file
        NOT TO BE CHANGED. The file must be named `.zenodo.json` and be stored in the root directory of the library.
    """
    root_dir = find_root_directory()

    files_json = [file for file in os.listdir(root_dir) if file.endswith('.json')]
    print(files_json)

    zenodo_metadata_filename = metadata_filename
    codemeta_file = 'codemeta.json'

    if codemeta_file in files_json and zenodo_metadata_filename not in files_json:
        parse_codemeta_and_write_zenodo_metadata_file(codemeta_file, zenodo_metadata_filename)
        print(f"\nCreating {zenodo_metadata_filename} automatically at the CI pipeline.\n")

    elif os.path.isfile(zenodo_metadata_filename):
        print(f"\n{zenodo_metadata_filename} metadata file found in the root directory of the library ! \n")
        pass

    else:
        print(f"\n{codemeta_file} not found, thus any zenodo_metadata file `{zenodo_metadata_filename}` was"
              f" created during the CI pipeline."
              f"Please provide one so that the CI can run correctly (examples in the 'codemeta_utils' directory)")
        exit(-1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Upload new deposit entry to Zenodo")

    # Required arguments
    parser.add_argument('--token', '-t', type=str,
                        dest='zenodo_token',
                        help='Personal access token to (sandbox)Zenodo')

    parser.add_argument('--sandbox_zenodo', '-s', action='store',
                        type=lambda x: bool(strtobool(x)),
                        dest='sandbox_flag',
                        help='Set the Zenodo environment.'
                             'If True connects with Zenodo. If False with Sanbox Zenodo',
                        default=False)

    parser.add_argument('--input-directory', '-i', type=str,
                        dest='input_directory',
                        help='Path to the directory containing the files to upload.'
                             'ALL files will be uploaded.',
                        required=True)

    args = parser.parse_args()

    z = ZenodoAPI(
        access_token=args.zenodo_token,
        sandbox=args.sandbox_flag  # True for sandbox.zenodo.org !! False for zenodo.org
    )

    # 1 - create empty deposit
    new_entry = z.create_new_entry()

    if new_entry.status_code < 399:
        deposition_id = new_entry.json()['id']
        doi = new_entry.json()['metadata']['prereserve_doi']['doi']
        print(f"Status {new_entry.status_code}. New entry to Zenodo created ! Deposition id {deposition_id}")
    else:
        print(new_entry.json())

    # 2 - upload files
    for file in os.listdir(args.input_directory):
        full_path_file = args.input_directory + '/' + file

        new_upload = z.upload_file_entry(
            deposition_id,
            name_file=file,
            path_file=full_path_file
        )

        print(f"File {file} correctly uploaded !\n", new_upload)

    # 3 - Create the zenodo metadata file from a codemeta.json file
    zenodo_metadata_filename = '.zenodo.json'
    create_zenodo_metadata(zenodo_metadata_filename)

    # And upload the repository metadata
    with open(zenodo_metadata_filename) as json_file:
        entry_metadata = json.load(json_file)

    # entry_info['metadata']['doi'] = doi  # In the new version of the API the doi is updated automatically.
    update_entry = z.update_info_entry(
        deposition_id,
        data=entry_metadata
    )

    if update_entry.status_code < 399:
        print(f"Status {update_entry.status_code}. Repository information correctly uploaded !")
    else:
        print(f"Repository information NOT correctly uploaded ! Status {update_entry.status_code}\n",
              update_entry.json())

    # 4 - publish entry - to publish the entry, uncomment the two lone below
    # publish = z.publish_entry(deposition_id)
    # print(publish.json())

    print("New deposit correctly published !")
    print(f"The new doi should look like 10.5281/{deposition_id}. However please")
    print(f" ** Check the upload at {z.zenodo_api_url[:-4]}/deposit/{deposition_id}  **")
