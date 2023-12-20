# -*- coding: utf-8 -*-
from sampleserver import app
from flask_restful import reqparse, Resource, Api
import platform
from flask import Flask, request
from flask import Response
import hashlib
import base64
import json
import os
import logging
from logging import handlers
from datetime import datetime, timedelta
import traceback
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
from sqlalchemy import ext
from sqlalchemy import text
from flask_cors import CORS
import math
import glob
import csv
import ast
import re
import codecs
import requests
#
import subprocess
import random
from configparser import ConfigParser
PRINT_LOG = True
import time

var_cros_v1 = {'Content-Type', 'token', 'If-Modified-Since', 'Cache-Control', 'Pragma'}
# var_cros_v2 = {'Content-Type', 'token'}
CORS(app, resources=r'/api/*', headers=var_cros_v1)

# Multilanguages
import sys
from importlib import reload
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

# --------------------------------------------------------------------------------------------------------------------
#                                            Static Area
# --------------------------------------------------------------------------------------------------------------------
DAEMON_HEADERS = {'Content-type': 'application/json'}

g_platform = platform.system()

if g_platform == "Linux":
    LOG_DEFAULT_DIR = './log'
elif g_platform == "Windows":
    LOG_DEFAULT_DIR = '.'
elif g_platform == "Darwin":
    LOG_DEFAULT_DIR = '.'



# --------------------------------------------------------------------------------------------------------------------
#                                            Function Area
# --------------------------------------------------------------------------------------------------------------------

def result(code, notice, objects, meta, author):
    """
    html status code def
    [ 200 ] - OK
    [ 400 ] - Bad Request
    [ 401 ] - Unauthorized
    [ 404 ] - Not Found
    [ 500 ] - Internal Server Error
    [ 503 ] - Service Unavailable
    - by thingscare
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    if author is None:
        author = "by sisung"

    result = {
        "status": code,
        "notice": notice,
        "author": author
    }

    log_bySisung = ''

    # [ Check ] Objects
    if objects is not None:
        result["objects"] = objects

    # [ Check ] Meta
    if meta is not None:
        result["meta"] = meta

    if code == 200:
        result["message"] = "OK"
        log_bySisung = OKBLUE
    elif code == 400:
        result["message"] = "Bad Request"
        log_bySisung = FAIL
    elif code == 401:
        result["message"] = "Unauthorized"
        log_bySisung = WARNING
    elif code == 404:
        result["message"] = "Not Found"
        log_bySisung = FAIL
    elif code == 500:
        result["message"] = "Internal Server Error"
        log_bySisung = FAIL
    elif code == 503:
        result["message"] = "Service Unavailable"
        log_bySisung = WARNING

    log_bySisung = log_bySisung + 'RES : [' + str(code) + '] ' + str(notice) + ENDC
    return result

def json_encoder(thing):
    list_date = str(thing).split(":")

    if hasattr(thing, 'isoformat'):
        if len(list_date[0]) == 1:
            return "0" + thing.isoformat()
        return thing.isoformat()
    else:
        if len(list_date[0]) == 1:
            return "0" + str(thing)
        return str(thing)

# --------------------------------------------------------------------------------------------------------------------
#                                            Class Area
# --------------------------------------------------------------------------------------------------------------------
class Helper(object):
    @staticmethod
    def get_file_logger(app_name, filename):
        log_dir_path = LOG_DEFAULT_DIR
        try:
            if not os.path.exists(log_dir_path):
                os.mkdir(log_dir_path)

            full_path = '%s/%s' % (log_dir_path, filename)
            file_logger = logging.getLogger(app_name)
            file_logger.setLevel(logging.INFO)

            file_handler = handlers.RotatingFileHandler(
                full_path,
                maxBytes=(1024 * 1024 * 10),
                backupCount=5
            )
            formatter = logging.Formatter('%(asctime)s %(message)s')

            file_handler.setFormatter(formatter)
            file_logger.addHandler(file_handler)

            return file_logger

        except :
            return logging.getLogger(app_name)


exception_logger = Helper.get_file_logger("exception", "exception.log")
service_logger = Helper.get_file_logger("service", "service.log")


def Log(msg) :
    try :
        if PRINT_LOG == True :
            print(msg)
        service_logger.info(msg)
    except :
        print("log exception!!")

@app.errorhandler(500)
def internal_error(exception):
    exception_logger.info(traceback.format_exc())
    return 500


@app.errorhandler(404)
def internal_error(exception):
    exception_logger.info(traceback.format_exc())
    return 404


@app.route('/', methods=['GET'])
class GptRequest(Resource):
    """
    [ GptRequest ]
    For GptRequest
    @ GET : Returns Result
    by sisung
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.api_headers = {'Content-type': 'application/json'}
        self.parser.add_argument("querystring", type=str, location="json")
        self.querystring = self.parser.parse_args()["querystring"]
        super(GptRequest, self).__init__()

    def get(self):
        Log("[GptRequest START...]")
        
        sObjcts = []
        meta = {
            "gpt_response": "",
        }

        return result(200, "GptRequest successful.", sObjcts, meta, "by sisung ")
    

    
api = Api(app)

# Basic URI
# 로그인
api.add_resource(GptRequest, '/api/GptRequest')
# api.add_resource(MakeJsonDataset, '/api/MakeJsonDataset')
# api.add_resource(MakeJsonFile, '/api/MakeJsonFile')