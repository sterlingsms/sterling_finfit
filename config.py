import os

# Enable Development Env

DEBUG = True

# Application Directory

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads. Common assumption is
# to use 2 threads per available core.
# Handles incoming requests using one and 
# performs background operations on other.

THREADS_PER_PAGE = 2

# CSRF

CSRF_ENABLED = True
CSRF_SESSION_KEY = ''

# Key for cookies

SECRET_KEY = 'Same as Session Key'

# define your API key and the other ID
AIRTABLE_API_KEY='pat9BjQk76tXmReDr.e75399d5bb7483e7460c042b2f59778137f0506585af37ef25ae9cfb2b9d4107'

APP_FINFIT='appAr6enCWvYHvXIA'
TABLE_AGENTS='tblIKZZ8gfOptULJo'
