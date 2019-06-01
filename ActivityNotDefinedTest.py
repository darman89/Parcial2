import json
import os

from DatabaseConnector import select_Apk_ActivitiesNames, insert_ApkProperties, insert_ActivityNotDefinedTest
from androguard.core.analysis import auto
import sys

PATH_BASELINE_APK = "G:\DANTE\/mutantes"


class AndroTest(auto.DirectoryAndroAnalysis):
    def __init__(self, path):
        super(AndroTest, self).__init__(path)
        self.has_crashed = False

    def analysis_apk(self, log, apkobj):
        # Consultar Actividades en la BD
        diff = set()
        activities_names = select_Apk_ActivitiesNames()
        mutant_activities_names = list(apkobj.get_all_attribute_value("activity", "name"))
        # Verificando la cantidad de actividades de las APKs
        act_mismatch = len(activities_names) == len(mutant_activities_names)

        if not act_mismatch:
            diff = set(activities_names) - set(mutant_activities_names)

        insert_ActivityNotDefinedTest(os.path.basename(log.filename), act_mismatch,
                                      json.JSONEncoder().encode(list(diff)))

    def finish(self, log):
        # This method can be used to save information in `log`
        # finish is called regardless of a crash, so maybe store the
        # information somewhere
        if self.has_crashed:
            print("Analysis of {} has finished with Errors".format(os.path.basename(log)))
        else:
            print("Analysis of {} has finished!".format(os.path.basename(log.filename)))

    def crash(self, log, why):
        # If some error happens during the analysis, this method will be
        # called
        self.has_crashed = True
        print("Error during analysis of {}: {}".format(log, why), file=sys.stderr)


settings = {
    # The directory `some/directory` should contain some APK files
    "my": AndroTest(PATH_BASELINE_APK),
    # Use the default Logger
    "log": auto.DefaultAndroLog,
    # Use maximum of 20 threads
    "max_fetcher": 20,
}

aa = auto.AndroAuto(settings)
aa.go()