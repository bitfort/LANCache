#! /bin/sh
python server.py -a &
cd data
python -m SimpleHTTPServer 9980 &
