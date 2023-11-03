# Continuously check every 5 minutes that a RELION job has finished successfully by looking in $JOB_DIRECTORY and checking for the presence of a file called "run_it025_optimiser.star". If this file is present, then the job has finished successfully and the script send an email to the specified email address. If the file is not present, then the script will sleep for 5 minutes and then check again. If the job has not finished after 24 hours, then the script will exit with an error.

# Usage: check_relion_job.sh <JOB_DIRECTORY> <EMAIL_ADDRESS>

# Arguments:
# <JOB_DIRECTORY> Absolute path to the RELION job directory.
# <EMAIL_ADDRESS> Email address to send notification to when the job has finished.

# Output: None


# Check the number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: check_relion_job.sh <JOB_DIRECTORY> <EMAIL_ADDRESS>"
    exit 1
fi

# Check that the job directory exists
if [ ! -d "$1" ]; then
    echo "Error: Job directory $1 does not exist."
    exit 1
fi

# Check that the email address is valid
if ! [[ "$2" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    echo "Error: Email address $2 is not valid."
    exit 1
fi
################
### FAILSAFE ###
################
# Check if any file has not been created or modified in $1 in the last 30 minutes
################
### FAILSAFE ###
################


# Check if the job has finished for 48 hours
for i in {1..576}; do
    # Check if the job has finished 
    if ls $1/RELION_JOB* 1> /dev/null 2>&1; then
        # Send an email to the specified email address
        echo "" > ~/email.txt
        echo "RELION job $1 has finished." >> ~/email.txt
        ssmtp $2 < ~/email.txt
        exit 0
    fi

    # Check if run.err has been updated since the start of the job
    if [ -f "$1/run.err" ]; then
        if [ $(stat -c %Y "$1/run.err") -gt $(stat -c %Y "$1/run.out") ]; then
            # Check if run.err has new text containing the string "You ran out of memory on the GPU(s)." 
            if grep -q "You ran out of memory on the GPU(s)." "$1/run.err"; then
                # Send an email to the specified email address
                echo "" > ~/email.txt
                echo "RELION job $1 has failed due to running out of memory on the GPU(s)." >> ~/email.txt
                ssmtp $2 < ~/email.txt
                exit 1
            fi
            # Send an email to the specified email address
            echo "" > ~/email.txt
            echo "RELION job $1 has failed." >> ~/email.txt
            ssmtp $2 < ~/email.txt
            exit 1
        fi
    fi

    # Check if run.out has been updated since the start of the job and it has been 60 minutes since this script was started 
    if [ $(find $1 -mmin -60 | read) ] && [ $($i -gt 12) ]; then
        # Send an email to the specified email address
        echo "" > ~/email.txt
        echo "RELION job $1 has not been updated in the last 60 minutes." >> ~/email.txt
        ssmtp $2 < ~/email.txt
    fi

    # Sleep for 5 minutes
    sleep 5m
done