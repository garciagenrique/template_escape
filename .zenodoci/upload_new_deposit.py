# -*- coding: utf-8 -*-
import os
import json
import argparse
from distutils.util import strtobool
from zenodolib import ZenodoHandler


parser = argparse.ArgumentParser(description="Upload new deposit entry to Zenodo")

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
                    help='Personal access token to (sandbox)Zenodo')

args = parser.parse_args()

if __name__ == '__main__':

    z = ZenodoHandler(access_token=args.zenodo_token,
                      test=args.sandbox_flag  # True for sandbox.zenodo.org !! False for zenodo.org
                      )

    # 1 - create empty deposit
    r = z.deposition_create()

    if r.status_code < 399:
        deposition_id = r.json()['id']
        doi = r.json()['metadata']['prereserve_doi']['doi']
        print("Status {}. New entry to Zenodo created ! Deposition id {}".format(r.status_code,
                                                                                 deposition_id))
    else:
        print(r.json())

    # 2 - upload files
    for file in os.listdir(args.input_directory):
        full_path_file = args.input_directory + '/' + file

        new_upload = z.deposition_file_upload_large_file(deposition_id,
                                                         target_name=file,
                                                         file_path=full_path_file)

        print("File {} correctly uploaded !\n".format(file), new_upload)

    # 3 - Upload repository information - that you must have filled before the json file !
    with open('.zenodoci/repository_information.json') as json_file:
        entry_info = json.load(json_file)

    # entry_info['metadata']['doi'] = doi  # In the new version of the API the doi is updated automatically.
    update_entry = z.deposition_update(deposition_id,
                                       data=entry_info)

    if update_entry.status_code < 399:
        print("Status {}. Repository information correctly uploaded !".format(update_entry.status_code))
    else:
        print("Repository information NOT correctly uploaded ! Status {}\n".format(update_entry.status_code),
              update_entry.json())

    # 4 - publish entry - to publish the entry, uncomment the two lone below
    # publish = z.deposition_actions_publish(deposition_id)
    # print(publish.json())

    print("New deposit correctly published !")
    print("The new doi should look like 10.5281/{}. However please".format(deposition_id))
    print(" ** Check the upload at {}deposit/{}  **".format(z.base_url[:-4], deposition_id))
