#!/bin/bash

# This source code is based on https://gitlab.com/singularityhub/gitlab-ci,
# with DOI: https://doi.org/10.5281/zenodo.3834833
# provided under the following license:

### BSD 3-Clause License
###
### Copyright (c) 2018, Vanessa Sochat
### All rights reserved.
###
### Redistribution and use in source and binary forms, with or without
### modification, are permitted provided that the following conditions are met:
###
### * Redistributions of source code must retain the above copyright notice, this
###   list of conditions and the following disclaimer.
###
### * Redistributions in binary form must reproduce the above copyright notice,
###   this list of conditions and the following disclaimer in the documentation
###   and/or other materials provided with the distribution.
###
### * Neither the name of the copyright holder nor the names of its
###   contributors may be used to endorse or promote products derived from
###   this software without specific prior written permission.
###
### THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
### AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
### IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
### DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
### FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
### DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
### SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
### CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
### OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
### OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###
#
# Installation Singularity and sregistry

apt-get update && apt-get install -y wget git \
                                          build-essential \
                                          squashfs-tools \
                                          libtool \
                                          autotools-dev \
                                          libarchive-dev \
                                          automake \
                                          autoconf \
                                          uuid-dev \
                                          libssl-dev


sed -i -e 's/^Defaults\tsecure_path.*$//' /etc/sudoers

# Check Python

echo "Python Version:"
python --version
pip install sregistry[all]
sregistry version

echo "sregistry Version:"

# Install Singularity

cd /tmp && \
    git clone -b vault/release-2.5 https://www.github.com/sylabs/singularity.git
    cd singularity && \
    ./autogen.sh && \
    ./configure --prefix=/usr/local && \
    make && make install
