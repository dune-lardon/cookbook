#!/bin/bash
. /your/miniconda/path/etc/profile.d/conda.sh
conda activate lardenv
elec=$1
run=$2
sub=$3
python /path/to/lardon.py -elec $elec -run $run -sub $sub -out test
