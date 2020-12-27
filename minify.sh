#!/bin/bash
pyminify tinyweb/server.py --remove-literal-statements > tinyweb/server_min.py
echo -e "# https://github.com/metachris/tinyweb\n$(cat tinyweb/server_min.py)" > tinyweb/server_min.py
echo "Minified server.py into tinyweb/server_min.py"
