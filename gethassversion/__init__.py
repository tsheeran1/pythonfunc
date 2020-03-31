#! /usr/bin/env python3

import logging
import azure.functions as func

import re
import requests
import json


def getImageTags(repoName: str, pgNum: int):

    rTagInfo = {}
    tagUrl=f'https://registry.hub.docker.com/v2/repositories/{repoName}/tags/?page={pgNum}'
    response = requests.get(tagUrl).json()
    for result in response['results']:
        currentTag = result['name']
        currentDigest = result['images'][0]['digest']
#        currentTuple = (currentTag, currentDigest)
        rTagInfo.update({currentTag: currentDigest})

    return rTagInfo

def getStableVersion(repoName: str):

    pg = 0
    stableFound = False
    while not stableFound:
        pg = pg+1
        tagList = getImageTags(repoName, pg)
#        print(f'got Page number {pg}')
        
        for tagKey in tagList:
#            print(f'Tag = {tagKey} %t Digest = {tagList[tagKey]}')
            if tagKey =='stable':
                stableDigest = tagList[tagKey]
            if  not (re.search(r"[^0-9.]", tagKey)) and (tagList[tagKey] == stableDigest):
                stableVersion = tagKey
                stableFound = True
                return stableVersion


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return func.HttpResponse(f'{getStableVersion("homeassistant/raspberrypi3-homeassistant")}')

