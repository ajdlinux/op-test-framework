#!/usr/bin/env python2
# IBM_PROLOG_BEGIN_TAG
# This is an automatically generated prolog.
#
# $Source: op-test-framework/testcases/OpTestDPO.py $
#
# OpenPOWER Automated Test Project
#
# Contributors Listed Below - COPYRIGHT 2017
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
# IBM_PROLOG_END_TAG

#  @package DPO.py
#       Delayed Power off testcase is to test OS graceful shutdown request
#       to be notified from OPAL and OS should process the request.
#       We will use "ipmitool power soft" command to issue DPO.

from common.OpTestConstants import OpTestConstants as BMC_CONST
from common.OpTestError import OpTestError

import unittest
import pexpect
import OpTestConfiguration
from common.OpTestSystem import OpSystemState
import common.OpTestQemu as OpTestQemu

import logging
import OpTestLogger
log = OpTestLogger.optest_logger_glob.get_logger(__name__)

class Base(unittest.TestCase):
    def setUp(self):
        conf = OpTestConfiguration.conf
        self.cv_IPMI = conf.ipmi()
        self.cv_SYSTEM = conf.system()
        self.cv_HOST = conf.host()
        self.bmc_type = conf.args.bmc_type
        self.util = self.cv_SYSTEM.util


class DPOSkiroot(Base):

    def setup_test(self):
        self.cv_SYSTEM.goto_state(OpSystemState.PETITBOOT_SHELL)
        self.host = "Skiroot"
        log.debug("Starting DPO test in Skiroot")

    ##
    # @brief This will test DPO feature in skiroot and Host
    #
    # @return BMC_CONST.FW_SUCCESS or raise OpTestError
    #
    def runTest(self):
        self.setup_test()
        # retry added for IPMI cases, seems more sensitive with initial start of state=4
        if isinstance(self.cv_SYSTEM.console, OpTestQemu.QemuConsole):
            raise self.skipTest("Performing \"ipmitool power soft\" will terminate QEMU so skipped")
        self.cv_SYSTEM.console.run_command("uname -a", retry=5)
        if self.host == "Host":
            self.cv_SYSTEM.load_ipmi_drivers(True)
        self.cv_SYSTEM.console.sol.sendline("ipmitool power soft")
        rc = self.cv_SYSTEM.console.sol.expect_exact(["reboot: Power down",
                                      "Chassis Power Control: Soft",
                                      "Power down",
                                      "Invalid command",
                                      "Unspecified error",
                                      "Could not open device at",
                                      pexpect.TIMEOUT,
                                      pexpect.EOF], timeout=120)
        self.assertIn(rc, [0, 1, 2], "Failed to power down")
        rc = self.cv_SYSTEM.sys_wait_for_standby_state()
        log.debug(rc)
        self.cv_SYSTEM.set_state(OpSystemState.OFF)
        self.cv_SYSTEM.goto_state(OpSystemState.OS)

class DPOHost(DPOSkiroot):
    def setup_test(self):
        self.host = "Host"
        self.cv_SYSTEM.goto_state(OpSystemState.OS)
        self.util.PingFunc(self.cv_HOST.ip, BMC_CONST.PING_RETRY_POWERCYCLE)
        log.debug("Starting DPO test in Host")
