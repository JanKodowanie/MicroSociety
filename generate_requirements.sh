#!/bin/bash

pip freeze > AccountService/requirements.txt
pip freeze > BlogWriteService/requirements.txt
pip freeze > BlogReadService/requirements.txt
pip freeze > EmailService/requirements.txt