# consul-scripts
A collection of scripts for importing, exporting, and utilising Consul KV data

These were used to very quickly spin up a demo of Consul's capabilities

##### import_yaml_to_consul.py
Takes a collection of simple YAML data sets and loads them into the Consul KV store

##### ohai_consul.rb
An ohai plugin for chef that reads a data set from the Consul API into the chef node attributes. It also outputs the data into a local temporary file.
