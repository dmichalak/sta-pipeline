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

# Check if the job has finished for 48 hours
for i in {1..576}; do
    # Check if the job has finished
    if [ -f "$1/run_it025_optimiser.star" ]; then
        # Send an email to the specified email address
        echo "RELION job $1 has finished successfully." | mail -s "RELION job finished" "$2"
        exit 0
    fi

    # Sleep for 5 minutes
    sleep 5m
done