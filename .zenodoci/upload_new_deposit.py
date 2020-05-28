# -*- coding: utf-8 -*-
import os
import json
import argparse
from zenodolib import ZenodoHandler


parser = argparse.ArgumentParser(description="Upload new deposit entry to Zenodo")

# Required arguments
parser.add_argument('--input-file', '-i', type=str,
                    dest='input_file',
                    help='Full path to the file to upload',
                    required=True)

parser.add_argument('--token', '-t', type=str,
                    dest='zenodo_token',
                    action='store_true',
                    help='Personal access token to (sandbox)Zenodo',
                    required=True)

args = parser.parse_args()

if __name__ == '__main__':

    z = ZenodoHandler(access_token=args.zenodo_token,
                      test=True  # True for sandbox.zenodo.org !! False for zenodo.org
                      )

    # create empty deposit
    r = z.deposition_create()
    if r.status_code < 399:
        deposition_id = r.json()['id']
        doi = r.json()['metadata']['prereserve_doi']['doi']
        print("Status {}. New entry to zenodo created ! Deposition id {}".format(r.status_code,
                                                                                 deposition_id))
    else:
        print(r.json())

    # upload files
    # To upload various files create a loop like : for file in os.listdir(directory):
    full_path_file = os.path.abspath(args.input_file)
    name = os.path.basename(args.input_file)
    new_upload = z.deposition_files_create(deposition_id,
                                           target_name=name,
                                           file_path=full_path_file)

    if new_upload.status_code < 399:
        print("Status {}. \nFile(s) correctly uploaded:\n".format(new_upload.status_code),
              z.deposition_files_list(deposition_id).json())
    else:
        print(new_upload.json())

    # Upload repository information - that you must have filled before ! - and add the doi
    with open('.zenodoci/repository_information.json') as json_file:
        entry_info = json.load(json_file)
    entry_info['metadata']['doi'] = doi

    update_entry = z.deposition_update(deposition_id,
                                       data=entry_info)
    if update_entry.status_code < 399:
        print("Status {}. Repository information correctly uploaded !".format(update_entry.status_code))
    else:
        print(update_entry.json())

    # publish entry - to publish the entry, uncomment the two lone below
    # publish = z.deposition_actions_publish(deposition_id)
    # print(publish.json())
    print("New deposit correctly published !")
    print("Check the upload at {}deposit/{}".format(z.base_url[:-4], deposition_id))
