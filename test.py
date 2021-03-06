#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import os
import sys
import zipfile

try:
    from .apkverify import ApkSignature
except (ValueError, ImportError):
    from apkverify import ApkSignature

if __name__ == '__main__':
    test_dir = os.path.join(os.path.abspath('.'), 'apksig')
    log = open(test_dir + '.py%d.txt' % (sys.version_info[0]), 'wb')
    for filename in os.listdir(test_dir):
        file_path = os.path.join(test_dir, filename)
        if not (os.path.isfile(file_path) and zipfile.is_zipfile(file_path)):
            continue
        print('=' * 79)
        print('File: {}'.format(file_path))
        log_verify = None
        try:
            a = ApkSignature(os.path.abspath(file_path))
            print(a.apkpath)
            signature_version = a.is_sigv2()
            v_auto = a.verify()  # auto check version
            v_ver1 = a.verify(1)  # force check version 1
            v_ver2 = a.verify(2)  # force check version 2
            print('Verify: {}, {}, {}, {}'.format(signature_version, v_auto, v_ver1, v_ver2))
            log_verify = v_ver1, v_ver2
            for line in a.errors:
                print('Error: {}'.format(line))
            all_certs = a.all_certs()
            sig_certs = a.get_certs()
            all_chain = a.get_chains()
            print(all_certs)
            print(sig_certs)
            print(all_chain)
            all_certs = a.all_certs(readable=True)
            sig_certs = a.get_certs(readable=True)
            all_chain = a.get_chains(readable=True)
            print(all_certs)
            print(sig_certs)
            print(all_chain)
            for one_chain in all_chain:  # 签名信息(一般只有一个)
                print('\t[chain]'.ljust(79, '-'))
                for i in range(0, len(one_chain)):  # 签名的证书链()
                    cert_prt, cert_sub, cert_iss = one_chain[i]
                    print('\t\t[%2d] [certprt]' % i, cert_prt)
                    print('\t\t\t [subject]', cert_sub)
                    print('\t\t\t [ issuer]', cert_iss)
        except Exception as e:
            import logging

            logging.exception(e)
            print(e)
            log_verify = type(e)
        log.write(('%s\t%s\n' % (log_verify, filename)).encode('utf8'))
        log.flush()
    log.close()
