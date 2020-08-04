# -*- coding: utf-8 -*-
import os
import json
import argparse
from distutils.util import strtobool
from zenodoapi import ZenodoAPI


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

if __name__ == '__main__':

    z = ZenodoAPI(access_token=args.zenodo_token,
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

        new_upload = z.upload_file_entry(deposition_id,
                                         name_file=file,
                                         path_file=full_path_file)

        print(f"File {file} correctly uploaded !\n", new_upload)

    # 3 - Upload repository information - that you must have filled before the json file !
    with open('.zenodoci/repository_information.json') as json_file:
        entry_info = json.load(json_file)

    # entry_info['metadata']['doi'] = doi  # In the new version of the API the doi is updated automatically.
    update_entry = z.update_info_entry(deposition_id,
                                       data=entry_info)

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
    print(f" ** Check the upload at {z.zenodo_api_url[:-4]}deposit/{deposition_id}  **")
