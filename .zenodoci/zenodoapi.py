# -*- coding: utf-8 -*-

import json
import requests


class ZenodoAPI:
    def __init__(self, access_token, sandbox=True):
        """
        Manages the communication with the (sandbox.)zenodo REST API.
        This class is **EXCLUSIVELY** developed to be used within a CI/CD pipeline and to **EXCLUSIVELY PERFORM**
         five tasks within the (sandbox.)zenodo api environment:

          - Create a new deposit,
          - Create a new version of an existing deposit,
          - Upload files to a specific Zenodo entry,
          - Upload information to the entry (Zenodo compulsory deposit information)
          - Publish an entry


        :param access_token: str
            Personal access token to (sandbox.)zenodo.org/api
        :param sandbox: bool
            Communicates with either zenodo or sandbox.zenodo api
        """

        if sandbox:
            zenodo_api_url = "https://sandbox.zenodo.org/api/"
        else:
            zenodo_api_url = "https://zenodo.org/api/"

        self.zenodo_api_url = zenodo_api_url
        self.access_token = access_token

    def create_new_upload(self):
        """
        Create a new entry / deposition in (sandbox.)zenodo
        POST method to {zenodo_api_url}/deposit/depositions

        :return: request.put answer
        """
        url = f"{self.zenodo_api_url}/deposit/depositions"
        headers = {"Content-Type": "application/json"}
        parameters = {'access_token': self.access_token}

        return requests.post(url, headers=headers, params=parameters)

    def upload_files_entry(self, entry_id, name_file, path_file):
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

        :return: json request.put object
        """
        # 1 - Retrieve and recover information of an existing deposit
        parameters = {'access_token': self.access_token}
        fetch = requests.get(f"{self.zenodo_api_url}/deposit/depositions/{entry_id}",
                             params=parameters)

        # 2 - Upload the files
        bucket_url = fetch.json()['links']['bucket']  # full url is recovered from fetch (GET) method
        url = f"{bucket_url}/{name_file}"

        with open(path_file, 'rb') as upload_file:
            upload = requests.put(url, data=upload_file)

        return upload.json()

    def update_info_entry(self, entry_id, data):
        """
        Update an entry resource. Data should be the entry information that will be shown when a deposition is visited
        at the Zenodo site.
        PUT method to {zenodo_api_url}/deposit/depositions/{entry_id}. `data` MUST be included as json.dump(data)

        :param entry_id: str
            deposition_id of the Zenodo entry
        :param data: object
            json object containing the metadata (compulsory fields) that are enclosed when a new entry is created.

        :return: request.put answer
        """
        url = f"{self.zenodo_api_url}/deposit/depositions/{entry_id}"
        headers = {"Content-Type": "application/json"}
        parameters = {'access_token': self.access_token}

        return requests.put(url, data=json.dump(data), headers=headers, params=parameters)

    def publish_entry(self, entry_id):
        """
        Publishes an entry in (sandbox.)zenodo
        POST method to {zenodo_api_url}/deposit/depositions/{entry_id}/actions/publish

        :param entry_id: str
            deposition_id of the Zenodo entry

        :return: request.put answer
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

        :return: request.post answer
        """
        url = f"{self.zenodo_api_url}deposit/depositions/{entry_id}/actions/newversion"
        parameters = {'access_token': self.access_token}

        return requests.post(url, params=parameters)
