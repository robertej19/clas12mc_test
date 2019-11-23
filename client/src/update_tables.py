#!/usr/bin/env python
#****************************************************************
"""
# Info
"""
#****************************************************************

from __future__ import print_function
import argparse, os, sqlite3, subprocess, sys, time
import numpy as np
from subprocess import PIPE, Popen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../')
#Could also do the following, but then python has to search the
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import fs, gcard_helper, get_args, scard_helper, user_validation, utils

def update_tables(args,UserSubmissionID,username,timestamp,scard_fields):
    #Grab username and gcard information that just got entered into DB
    strn = "SELECT UserID FROM Users WHERE User = '{0}';".format(username)
    userid = utils.db_grab(strn)[0][0]
    strn = "SELECT GcardID, gcard_text FROM Gcards WHERE UserSubmissionID = {0};".format(UserSubmissionID)
    gcards = utils.db_grab(strn)

    #Update tables
    strn = "UPDATE UserSubmissions SET {0} = '{1}' WHERE UserSubmissionID = {2};".format('UserID',userid,UserSubmissionID)
    utils.db_write(strn)
    strn = "UPDATE UserSubmissions SET {0} = '{1}' WHERE UserSubmissionID = {2};".format('User',username,UserSubmissionID)
    utils.db_write(strn)
    for gcard in gcards:
      GcardID = gcard[0]
      strn = "INSERT INTO FarmSubmissions(UserSubmissionID,GcardID) VALUES ({0},{1});".format(UserSubmissionID,GcardID)
      utils.db_write(strn)
      strn = "UPDATE FarmSubmissions SET submission_pool = '{0}' WHERE GcardID = '{1}';".format(scard_fields.data['farm_name'],GcardID)
      utils.db_write(strn)
      strn = "UPDATE FarmSubmissions SET run_status = 'Not Submitted' WHERE GcardID = '{0}';".format(GcardID)
      utils.db_write(strn)

if __name__ == "__main__":
  args = get_args.get_args_client()
  update_tables(args,UserSubmissionID,username,scard)
