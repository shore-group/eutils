# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

import lxml.etree as le

from .exceptions import EutilsError
from .queryservice import QueryService
from .xmlfacades.dbsnp import ExchangeSet
from .xmlfacades.einforesult import EInfoResult
from .xmlfacades.entrezgeneset import EntrezgeneSet
from .xmlfacades.esearchresult import ESearchResult
from .xmlfacades.gbset import GBSet
from .xmlfacades.pubmedarticleset import PubmedArticleSet
from .xmlfacades.pubmedcentralarticleset import PubmedCentralArticleSet


logger = logging.getLogger(__name__)


class Client(object):
    """class-based access to NCBI E-Utilities, returning Python classes
    with rich data accessors

    """

    def __init__(self, cache=False, api_key=None):
        """
        :param str cache: passed to QueryService, which see for explanation
        :param str api_key: API key from NCBI
        :raises EutilsError: if cache file couldn't be created

        """

        self._qs = QueryService(cache=cache, api_key=api_key)


    @property
    def databases(self):
        """
        list of databases available from eutils (per einfo query)
        """
        try:
            return self._databases
        except AttributeError:
            self._databases = self.einfo().databases
            return self._databases

    def einfo(self, db=None):
        """query the einfo endpoint

        :param db: string (optional)
        :rtype: EInfo or EInfoDB object

        If db is None, the reply is a list of databases, which is returned
        in an EInfo object (which has a databases() method).

        If db is not None, the reply is information about the specified
        database, which is returned in an EInfoDB object.  (Version 2.0
        data is automatically requested.)
        """

        if db is None:
            return EInfoResult(self._qs.einfo()).dblist
        return EInfoResult(self._qs.einfo({'db': db, 'version': '2.0'})).dbinfo

    def esearch(self, db, term):
        """query the esearch endpoint
        """
        return ESearchResult(self._qs.esearch({'db': db, 'term': term, 'usehistory': 'y'}))

    def efetch(self, args):
        """query the efetch endpoint
        """
        return self._qs.efetch(args)


# <LICENSE>
# Copyright 2015 eutils Committers
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.
# </LICENSE>
