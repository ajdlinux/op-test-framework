#!/usr/bin/env python2
# OpenPOWER Automated Test Project
#
# Contributors Listed Below - COPYRIGHT 2018
# [+] International Business Machines Corp.
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
#
# Do a basic sanity check of the Petitboot UI to see if unicode strings are
# being displayed correctly. We do this by moving to the Language screen and
# checking each example string is present. These representations match the
# layout and encoding in ui/ncurses/nc-lang.c

import time
import pexpect
import unittest

import OpTestConfiguration
from common.OpTestSystem import OpSystemState
import logging
import OpTestLogger
log = OpTestLogger.optest_logger_glob.get_logger(__name__)

class Petitbooti18n(unittest.TestCase):
    def setUp(self):
        conf = OpTestConfiguration.conf
        self.cv_SYSTEM = conf.system()

    def runTest(self):
        self.cv_SYSTEM.goto_state(OpSystemState.PETITBOOT)
        log.debug("Test i18n strings appear correctly in Petitboot")

        # Wait a moment for pb-discover to connect
        time.sleep(3)

        my_console = self.cv_SYSTEM.console.get_console()
        my_console.sendcontrol('l') # refresh the screen
        rc = my_console.expect(['Petitboot', pexpect.TIMEOUT, pexpect.EOF], timeout=5)

        my_console.send("l") # key press L
        rc = my_console.expect(['Deutsch', pexpect.TIMEOUT, pexpect.EOF], timeout=5)
        rc = my_console.expect(['English', pexpect.TIMEOUT, pexpect.EOF], timeout=5)
        rc = my_console.expect([u'Espa\u00f1ol'.encode('utf-8'), pexpect.TIMEOUT, pexpect.EOF], timeout=5)
        rc = my_console.expect([u'Fran\u00e7ais'.encode('utf-8'), pexpect.TIMEOUT, pexpect.EOF], timeout=5)
        rc = my_console.expect(['Italiano', pexpect.TIMEOUT, pexpect.EOF], timeout=5)
        rc = my_console.expect([u'\u65e5\u672c\u8a9e'.encode('utf-8'), pexpect.TIMEOUT, pexpect.EOF], timeout=5)
        rc = my_console.expect([u'\ud55c\uad6d\uc5b4'.encode('utf-8'), pexpect.TIMEOUT, pexpect.EOF], timeout=5)
        rc = my_console.expect([u'Portugu\u00eas/Brasil'.encode('utf-8'), pexpect.TIMEOUT, pexpect.EOF], timeout=5)
        rc = my_console.expect([u'\u0420\u0443\u0441\u0441\u043a\u0438\u0439'.encode('utf-8'), pexpect.TIMEOUT, pexpect.EOF], timeout=5)
        rc = my_console.expect([u'\u7b80\u4f53\u4e2d\u6587'.encode('utf-8'), pexpect.TIMEOUT, pexpect.EOF], timeout=5)
        rc = my_console.expect([u'\u7e41\u9ad4\u4e2d\u6587'.encode('utf-8'), pexpect.TIMEOUT, pexpect.EOF], timeout=5)

        # Return to the Petitboot main menu
        my_console.sendcontrol('l') # refresh the screen to Languages
        my_console.send("x") # exit to main petitboot menu
        my_console.sendcontrol('l') # refresh the main petitboot menu
        my_console.sendcontrol('u') # clear from cursor move cursor
        rc = my_console.expect(['x=exit', pexpect.TIMEOUT, pexpect.EOF], timeout=10)

        pass
