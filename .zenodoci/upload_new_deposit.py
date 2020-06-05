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

    # create empty deposit
    r = z.deposition_create()
    if r.status_code < 399:
        deposition_id = r.json()['id']
        doi = r.json()['metadata']['prereserve_doi']['doi']
        print("Status {}. New entry to Zenodo created ! Deposition id {}".format(r.status_code,
                                                                                 deposition_id))
    else:
        print(r.json())

    # upload files
    for file in os.listdir(args.input_directory):
        full_path_file = args.input_directory + '/' + file

        # # For standard files
        # new_upload = z.deposition_files_create(deposition_id,
        #                                        target_name=file,
        #                                        file_path=full_path_file)
        # print(new_upload.json())

        # # For large files
        new_upload = z.deposition_file_upload_large_file(deposition_id,
                                                         target_name=file,
                                                         file_path=full_path_file)
        print("File {} correctly uploaded !\n".format(file), new_upload)

    # Upload repository information - that you must have filled before ! - and add the doi
    with open('.zenodoci/repository_information.json') as json_file:
        entry_info = json.load(json_file)
    #entry_info['metadata']['doi'] = doi

    update_entry = z.deposition_update(deposition_id,
                                       data=entry_info)
    if update_entry.status_code < 399:
        print("Status {}. Repository information correctly uploaded !".format(update_entry.status_code))
    else:
        print("Repository information NOT correctly uploaded !", update_entry.json())

    # publish entry - to publish the entry, uncomment the two lone below
    # publish = z.deposition_actions_publish(deposition_id)
    # print(publish.json())
    print("New deposit correctly published !")
    print("Check the upload at {}deposit/{}".format(z.base_url[:-4], deposition_id))
