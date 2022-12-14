# Copyright 2019-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import boto3
import logging
import traceback
import sys
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def handler(event, context):
    """
    Lambda handler function to be triggered by findProduct API.
    """
    try:
        productId = event['pathParameters']['id']

        logger.debug("Product Id: %s", productId)

        logger.info("Finding product...")
        client = boto3.client('dynamodb')
        response = client.get_item(
                            TableName=os.environ['DYNAMODB_TABLE'],
                            Key={
                                    'id': {
                                        'S': productId
                                    }
                                })
        logger.info("Success: %s", response)
        returnResp = {
            "isBase64Encoded": True,
            "statusCode": 200,
            "body": json.dumps(response)
        }
        return returnResp
    except Exception as e:
        logger.error("Unknow exception occured when finding product. %s", e)
        traceback.print_exc()
        sys.exit()
        returnResp = {
            "isBase64Encoded": True,
            "statusCode": 500,
            "body": "Error occured when finding product"
        }
        return returnResp