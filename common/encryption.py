# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: encryption.py
@IDE: PyCharm
@time: 2023-06-09 16:08
@description: 加密
"""
import base64, logging, hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def encryption(message):
    """
    RSA加密
    :param message: 需要加密的字符串
    :return:
    """
    # 公钥
    public_key = """-----BEGIN PUBLIC KEY-----
   MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCx/TwSbu0zigoG3b7/2+QL/xwu6cAizkv+82XBHV/pXvrbTHAqvzrxqijg5+ojFqfh00vtSdio0ubN3MnG/5PTS1NwNUvPHNnzGmq+qmRWbcB7e20eiNQ60HhGlrFOmOb68yBKq9YRf8/1R0Lcl8V1nd25pAuHCjbSz+4Q73xFwQIDAQAB
    -----END PUBLIC KEY-----"""

    #读取公钥
    publickey = RSA.import_key(public_key)
    #加密
    pk = PKCS1_v1_5.new(publickey)
    encrypt_test = pk.encrypt(message.encode("utf-8"))
    #base64编码
    result = base64.b64encode(encrypt_test)
    enc_message = result.decode()

    return enc_message

def enc_base64(message):
    """
    base64加密
    :param message: 需要加密的字符串
    :return:
    """
    result = base64.b64encode(message.encode("utf-8")).decode()
    return result


def enc_sha1(message):
    """
    sha1加密
    :param message: 需要加密的字符串
    :return:
    """
    sha1_obj = hashlib.sha1()
    sha1_obj.update(message.encode('utf-8'))
    return sha1_obj.hexdigest()
