#!/bin/bash
mkdir -p datasets

dtool create he datasets
dtool add item datasets_dtoolcore_v2.4.0/he/data/he.txt datasets/he
dtool freeze datasets/he

dtool create she datasets
dtool add item datasets_dtoolcore_v2.4.0/she/data/file.txt datasets/she
dtool freeze datasets/she

dtool create cat datasets
dtool add item datasets_dtoolcore_v2.4.0/cat/data/file.txt datasets/cat
dtool freeze datasets/cat

dtool create lion datasets
dtool add item datasets_dtoolcore_v2.4.0/lion/data/file.txt datasets/lion
dtool freeze datasets/lion

dtool create people datasets
dtool add item datasets_dtoolcore_v2.4.0/people/data/anna.txt datasets/people
dtool add item datasets_dtoolcore_v2.4.0/people/data/patrick.txt datasets/people
dtool add item datasets_dtoolcore_v2.4.0/people/data/sarah.txt datasets/people
dtool freeze datasets/people

