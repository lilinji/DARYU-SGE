#!/usr/bin/env bash
# Copyright 2015, Rackspace US, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Note:
# This file is maintained in the hpc-sdk repository.
# https://github.com/lilinji/hpc-sdk.git
# If you need to modify this file, update the one in the hpc-sdk
# repository and then update this file as well. The purpose of this file is to
# prepare the host and then execute all the tox tests.
#

#######01  Creat conf json
/usr/bin/python modfiy_conf_json.py -c compute -f gridengine -k 1 -m master -p Novo2017 
sleep 10
echo "install  HPC-CLUSTER.........."

/usr/bin/python digger.py -c hpc-sge.json

sleep 30
####clear transh
cd ../../

rm -rf hpc-sdk
