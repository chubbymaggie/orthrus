import os
from collections import namedtuple
import orthrusutils.orthrusutils as util

class BuildEnv(object):

    BEnv = namedtuple('BEnv', ['cc', 'cxx', 'cflags', 'cxxflags', 'ldflags',
                          'ldxxflags', 'misc'])

    BEnv_afl_asan = BEnv('afl-clang', 'afl-clang++', '-O3', '-O3', '', '',
                        {'AFL_USE_ASAN': '1', 'AFL_DONT_OPTIMIZE': '1'})

    BEnv_afl_harden = BEnv('afl-clang', 'afl-clang++', '-O2', '-O2', '', '',
                        {'AFL_HARDEN': '1', 'AFL_DONT_OPTIMIZE': '1'})

    BEnv_afl_harden_softfail = BEnv('afl-clang', 'afl-clang++', '-O2', '-O2', '', '',
                        {'AFL_DONT_OPTIMIZE': '1'})

    BEnv_asan_debug = BEnv('clang', 'clang++', '-g -O0 -fsanitize=address -fno-omit-frame-pointer',
                        '-g -O0 -fsanitize=address -fno-omit-frame-pointer',
                        '-fsanitize=address', '-fsanitize=address', {})

    BEnv_harden_debug = BEnv('clang', 'clang++', '-g -O0 -fstack-protector-all -D_FORTIFY_SOURCE=2 ' \
                        '-fno-omit-frame-pointer', '-g -O0 -fstack-protector-all ' \
                        '-D_FORTIFY_SOURCE=2 -fno-omit-frame-pointer', '', '', {})

    BEnv_harden_debug_softfail = BEnv('clang', 'clang++', '-g -O0 -fstack-protector-all ' \
                        '-fno-omit-frame-pointer', '-g -O0 -fstack-protector-all ' \
                        '-fno-omit-frame-pointer', '', '', {})

    BEnv_gcc_coverage = BEnv('gcc', 'g++', '-g -O0 -fprofile-arcs -ftest-coverage',
                        '-g -O0 -fprofile-arcs -ftest-coverage', '-lgcov', '-lgcov', {})

    BEnv_asan_coverage = BEnv('clang', 'clang++',
                              '-g -O0 -fsanitize=address -fno-omit-frame-pointer -fsanitize-coverage=bb',
                              '-g -O0 -fsanitize=address -fno-omit-frame-pointer -fsanitize-coverage=bb',
                              '-fsanitize=address', '-fsanitize=address', {})
    BEnv_ubsan_coverage = BEnv('clang', 'clang++',
                              '-g -O0 -fsanitize=undefined -fsanitize-coverage=bb',
                              '-g -O0 -fsanitize=undefined -fsanitize-coverage=bb',
                              '-fsanitize=undefined', '-fsanitize=undefined', {})


    def __init__(self, buildenv):

        self.buildenv = os.environ.copy()
        self.exportvars = {}
        self.exportvars['CC'] = buildenv.cc
        self.exportvars['CXX'] = buildenv.cxx
        self.exportvars['CFLAGS'] = buildenv.cflags
        self.exportvars['CXXFLAGS'] = buildenv.cxxflags
        self.exportvars['LDFLAGS'] = buildenv.ldflags
        self.exportvars['LDXXFLAGS'] = buildenv.ldxxflags
        self.exportvars.update(buildenv.misc)

    def getenvdict(self):
        self.buildenv.update(self.exportvars)
        return self.buildenv

class Builder(object):

    def __init__(self, buildenv, configargs, logfile=None):
        self.env = buildenv.getenvdict()
        self.configargs = configargs
        self.logfile = logfile

    def configure(self):

        if not os.path.isfile("configure"):
            return False

        # AFL-fuzz likes statically linked binaries
        # "--disable-shared " +
        command = ["./configure " + " ".join(self.configargs)]

        if not util.run_cmd(command, self.env, self.logfile):
            return False
        return True

    def make_install(self):
        if not os.path.isfile("Makefile"):
            return False

        command = ["make clean && make -j install"]
        if not util.run_cmd(command, self.env, self.logfile):
            return False
        return True