#! /bin/sh
python server.py &
cd data
python -m SimpleHTTPServer 9980 &
