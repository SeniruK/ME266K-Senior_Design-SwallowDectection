#!/bin/env bash

# configuration paths

PT_INDEX=$(( LAUNCHER_JID ))
if [ -z "$LAUNCHER_JID" ]
then
    echo "LAUNCHER_JID is not defined, was this job called from Launcher?"
    exit 1
else
    echo "Executing job #: ${LAUNCHER_JID} on dataset ${PT_INDEX}"
fi

module load python3

python3 load.py --videoNum=$PT_INDEX