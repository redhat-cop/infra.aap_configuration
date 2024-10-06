#!/bin/bash

# Ensure git-filter-repo is installed
if ! command -v git-filter-repo &> /dev/null
then
    echo "git-filter-repo could not be found, please install it first."
    exit
fi

# Get a list of all files that were deleted at some point in history
deleted_files=$(git log --diff-filter=D --summary | grep delete | awk '{print $NF}')

# Loop through each deleted file
for file in $deleted_files; do
    # Check if the file still exists in the current working directory
    if [ ! -f "$file" ]; then
        echo "Removing history of $file as it no longer exists..."
        # Remove history of the file using git filter-repo
        git filter-repo --path "$file" --invert-paths --force
    else
        echo "$file still exists, skipping history removal."
    fi
done

# Prompt the user to force-push the changes
echo "History rewrite is complete."
echo "To update the remote repository, run the following commands:"
echo "git push origin --force --all"
echo "git push origin --force --tags"