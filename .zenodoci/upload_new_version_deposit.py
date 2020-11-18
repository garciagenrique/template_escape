# -*- coding: utf-8 -*-
import os
import json
import argparse
from distutils.util import strtobool
from zenodoapi import ZenodoAPI

parser = argparse.ArgumentParser(description="Upload a new version of an existing deposit to Zenodo")

# Required arguments
parser.add_argument('--token', '-t', type=str,
                    dest='zenodo_token',
                    help='Personal access token to (sandbox)Zenodo',
                    required=True)

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

parser.add_argument('--deposit_id', '-id', type=str,
                    dest='deposit_id',
                    help='deposit_id of the deposit that is going to be updated by a new version',
                    required=True)

args = parser.parse_args()

if __name__ == '__main__':

    z = ZenodoAPI(access_token=args.zenodo_token,
                  sandbox=args.sandbox_flag  # True for sandbox.zenodo.org !! False for zenodo.org
                  )

    # 1 - request a new version of an existing deposit
    new_version = z.new_version_entry(args.deposit_id)

    if new_version.status_code < 399:
        print(f"Status {new_version.status_code}. New version of the {args.deposit_id} entry correctly created !")
    else:
        print(new_version.json())

    new_deposition_id = new_version.json()['links']['latest_draft'].rsplit('/')[-1]

    # PRE-2 - If you DO NOT want to erase the old files, comment the following lines
    old_files_ids = [file['id'] for file in new_version.json()['files']]
    for file_id in old_files_ids:
        z.erase_file_entry(new_deposition_id,
                           file_id)

    # 2 - Upload new version of file(s)
    for file in os.listdir(args.input_directory):
        full_path_file = args.input_directory + '/' + file

        new_upload = z.upload_file_entry(new_deposition_id,
                                         name_file=file,
                                         path_file=full_path_file)

        print(f"File {file} correctly uploaded !\n", new_upload)

    # 3 - Update metadata info
    with open('.zenodoci/repository_information.json') as json_file:
        update_entry_info = json.load(json_file)

    # update_entry_info['metadata']['doi'] = doi  # In the new version of the API the doi is updated automatically.

    update_entry = z.update_info_entry(new_deposition_id,
                                       data=update_entry_info)

    if update_entry.status_code < 399:
        print(f"Status {update_entry.status_code}. Repository information correctly uploaded !\n")
    else:
        print(f"Repository information NOT correctly uploaded ! Status {update_entry.status_code}\n",
              update_entry.json())

    # 4 - publish entry - to publish the entry, uncomment the two lone below
    # publish = z.publish_entry(new_deposition_id)
    # print(publish.json())

    print("New version of the old deposition correctly published !")
    print(f"Old deposition id {args.deposit_id}, new deposition id {new_deposition_id}")
    print(f"The new doi should look like 10.5281/{new_deposition_id}. However please")
    print(f" ** Check the upload at {z.zenodo_api_url[:-4]}/deposit/{new_deposition_id}  **")
