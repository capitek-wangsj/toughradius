#!/usr/bin/env python
#coding=utf-8

import cyclone.auth
import cyclone.escape
import cyclone.web
import decimal
from toughradius.console import models
from toughradius.console.admin.base import BaseHandler
from toughradius.console.admin.customer import account, account_forms
from toughradius.common.permit import permit
from toughradius.common import utils
from toughradius.common.settings import * 

@permit.route(r"/account/pause", u"用户停机",MenuUser, order=2.1000)
class AccountPausetHandler(account.AccountHandler):

    @cyclone.web.authenticated
    def get(self):
        pass