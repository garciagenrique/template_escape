FROM continuumio/miniconda3
ENV PATH=/opt/conda/bin/:${PATH}

# Ensure use of bash
SHELL [ "/bin/bash", "-c"]

RUN git clone https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape.git && \
    cd template_project_escape && \
    conda env create -f environment.yml && \
    source activate escape_template && \
    git fetch --tags && \
    tag=$(git describe --tags `git rev-list --tags --max-count=1`) && \
    if [ -z "$tag" ]; then git pull origin master; else git checkout $tag -b master_tag_$tag; fi && \
    python setup.py install && \
    cd .. && \
    rm -rf template_project_escape

RUN sed -i 's/base/escape_template/g' ~/.bashrc

RUN conda clean -a

CMD conda activate escape_template
