#!/usr/local/bin/python

import os, sys
import yaml
import json
import base64
from glob import glob
from subprocess import Popen, PIPE

consul_staging_file = "./_consul.json_"
data_sets = glob("test_data_sets/*.yml")
consul_hash = []

def import_to_consul(json_file):
    command = ["consul", "kv", "import", "@" + json_file]
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    process.wait()

def parse_data(key, value):
    if type(value) == dict:
        for k,v in value.items():
            consul_key = "%s/%s" % (key, k)
            parse_data(consul_key, v)
    else:
        new_item = {
            "key": key,
            "flags": 0,
            "value": base64.encodestring(value).rstrip()
        }
        consul_hash.append(new_item)

for data_set in data_sets:
    with open(data_set, 'r') as f:
        kv_items = yaml.load(f)
    for k,v in kv_items.items():
        parse_data(k,v)

consul_json = json.dumps(consul_hash)

with open(consul_staging_file, 'w') as f:
    f.write(consul_json)

import_to_consul(consul_staging_file)
os.remove(consul_staging_file)

sys.exit(0)
