#!/bin/bash
export LD_LIBRARY_PATH=/usr/lib/oracle/11.2/client64/lib/${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export ORACLE_HOME=/usr/lib/oracle/11.2/client64
export NLS_DATE_FORMAT="dd/mm/yyyy hh24:mi:ss"
export NLS_LANG="THAI_THAILAND.TH8TISASCII"
cd /home/python3/svl-api-falcon
. venv/bin/activate
gunicorn -c config.py  main:app --reload
