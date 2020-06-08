# -*- coding: utf-8 -*-
import os
import json
import argparse
from distutils.util import strtobool
from zenodolib import ZenodoHandler

parser = argparse.ArgumentParser(description="Upload a new version of an existing deposit to Zenodo")

# Required arguments
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

parser.add_argument('--token', '-t', type=str,
                    dest='zenodo_token',
                    help='Personal access token to (sandbox)Zenodo',
                    required=True)

parser.add_argument('--deposit_id', '-id', type=str,
                    dest='deposit_id',
                    help='deposit_id of the deposit that is going to be updated by a new version',
                    required=True)

parser.add_argument('--new_deposit_version', '-nV', type=str,
                    dest='new_deposit_version',
                    help='Numerical version of the new version deposit.')

args = parser.parse_args()

if __name__ == '__main__':

    z = ZenodoHandler(access_token=args.zenodo_token,
                      test=args.sandbox_flag  # True for sandbox.zenodo.org !! False for zenodo.org
                      )

    new_version = z.deposition_actions_newversion(args.deposit_id)
    if new_version.status_code < 399:
        print("Status {}. New version of the {} entry correctly created !".format(new_version.status_code,
                                                                                  args.deposit_id)
              )
    else:
        print(new_version.json())

    new_deposition_id = new_version.json()['links']['latest_draft'].rsplit('/')[-1]

    # # If you DO NOT want to erase the old files, comment the following lines
    old_files_ids = [file['id'] for file in new_version.json()['files']]
    for file_id in old_files_ids:
        z.deposition_files_delete(new_deposition_id,
                                  file_id)

    # Upload new version of file(s)
    for file in os.listdir(args.input_directory):
        full_path_file = args.input_directory + '/' + file

        # # For standard files
        # new_upload = z.deposition_files_create(deposition_id,
        #                                        target_name=file,
        #                                        file_path=full_path_file)
        # print(new_upload.json())

        # # For large files
        new_upload = z.deposition_file_upload_large_file(new_deposition_id,
                                                         target_name=file,
                                                         file_path=full_path_file)
        print("File {} correctly uploaded !\n".format(file), new_upload)

    # Update metadata info
    with open('.zenodoci/repository_information.json') as json_file:
        update_entry_info = json.load(json_file)

    # update_entry_info['metadata']['doi'] = doi
    # In the new version of the API the doi is updated automatically. The new doi must look something
    # like 10.5281/{new_deposition_id}

    update_entry = z.deposition_update(new_deposition_id,
                                       data=update_entry_info)
    if update_entry.status_code < 399:
        print("Status {}. Repository information correctly uploaded !\n".format(update_entry.status_code))
    else:
        print("Repository information NOT correctly uploaded !\n", update_entry.json())

    # publish entry - to publish the entry, uncomment the two lone below
    # publish = z.deposition_actions_publish(new_deposition_id)
    # print(publish.json())

    print("New version of the old deposition correctly published !")
    print("Old deposition id {}, new deposition id {}".format(args.deposit_id, new_deposition_id))
    print("The new doi should look like 10.5281/{}. However please".format(new_deposition_id))
    print(" ** Check the upload at {}deposit/{}  **".format(z.base_url[:-4], new_deposition_id))
