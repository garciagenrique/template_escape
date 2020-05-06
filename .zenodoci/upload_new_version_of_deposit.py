# -*- coding: utf-8 -*-
import os
import argparse
from zenodolib import ZenodoHandler

parser = argparse.ArgumentParser(description="Upload a new version of an existing deposit to zenodo")

# Required arguments
parser.add_argument('--input-file', '-i', type=str,
                    dest='input_file',
                    help='Full path to the file to upload')

parser.add_argument('--token', '-t', type=str,
                    dest='zenodo_token',
                    help='Personal access token to Sandbox/zenodo')

parser.add_argument('--deposit_id', '-id', type=str,
                    dest='deposit_id',
                    help='deposit of the existing deposit '
                    )

args = parser.parse_args()

if __name__ == '__main__':
    if not args.input_file:
        print("No file declared ! Exiting. ")
        exit(1)
    if not args.deposit_id:
        print("No zenodo deposition id declared ! Exiting. ")
        exit(1)

    z = ZenodoHandler(access_token=args.zenodo_token,
                      test=True  # True for sandbox.zenodo.org !! False for zenodo.org
                      )

    new_version = z.deposition_actions_newversion(args.deposit_id)
    if new_version.status_code < 399:
        print("Status {}".format(new_version.status_code),
              new_version.json())

    new_deposition_id = new_version.json()['links']['latest_draft'].rsplit('/')[-1]

    # # If you DO NOT want to erase the old files, comment the following lines
    old_files_ids = [file['id'] for file in new_version.json()['files']]
    for file_id in old_files_ids:
        z.deposition_files_delete(new_deposition_id,
                                  file_id)

    # Upload new version of file(s)
    # To upload various files create a loop like : for file in os.listdir(directory):
    full_path_file = os.path.abspath(args.input_file)
    name = os.path.basename(args.input_file)
    new_upload = z.deposition_files_create(new_deposition_id,
                                           target_name=name,
                                           file_path=full_path_file)

    if new_upload.status_code < 399:
        print("Status {}. \nFile(s) correctly uploaded:\n".format(new_upload.status_code),
              z.deposition_files_list(new_version).json())

    # publish entry - to publish the entry, uncomment the two lone below
    # publish = z.deposition_actions_publish(new_deposition_id)
    # print(publish.json())
    print("New version of the old deposition correctly published !")
    print("Old deposition id {}, new deposition id {}".format(args.deposit_id, new_deposition_id))
    print("Check the upload at {}deposit/{}".format(z.base_url[:-4], new_deposition_id))
