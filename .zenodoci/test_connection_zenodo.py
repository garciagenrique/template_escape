#!/usr/bin/env python

# E. Garcia Nov 2020
# Module to test the connection and the upload of new entries/version to Zenodo.

import argparse
from distutils.util import strtobool
from zenodoapi import ZenodoAPI

if __name__ == '__main__':

    # Required arguments
    parser = argparse.ArgumentParser(description="Upload new deposit entry to Zenodo")

    parser.add_argument('--token', '-t', type=str,
                        dest='zenodo_token',
                        help='Personal access token to (sandbox)Zenodo',
                        required=True)

    parser.add_argument('--sandbox', '-s', action='store',
                        type=lambda x: bool(strtobool(x)),
                        dest='sandbox_flag',
                        help='Set the Zenodo environment.'
                             'If True connects with Zenodo. If False with Sandbox Zenodo',
                        default=False)

    args = parser.parse_args()

    zenodo = ZenodoAPI(access_token=args.zenodo_token,
                       sandbox=args.sandbox_flag
                       )

    zenodo.test_upload_to_zenodo()
