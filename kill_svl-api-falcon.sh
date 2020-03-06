#!/bin/bash
ps aux|grep svl-api-falcon |awk '{print $2}' | xargs kill
ps aux|grep svl-api-falcon

