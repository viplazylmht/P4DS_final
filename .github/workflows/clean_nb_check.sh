#!/bin/sh

# Get all notebooks currently staged for commit
notebooks=`git ls-tree --full-tree -r --name-only HEAD | grep .ipynb`

# Checks if $notebooks is non-empty
if [ ! -z "$notebooks" ]
then
    # Run the script to test the clean of notebooks
    python .github/workflows/check_clean_notebooks.py $notebooks
    
fi