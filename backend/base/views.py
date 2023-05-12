# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from .products import products
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from django.shortcuts import render

from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20180509 import TextScanRequest
import json
import uuid
import datetime
import openai
import re
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
alicloud_id_key= os.getenv('ALICLOUD_ACCESS_ID')
alicloud_secret_key=os.getenv('ALICLOUD_ACCESS_SECRET')

# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/alicloud/',
        '/api/betterchinese/',
        '/api/transenglish/'
    ]
    return Response(routes)

@api_view(['POST'])
def getProducts(request):
    print("request555" ,request.data['test'])
    return  Response()

@api_view(['POST'])
def getAlicloud(request):
    content = request.data['content']
    clt = client.AcsClient(alicloud_id_key, alicloud_secret_key,'cn-shanghai')
    region_provider.modify_point('Green', 'cn-shanghai', 'green.cn-shanghai.aliyuncs.com')
    # 每次请求时需要新建request，请勿复用request对象。
    request = TextScanRequest.TextScanRequest()
    request.set_accept_format('JSON')
    task1 = {"dataId": str(uuid.uuid1()),
            "content":content,
            "time":datetime.datetime.now().microsecond
            }
    # 文本反垃圾检测场景的场景参数是antispam。
    request.set_content(bytearray(json.dumps({"tasks": [task1], "scenes": ["antispam"]}), "utf-8"))
    response = clt.do_action_with_exception(request)
    print(response)
    result = json.loads(response)
    if 200 == result["code"]:
        taskResults = result["data"]
        for taskResult in taskResults:
            if (200 == taskResult["code"]):
                sceneResults = taskResult["results"]
                for sceneResult in sceneResults:
                    scene = sceneResult["scene"]
                    print(scene)
                    suggestion = sceneResult["suggestion"]
                    print(suggestion)
                    # 根据scene和suggestion设置后续操作。
    return  Response(result)

@api_view(['POST'])
def getBetterChinese(request):
    content = request.data['content']
    # openai.api_key = openai_api_key
    # response = openai.Completion.create(
    #   model = "davinci",
    #   prompt="把这个改写成好的中文:"+content, 
    #   temperature=0.7, # 设置生成文本的创造性程度
    #   max_tokens=100, # 限制生成文本的最大长度
    #   top_p=1, # 返回生成文本的数量
    #   stop=None # 可以用来停止生成文本的字符串
    # )

    # story = response.choices[0].text
    # story = re.sub('[^0-9a-zA-Z\u4e00-\u9fa5，。？！]', '', story) # 只保留中文字符、标点符号和空格
    # print(story)
    openai.api_key = openai_api_key
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0301",
    messages=[
        {"role": "user", "content": "把这些文字变成优美的中文:"+content}
    ],
     max_tokens=100
    )

    print(completion.choices[0].message.content)
    return  Response(completion.choices[0].message.content)

@api_view(['POST'])
def getTranslation(request):
    content = request.data['content']
    # openai.api_key = openai_api_key
    # response = openai.Completion.create(
    #   model = "davinci",
    #   prompt="把这个改写成好的中文:"+content, 
    #   temperature=0.7, # 设置生成文本的创造性程度
    #   max_tokens=100, # 限制生成文本的最大长度
    #   top_p=1, # 返回生成文本的数量
    #   stop=None # 可以用来停止生成文本的字符串
    # )

    # story = response.choices[0].text
    # story = re.sub('[^0-9a-zA-Z\u4e00-\u9fa5，。？！]', '', story) # 只保留中文字符、标点符号和空格
    # print(story)
    openai.api_key = openai_api_key
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "please tanslate it to good English:"+content}
    ],
     max_tokens=100
    )

    print(completion.choices[0].message.content)
    return  Response(completion.choices[0].message.content)