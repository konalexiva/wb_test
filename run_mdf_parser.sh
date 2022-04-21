#!/bin/bash

mv /code/parsed_data/data.json /code/parsed_data/"$(date)"_data.json
cd /code/mdf_parser && scrapy runspider mdf_parser/spiders/main_parser.py -o $PARSED_DATA_PATH

