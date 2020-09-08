# -*- coding: utf-8 -*-
import sys
import yaml
import os.path
from distutils.util import strtobool


class FillCiScript:
    """ template_project_escape .gitlab-ci.yml file generator.

        If you are going to modify this script, please note that YAML does NOT allow TABS !
    """
    def __init__(self, config_dict):
        self.stages = config_dict['stages']
        self.repository_info = config_dict['repository_information']
        self.zenodoci_info = config_dict['zenodoci_information']

        # Format dict['repository_information']['base_url']
        if self.repository_info['base_url'][-1] is not '/':
            self.repository_info['base_url'] = self.repository_info['base_url'] + '/'

        self.str_stages = ["stages:\n"]
        self.str_test = []
        self.str_build = []
        self.str_deploy = [
            "deploy_zenodo:\n",
            "  stage: deploy\n",
            "  image: python:3.6.11-buster\n"
        ]

    def format_str_stages(self):
        """ Format the string containing the `stages` stage"""
        for stage in self.stages:
            self.str_stages.append(f" - {stage}\n")
        self.str_stages.extend(["\n"])

    def format_str_test(self):
        """ Format the string containing the `test` stage"""
        self.str_test = [
            "build_and_test_project:\n",
            "  stage: test\n",
            "  image: continuumio/miniconda3:latest\n",
            "  script:\n",
            "    - . /opt/conda/etc/profile.d/conda.sh\n",
            "    - conda env create -f environment.yml\n",
            f"    - conda activate {self.repository_info['name']}\n",
            "    - python setup.py install\n",
            "    - pytest .\n",
            "\n"
        ]

    def format_str_build(self):
        """ Format the string containing the `build` stage"""
        self.str_build = [
            "build_image:\n",
            "  stage: build\n",
            "  image: singularityware/singularity:gitlab-2.6\n",
            "  script:\n",
            "    - /bin/bash .gitlabci/build.sh Singularity\n",
            "    - mkdir -p build && cp *.simg build\n",
            "    - mkdir -p build && cp Singularity* build\n",
            "\n",
            "  artifacts:\n",
            "    paths:\n",
            "      - build/Singularity.simg\n",
            "      - build/Singularity\n",
            "\n",
            "  only:\n",
            "    - tags\n",
            "\n"
        ]

    def format_str_deploy(self):
        """ Format the string containing the `deploy` stage"""
        if "build" in self.str_stages and "deploy" in self.str_stages:
            str_dependencies = [
                "  dependencies:\n",
                "    - build_image\n"
            ]
            self.str_deploy.extend(str_dependencies)

        body_deploy = [
            "  script:\n",
            "    - apt-get -y update\n",
            "    - pip3 install requests\n",
            "\n",
            f"    - export REPOSITORY_NAME={self.repository_info['name']}\n",
            f"    - export REPOSITORY_BASE_URL={self.repository_info['base_url']}$REPOSITORY_NAME\n",
            """    - export LAST_RELEASE=`git ls-remote --tags --refs --sort="v:refname" $REPOSITORY_URL.git | tail -n1 | sed 's/.*\///'`\n""",
            "\n",
            "    - mkdir -p build\n",
            "    - >\n",
            '      if [ -z "$LAST_RELEASE" ]; then\n',
            '        echo "No tag / new release found ! - Or error when parsing. Downloading last commit to the repository (master branch) ;"; \ \n',
            '        wget -O $REPOSITORY_NAME-master.zip "REPOSITORY_BASE_URL"/-/archive/master/"$REPOSITORY_NAME"-master.zip; \ \n',
            '        mv $REPOSITORY_NAME-master.zip ./build\n',
            "      else\n",
            '        echo "$LAST_RELEASE tag / release found !"; \ \n',
            '        wget -O $REPOSITORY_NAME-$LAST_RELEASE.zip "REPOSITORY_BASE_URL"/-/archive/"$LAST_RELEASE"/"$REPOSITORY_NAME"-"$LAST_RELEASE".zip; \ \n',
            '        mv $REPOSITORY_NAME-$LAST_RELEASE.zip ./build\n',
            "      fi\n",
            "\n",
            "    - ls ./build\n",
            "\n"
        ]

        end_deploy = [
            "  only:\n",
            "    - tags"
        ]

        if self.zenodoci_info['new_entry'] and self.zenodoci_info['new_version'] or not self.zenodoci_info['new_entry'] and not self.zenodoci_info['new_version']:
            exit("READ the instructions in the ci-config.yml file. Please.")
        # new entry to Zenodo
        elif self.zenodoci_info['new_entry'] and not self.zenodoci_info['sandbox']:
            option_deploy = [
                "    - >\n",
                "      python3 .zenodoci/upload_new_deposit.py\n",
                "      --token $ZENODO_TOKEN\n",
                "      --sandbox_zenodo False\n",
                "      --input-directory ./build\n",
                "\n"
            ]
        # new version to Zenodo
        elif self.zenodoci_info['new_version'] and not self.zenodoci_info['sandbox']:
            option_deploy = [
                "    - >\n",
                "      python3 .zenodoci/upload_new_version_deposit.py\n",
                "      --token $ZENODO_TOKEN\n",
                "      --sandbox_zenodo False\n",
                "      --input-directory ./build\n",
                "      --deposit_id $DEPOSIT_ID_ESCAPE_TEMPLATE\n",
                "\n"
            ]
        # new entry to SANDBOX Zenodo
        elif self.zenodoci_info['new_entry'] and self.zenodoci_info['sandbox']:
            option_deploy = [
                "    - >\n",
                "      python3 .zenodoci/upload_new_deposit.py\n",
                "      --token $SANDBOX_ZENODO_TOKEN\n",
                "      --sandbox_zenodo True\n",
                "      --input-directory ./build\n",
                "\n"
            ]
        # new version to SANDBOX Zenodo
        elif self.zenodoci_info['new_version'] and self.zenodoci_info['sandbox']:
            option_deploy = [
                "    - >\n",
                "      python3 .zenodoci/upload_new_version_deposit.py\n",
                "      --token $SANDBOX_ZENODO_TOKEN\n",
                "      --sandbox_zenodo True\n",
                "      --input-directory ./build\n",
                "      --deposit_id $ZENODO_DEPOSIT_ID\n",
                "\n"
            ]

        self.str_deploy.extend(body_deploy)
        self.str_deploy.extend(option_deploy)
        self.str_deploy.extend(end_deploy)


def query_yes_no(question, default="yes"):
    """
    Ask a yes/no question via raw_input() and return their answer.

    :param question: str
        question to the user
    :param default: str - "yes", "no" or None
        resumed answer if the user just hits <Enter>.
        "yes" or "no" will set a default answer for the user
        None will require a clear answer from the user

    :return: bool - True for "yes", False for "no"
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        else:
            try:
                return bool(strtobool(choice))
            except:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")


def query_continue(question, default="no"):
    """
    Ask a question and if the answer is no, exit the program.
    Calls `query_yes_no`.

    :param question: str
    :param default: str

    :return answer: bool - answer from query_yes_no
    """
    answer = query_yes_no(question, default=default)
    if not answer:
        sys.exit("Program stopped by user")
    else:
        return answer


def read_ci_config_file(yaml_ci_config_file="./ci-config.yml"):
    """
    Paese the `ci-config.yml` yaml file into a dictionary

    :param yaml_ci_config_file: str
        yaml input file

    :return config: dict
    """
    with open(yaml_ci_config_file) as p:
        config = yaml.safe_load(p)
    return config


if __name__ == '__main__':
    if os.path.isfile("../.gitlab-ci.yml"):
        query_continue("\nThe `.gitlab.yml` file already exists. "
                       "If you continue you will overwrite the file.\nAre you sure ?")

    # Load config
    ci_config_dict = read_ci_config_file()

    # Open output file & initialize class
    out_file = open("../.gitlab-ci.yml", "w")
    ci_template = FillCiScript(ci_config_dict)

    # Format and dump stages
    ci_template.format_str_stages()
    out_file.writelines(ci_template.str_stages)

    if "test" in ci_template.stages:
        ci_template.format_str_test()
        out_file.writelines(ci_template.str_test)

    if "build" in ci_template.stages:
        ci_template.format_str_build()
        out_file.writelines(ci_template.str_build)

    if "deploy" in ci_template.stages:
        ci_template.format_str_deploy()
        out_file.writelines(ci_template.str_deploy)

    # Close output file
    out_file.close()
