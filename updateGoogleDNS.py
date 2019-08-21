#! /usr/bin/python3
'''
   Copyright [2019] [Raúl Eduardo González Argote]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
Created on Aug 19, 2019

@author: rafex

'''
import time
import os
import logging
import requests

from google.oauth2 import service_account
from google.cloud import dns
from bs4 import BeautifulSoup
from sys import exit

try:
    PATH_LOGS=os.environ["UPDATE_GOOGLE_DNS_LOGS"]
except KeyError:
    print('log path not found creating in default folder')
    
try:
    logging.basicConfig(
        filename=PATH_LOGS+'/updateGoogleDNS.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p')
except:
    logging.basicConfig(
        filename='/tmp/updateGoogleDNS.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p')
        
logging.info('Started')

try:
    PROJECT_ID=os.environ["UPDATE_GOOGLE_DNS_PROJECT_ID"]
    PATH_OAUTH2_JSON=os.environ["UPDATE_GOOGLE_DNS_JSON"]
    ZONE_NAME=os.environ["UPDATE_GOOGLE_DNS_ZONE_NAME"]
except KeyError:
    logging.info('there are no environment variables')
    exit()
    


page_link ='https://www.cual-es-mi-ip.net/'
page_response = requests.get(page_link, timeout=5)
page = requests.get("https://www.cual-es-mi-ip.net/").text
page_content = BeautifulSoup(page_response.content, "html.parser")
tag = page_content.find_all('span', attrs={'class':'big-text font-arial'})
my_ip = tag[0].get_text()

logging.info("My IP: " + my_ip)

credentials = service_account.Credentials.from_service_account_file(
    PATH_OAUTH2_JSON)

scoped_credentials = credentials.with_scopes(
    ['https://www.googleapis.com/auth/ndev.clouddns.readwrite'])

client_dns = dns.Client(
    project=PROJECT_ID,
    credentials=scoped_credentials)

zones = client_dns.list_zones()

for zone in zones:
    if ZONE_NAME == zone.name:
        records = zone.list_resource_record_sets()
        for record in records:
            if 'A' == record.record_type:
                logging.info('name: ' + record.name)
                logging.info('type: ' + record.record_type)
                logging.info('ttl: ' + str(record.ttl))
                logging.info('data: ' + str(record.rrdatas))
                if record.rrdatas[0] == my_ip:
                    logging.info('same ip')
                else:
                    logging.info('different ip')
                    changes = zone.changes()
                    changes.delete_record_set(record)
                    changes.create()
                    while changes.status != 'done':
                        logging.info('Waiting for changes to complete')
                        time.sleep(30)
                        changes.reload()
                    record_set = zone.resource_record_set('rafex.dev.', 'A', 300, [my_ip,])
                    changes = zone.changes()
                    changes.add_record_set(record_set)
                    changes.create()  # API request
                    while changes.status != 'done':
                        logging.info('Waiting for changes to complete')
                        time.sleep(30)
                        changes.reload()

            break
    break

logging.info('Finished')
