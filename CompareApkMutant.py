import re
import subprocess
import os

from DatabaseConnector import insert_CompareApkMutantMethods
from androguard.core.analysis import auto
import sys

PATH_BASELINE_APK = "G:\DANTE\/baseline\com.evancharlton.mileage_3110.apk"
PATH_MUTANTS_DIR = "G:\DANTE\/mutantes"


class AndroTest(auto.DirectoryAndroAnalysis):
    def __init__(self, path):
        super(AndroTest, self).__init__(path)
        self.has_crashed = False

    def analysis_apk(self, log, apkobj):
        result = True
        diff = subprocess.run(['./androsim.exe', '-i', PATH_BASELINE_APK,
                               log.filename, '-c', "ZLIB", '-n', '-d', '-e', "^Lcom/artfulbits"],
                              stdout=subprocess.PIPE,
                              encoding='utf-8').stdout
        if len(re.findall("--> methods: 100.000000%", diff)) == 1:
            diff = 'Los métodos de ambas APK son Idénticos'
        else:
            diff = diff.replace('\t', "").replace('\n', ' *** ')
            result = False

        insert_CompareApkMutantMethods(os.path.basename(log.filename), result, diff)

    def finish(self, log):
        # This method can be used to save information in `log`
        # finish is called regardless of a crash, so maybe store the
        # information somewhere

        if self.has_crashed:
            print("Analysis of {} has finished with Errors".format(os.path.basename(log.filename)))
        else:
            print("Analysis of {} has finished!".format(os.path.basename(log.filename)))

    def crash(self, log, why):
        # If some error happens during the analysis, this method will be
        # called
        self.has_crashed = True
        print("Error during analysis of {}: {}".format(log, why), file=sys.stderr)


settings = {
    # The directory `some/directory` should contain some APK files
    "my": AndroTest(PATH_MUTANTS_DIR),
    # Use the default Logger
    "log": auto.DefaultAndroLog,
    # Use maximum of 5 threads
    "max_fetcher": 5,
}

aa = auto.AndroAuto(settings)
aa.go()
