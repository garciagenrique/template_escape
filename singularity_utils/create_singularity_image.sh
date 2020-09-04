#!/bin/bash

cp ../environment.yml environment.yml
cp ../Singularity Singularity

sudo singularity build escape_template.simg Singularity

rm environment.yml
rm Singularity

echo -e "\n\tContainer created ! To run it : >> singularity run escape_template.simg #NUMBER# "
echo -e "\tTo get help run : >> singularity run-help escape_template.simg\n"
