#!/usr/bin/env bash
set -e

if [ "$DEBUG" = true ] ; then
    echo 'Debugging - ON'
    nodemon --exec streamlit run main.py
else
    echo 'Debugging - OFF'
    streamlit run main.py
fi