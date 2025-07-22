#!/bin/bash

#SBATCH -N 1
#SBATCH -p gpu --gres=gpu:1
#SBATCH --mem 24G
#SBATCH -J Zebrafish_Analysis
#SBATCH -D /users/rrai8/zebrafish_analysis/Automated-Analysis-of-Zebrafish/examples
#SBATCH -o zebrafish-%j.out
#SBATCH -t 1:00:00
# SBATCH -e ../output/zebrafish-%j.err

function fix_names(){

	j=1
	DATA_DIR="/gpfs/data/rcretonp/experiment_data/${USER}/$3"
	for ((i = $1; i <= $2; i++)); do
  		old=$(printf "${DATA_DIR}/IMG_%04d.JPG" "$i") #04 pad to length of 4
  		new=$(printf "${DATA_DIR}/IMG_%04d.JPG" "$j")
		if [ -f $old ]; then mv -i -- "$old" "$new" ; fi
  		let j=j+1
	done

}

source /gpfs/runtime/opt/anaconda/2020.02/bin/activate

module load anaconda/2020.02
module unload anaconda/2020.02

RUN_EXE=$HOME/Automated-Analysis-of-Zebrafish/examples/inference_script.py



if [ "$#" -eq 5 ]; then
	fix_names $4 $5 $3
fi 

cd $WORK_DIR

conda activate /gpfs/data/rcretonp/venv/tfgpu-v2/


echo "Using Python: $(which python3)"
echo "Running script: ${RUN_EXE}"

# which python3

if [ "$#" -eq 5 ]; then
	python3 ${RUN_EXE} --rmin $1 --rmax $2 --experiment_dir $3 --model_name 96_well_plate-13-10-2021-Rohit.pb --starting_image $4
else
	python3 ${RUN_EXE} --rmin $1 --rmax $2 --experiment_dir $3 --model_name 96_well_plate-13-10-2021-Rohit.pb
fi
