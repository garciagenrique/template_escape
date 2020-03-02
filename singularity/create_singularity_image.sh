#!/bin/bash

cp ../env_template_escape.yml env_template_escape.yml

sudo singularity build escape_template.simg singularity_template_escape.recipe

rm env_template_escape.yml

echo "Container created ! To run it : >> singularity run escape_template.simg #NUMBER# "
echo "To get help run : >> singularity run-help escape_template.simg"