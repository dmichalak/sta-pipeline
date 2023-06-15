#!/usr/bin/env python

import click
# # # # # # # # # # # # # # # # # # # # # # # #
# Usage:
# $ bash isonet.sh <task-number>
# 	<task-number> = 1 for preparing the STAR file
# 			2 for CTF deconvolution
# 			3 for generating masks
# 			4 for extracting subtomograms
# 			5 for refining the model
# 			6 for prediction
#
# ***Note: Make sure to manually enter the zero-tilt defocus values for each tomogram after preparing the STAR file
# # # # # # # # # # # # # # # # # # # # # # # #

@click.group()
@click.argument('task_name')
def cli(task):
    click.echo(f"Running a \"{task_name}\" task.")
    return None

@click



#####
##### Options for preparing the STAR file
#####

TOMO_DIR="./tomograms" # authors recommend 1 to 5 tomograms
JOB_NAME="wws_20230403"
PIXEL_SIZE="10.0" # A/px
NUM_SUBTOMOS="60" # per tomogram


#####
##### Options for CTF deconvolution
#####

STAR_FILE="${JOB_NAME}.star"
VOLTAGE="300.0" # keV
SPHERICAL_ABERRATION="2.7" # mm
SNR_FALLOFF="0.50" # high values mean losing more high frequency data (default = 1.0)
DECONV_STRENGTH="1.0" # (default = 1.0)
HIGHPASS_NYQUIST="0.02" # authors recommend keeping this at its default value (0.02)
NCPU="12" # (default = 4)
DECONV_DIR="${JOB_NAME}_deconv_snrfalloff${SNR_FALLOFF}"
#TOMO_IDX= # only process tomograms listed, e.g., 1,2,4 or 5-10,15,16


#####
##### Options for generating masks
#####
MASK_DIR="${JOB_NAME}_mask"
DENSITY_PERCENTAGE="50" # (default = 50)
STD_PERCENTAGE="50" # (default = 50)
Z_CROP="0.2" # mask out the top and bottom $Z_CROP*100 percent of the tomogram (z-axis)


#####
##### Options for extracting subtomograms
#####

SUBTOMO_DIR="${JOB_NAME}_subtomo"
SUBTOMO_STAR="${JOB_NAME}_subtomo.star"
CUBE_SIZE_SUBTOMO="64" # size of cubes for training (default = 64)
CROP_SIZE_SUBTOMO="80" # size of subtomogram volumes (default = 16+CUBE_SIZE}


#####
##### Options for refining the model
#####

#CONTINUE_FROM=".json"
GPUID="0,2"
DATA_DIR="$SCRATCH"
#PRETRAINED_MODEL
RESULT_DIR="${JOB_NAME}_results"
PREPROCESSING_CPUS="1"

NOISE_LEVEL="0.05,0.1,0.15,0.2" # level of noise STD(added noise)/STD(data) after the defined iterations
NOISE_START_ITER="11,16,21,26"
#NOISE_DIR="${JOB_NAME}_noise"

ITERATIONS="30" # (default = 30)
EPOCHS="10" # (default = 10)
#BATCH_SIZE=
#STEPS_PER_EPOCH=

# generally, keep these as their default values
LEARNING_RATE="0.0004"
DROP_OUT="0.3"
CONVS_PER_DEPTH=3
KERNEL="(3,3,3)"
UNET_DEPTH="3"


#####
##### Options for prediction
#####

TRAINED_MODEL=" .h5"
OUTPUT_DIR="${JOB_NAME}_corrected_tomos"
CUBE_SIZE_PREDICT="64"
CROP_SIZE_PREDICT="96"

################ Ready to go! #################


if [ $1 = '1' ]; then
	isonet.py prepare_star $TOMO_DIR --output_star $STAR_FILE --pixel_size $PIXEL_SIZE --number_subtomos $NUM_SUBTOMOS
elif [ $1 = '2' ]; then
	isonet.py deconv $STAR_FILE --deconv_folder "${JOB_NAME}_deconv" --voltage $VOLTAGE --cs $SPHERICAL_ABERRATION \
		--snrfalloff $SNR_FALLOFF --deconvstrength $DECONV_STRENGTH --highpassnyquist $HIGHPASS_NYQUIST \
		--ncpu $NCPU #--tomo_idx $TOMO_IDX
elif [ $1 = '3' ]; then
	isonet.py make_mask $STAR_FILE --mask_folder $MASK_DIR --density_percentage $DENSITY_PERCENTAGE \
		--std_percentage $STD_PERCENTAGE --z_crop $Z_CROP #--tomo_idx $TOMO_IDX
elif [ $1 = '4' ]; then
	echo "Running isonet.py extract $STAR_FILE --subtomo_folder $SUBTOMO_DIR --subtomo_star $SUBTOMO_STAR --cube_size $CUBE_SIZE_SUBTOMO --crop_size $CROP_SIZE_SUBTOMO #--tomo_idx $TOMO_IDX"
	isonet.py extract $STAR_FILE --subtomo_folder $SUBTOMO_DIR --subtomo_star $SUBTOMO_STAR \
		--cube_size $CUBE_SIZE_SUBTOMO --crop_size $CROP_SIZE_SUBTOMO #--tomo_idx $TOMO_IDX
elif [ $1 = '5' ]; then
	isonet.py refine $SUBTOMO_STAR --gpuID $GPUID --iterations $ITERATIONS --data_dir $DATA_DIR \
		--result_dir $RESULT_DIR --preprocessing_ncpus $PREPROCESSING_CPUS --epochs $EPOCHS \
		--noise_level $NOISE_LEVEL --noise_start_iter $NOISE_START_ITER --learning_rate $LEARNING_RATE \
		--drop_out $DROP_OUT --kernel $KERNEL --unet_depth $UNET_DEPTH
elif [ $1 = '6' ]; then
	isonet.py predict $STAR_FILE $TRAINED_MODEL --output_dir $OUTPUT_DIR --gpuID $GPUID --cube_size $CUBE_SIZE_PREDICT \
		--crop_size $CROP_SIZE_PREDICT 
fi
