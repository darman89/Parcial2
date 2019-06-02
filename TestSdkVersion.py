import json
import os

from DatabaseConnector import select_Apk_MinSdkVersion, select_Apk_TargetSdkVersion, insert_SdkVersionTest
from androguard.core.analysis import auto
import sys

PATH_MUTANTS_DIR = "G:\DANTE\/mutantes"


class AndroTest(auto.DirectoryAndroAnalysis):
    def __init__(self, path):
        super(AndroTest, self).__init__(path)
        self.has_crashed = False

    def analysis_apk(self, log, apkobj):
        # Consultar Actividades en la BD
        apk_min_sdk_version = select_Apk_MinSdkVersion()
        apk_target_sdk_version = select_Apk_TargetSdkVersion()

        mutant_min_sdk_version = apkobj.get_min_sdk_version()
        mutant_target_sdk_version = apkobj.get_target_sdk_version()

        # Verificando la cantidad de actividades de las APKs
        min_sdk_mismatch = apk_min_sdk_version == mutant_min_sdk_version
        target_sdk_mismatch = apk_target_sdk_version == mutant_target_sdk_version

        result = []

        if not min_sdk_mismatch:
            result.append("min_sdk_version_mismatch: Apk - {}, Mutant - {}".format(apk_min_sdk_version, mutant_min_sdk_version))
        elif not target_sdk_mismatch:
            result.append("target_sdk_mismatch: Apk - {}, Mutant - {}".format(apk_target_sdk_version, mutant_target_sdk_version))

        insert_SdkVersionTest(os.path.basename(log.filename), len(result) == 0,
                              json.JSONEncoder().encode(result))

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
    # Use maximum of 20 threads
    "max_fetcher": 20,
}

aa = auto.AndroAuto(settings)
aa.go()
