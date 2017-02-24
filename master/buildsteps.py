# -*- python -*-
# ex: set syntax=python:

import string
import re
from buildbot.steps.shell import ShellCommand

class ZFSTestsShellCommand(ShellCommand):
    def __init__(self, **kwargs):
        ShellCommand.__init__(self, **kwargs)

    def describe(self, done=False):
        description = ShellCommand.describe(self,done)
        if done:
            description.append('total: %d ' % self.step_status.getStatistic('total', 0))

            failed = self.step_status.getStatistic('failed', 0)
            if failed > 0:
                description.append('failed: %d' % failed)

            skipped = self.step_status.getStatistic('skipped', 0)
            if skipped > 0:
                description.append('skipped: %d' % skipped)

            passed = self.step_status.getStatistic('passed', 0)
            if passed > 0:
                description.append('passed: %d' % passed)

        return description

    def createSummary(self,log):
        _re_fail_result = re.compile(r'^FAIL\s*(\d*)')
        _re_pass_result = re.compile(r'^PASS\s*(\d*)')
        _re_skip_result = re.compile(r'^SKIP\s*(\d*)')

        failed = 0
        skipped = 0
        passed = 0

        lines = self.getLog('stdio').readlines()
        for l in lines:
            m = _re_fail_result.search(l)
            if m:
                failed = int(m.group(1))
                continue

            m = _re_skip_result.search(l)
            if m:
                skipped = int(m.group(1))
                continue

            m = _re_pass_result.search(l)
            if m:
                passed = int(m.group(1))
                continue

        total = failed + skipped + passed

        self.step_status.setStatistic('total', total)
        self.step_status.setStatistic('failed', failed)
        self.step_status.setStatistic('skipped', skipped)
        self.step_status.setStatistic('passed', passed)
