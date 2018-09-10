#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
reload(sys)

import detect_unnormal_files 
import check_sha256
import change_attribute
import get_sha256_list 

detect_unnormal_files.main()
check_sha256.main()
change_attribute.main()
get_sha256_list.main() 
