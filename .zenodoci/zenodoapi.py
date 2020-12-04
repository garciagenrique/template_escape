#!/usr/bin/env python

# E. Garcia 2020
# email: garcia 'at' lapp.in2p3.fr

import json
import requests
from utils_zenodoci import (find_root_directory,
                            parse_codemeta_and_write_zenodo_metadata_file
                            )


class ZenodoAPI:
    def __init__(self, access_token, sandbox=True):
        """
        Manages the communication with the (sandbox.)zenodo REST API through the Python request library.
        This class is **EXCLUSIVELY** developed to be used within a CI/CD pipeline and to **EXCLUSIVELY PERFORM**
         the following tasks within the (sandbox.)zenodo api environment:

          - Fetches a user's published entries,
          - Creates a new deposit,
          - Creates a new version of an existing deposit,
          - Uploads files to a specific Zenodo entry,
          - Erases a non-published entry / new version draft,
          - Erases (old version) files from an entry (when creating a new_version entry and uploading
            new_version files),
          - Uploads information to the entry (Zenodo compulsory deposit information),
          - Publishes an entry


        :param access_token: str
            Personal access token to (sandbox.)zenodo.org/api
        :param sandbox: bool
            Communicates with either zenodo or sandbox.zenodo api
        """

        if sandbox:
            zenodo_api_url = "https://sandbox.zenodo.org/api"
        else:
            zenodo_api_url = "https://zenodo.org/api"

        self.zenodo_api_url = zenodo_api_url
        self.access_token = access_token
        self.exist_codemeta_file = False
        self.path_codemeta_file = ''
        self.exist_zenodo_metadata_file = False
        self.path_zenodo_metadata_file = ''

    def fetch_user_entries(self):
        """
        Fetch the published entries of an user. Works to tests connection to Zenodo too.

        GET method to {zenodo_api_url}/deposit/depositions

        :return: obj
            request.get answer
        """
        url = f"{self.zenodo_api_url}/deposit/depositions"
        parameters = {'access_token': self.access_token}

        return requests.get(url, params=parameters)

    def create_new_entry(self):
        """
        Create a new entry / deposition in (sandbox.)zenodo

        POST method to {zenodo_api_url}/deposit/depositions

        :return: obj
            requests.put answer
        """
        url = f"{self.zenodo_api_url}/deposit/depositions"
        headers = {"Content-Type": "application/json"}
        parameters = {'access_token': self.access_token}

        return requests.post(url, json={}, headers=headers, params=parameters)

    def upload_file_entry(self, entry_id, name_file, path_file):
        """
        Upload a file to a Zenodo entry. If first retrieve the entry by a GET method to the
            {zenodo_api_url}/deposit/depositions/{entry_id}.

        PUT method to {bucket_url}/{filename}. The full api url is recovered when the entry is firstly retrieved.

        :param entry_id: str
            deposition_id of the Zenodo entry
        :param name_file: str
            File name of the file when uploaded
        :param path_file: str
            Path to the file to be uploaded

        :return: obj
            json requests.put object
        """
        # 1 - Retrieve and recover information of an existing deposit
        parameters = {'access_token': self.access_token}
        fetch = requests.get(f"{self.zenodo_api_url}/deposit/depositions/{entry_id}",
                             params=parameters)

        # 2 - Upload the files
        bucket_url = fetch.json()['links']['bucket']  # full url is recovered from fetch (GET) method
        url = f"{bucket_url}/{name_file}"

        with open(path_file, 'rb') as upload_file:
            upload = requests.put(url, data=upload_file, params=parameters)

        return upload.json()

    def update_metadata_entry(self, entry_id, data):
        """
        Update an entry resource. Data should be the entry information that will be shown when a deposition is visited
        at the Zenodo site.

        PUT method to {zenodo_api_url}/deposit/depositions/{entry_id}. `data` MUST be included as json.dump(data)

        :param entry_id: str
            deposition_id of the Zenodo entry
        :param data: object
            json object containing the metadata (compulsory fields) that are enclosed when a new entry is created.

        :return: obj
            requests.put answer
        """
        url = f"{self.zenodo_api_url}/deposit/depositions/{entry_id}"
        headers = {"Content-Type": "application/json"}
        parameters = {'access_token': self.access_token}

        return requests.put(url, data=json.dumps(data),
                            headers=headers, params=parameters)

    def erase_entry(self, entry_id):
        """
        Erase an entry/new version of an entry that HAS NOT BEEN published yet.
        Any new upload/version will be first saved as 'draft' and not published until confirmation (i.e, requests.post)

        DELETE method to {zenodo_api_url}/deposit/depositions/{entry_id}.

        :param entry_id: str
            deposition_id of the Zenodo entry to be erased

        :return: obj
            requests.delete json answer
        """
        url = f"{self.zenodo_api_url}/deposit/depositions/{entry_id}"
        parameters = {'access_token': self.access_token}

        return requests.delete(url, params=parameters)

    def erase_file_entry(self, entry_id, file_id):
        """
        Erase a file from an entry resource.
        This method is intended to be used for substitution of files (deletion) within an entry by their correspondent
         new versions.
        DELETE method to {zenodo_api_url}/deposit/depositions/{entry_id}/files/{file_id}

        :param entry_id: str
            deposition_id of the Zenodo entry
        :param file_id: str
            Id of the files stored in Zenodo

        :return: obj
            requests.delete answer
        """
        url = f"{self.zenodo_api_url}/deposit/depositions/{entry_id}/files/{file_id}"
        parameters = {'access_token': self.access_token}

        return requests.delete(url, params=parameters)

    def publish_entry(self, entry_id):
        """
        Publishes an entry in (sandbox.)zenodo
        POST method to {zenodo_api_url}/deposit/depositions/{entry_id}/actions/publish

        :param entry_id: str
            deposition_id of the Zenodo entry

        :return: obj
            requests.put answer
        """
        url = f"{self.zenodo_api_url}/deposit/depositions/{entry_id}/actions/publish"
        parameters = {'access_token': self.access_token}

        return requests.post(url, params=parameters)

    def new_version_entry(self, entry_id):
        """
        Creates a new version of AN EXISTING entry resource.
        POST method to {zenodo_api_url}/deposit/depositions/{entry_id}/actions/newversion

        :param entry_id: str
            deposition_id of the Zenodo entry

        :return: obj
            requests.post answer
        """
        url = f"{self.zenodo_api_url}/deposit/depositions/{entry_id}/actions/newversion"
        parameters = {'access_token': self.access_token}

        return requests.post(url, params=parameters)

    def search_codemeta_file(self):
        """Check if a `codemeta.json` files exists in the ROOT directory of the project"""

        root_dir = find_root_directory()
        codemeta_file = root_dir / 'codemeta.json'

        if codemeta_file.exists():
            print("\n * Found codemeta.json file within the project !")
            self.exist_codemeta_file = True
            self.path_codemeta_file = codemeta_file
        else:
            print("\n ! codemeta.json file NOT found in the root directory of the  project !")

    def search_zenodo_json_file(self):
        """Check if a `.zenodo.json` files exists in the ROOT directory of the project"""

        root_dir = find_root_directory()
        zenodo_metadata_file = root_dir / '.zenodo.json'

        if zenodo_metadata_file.exists():
            print("\n * Found .zenodo.json file within the project !")
            self.exist_zenodo_metadata_file = True
            self.path_zenodo_metadata_file = zenodo_metadata_file
        else:
            print("\n ! .zenodo.json file NOT found in the root directory of the  project !")

    def test_upload_to_zenodo(self):
        """
        `Tests` the different stages of the GitLab-Zenodo connection and that the status_code returned by every
        stage is the correct one.

        Tests:
         - If it exists a `codemeta.json` file
            - If it exists a `.zenodo.json` file
               - If not, it creates one, based on the `codemeta.json` file
         - The communication with Zenodo through its API to verify that:
            - You can fetch an user entries
            - You can create a new entry
            - The provided zenodo metadata can be digested, and not errors appear
            - Finally erases the test entry - because IT HAS NOT BEEN PUBLISHED !
        """
        # Search for codemeta.json file within the project
        self.search_codemeta_file()

        if self.exist_codemeta_file:

            # Search for zenodo.json metadata file within the project
            self.search_zenodo_json_file()
            if self.exist_zenodo_metadata_file:
                print("\n * Using the .zenodo.json file to simulate a new upload to Zenodo... \n")
            else:
                print("\n ! Creating a .zenodo.json file from your codemeta.json file...\n"
                      "     Please add, commit and push this file to your project repository.")
                self.path_zenodo_metadata_file = self.path_codemeta_file.parent / '.zenodo.json'

                parse_codemeta_and_write_zenodo_metadata_file(self.path_codemeta_file,
                                                              self.path_zenodo_metadata_file)

            # 1 - Test connection
            print("Testing communication with Zenodo...")
            test_connection = self.fetch_user_entries()
            if test_connection.status_code == 200:
                print("OK !")
            else:
                print(test_connection.json())

            # 2 - Test new entry
            print("Testing the creation of a dummy entry to (sandbox)Zenodo...")
            new_entry = self.create_new_entry()
            if new_entry.status_code == 201:
                print("OK !")
            else:
                print(new_entry.json())

            # 3 - Test upload metadata
            print("Testing the ingestion of the Zenodo metadata...")
            test_entry_id = new_entry.json()['id']

            with open(self.path_zenodo_metadata_file) as file:
                metadata_entry = json.load(file)

            update_metadata = self.update_metadata_entry(test_entry_id,
                                                         data=metadata_entry
                                                         )
            if update_metadata.status_code == 200:
                print("OK !")
            else:
                print(update_metadata.json())

            # 4 - Test delete entry
            print("Testing the deletion of the dummy entry...")
            delete_test_entry = self.erase_entry(test_entry_id)
            if delete_test_entry.status_code == 204:
                print("OK !")
            else:
                print(delete_test_entry.json())

            print("\n\tYAY ! Successful testing of the connection to Zenodo ! \n\n"
                  "You should not face any trouble when uploading a project to Zenodo through the "
                  "ESCAPE-GitLabCI pipeline.\n"
                  "In case you do, please contact us !\n")

        else:

            print("\n ! Please add a codemeta.json file to the ROOT directory of your project.\n")