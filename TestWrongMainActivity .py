import json
import os

from DatabaseConnector import select_Apk_MainActivity, insert_WrongMainActivityTest
from androguard.core.analysis import auto
import sys

PATH_MUTANTS_DIR = "G:\DANTE\/mutantes"


class AndroTest(auto.DirectoryAndroAnalysis):
    def __init__(self, path):
        super(AndroTest, self).__init__(path)
        self.has_crashed = False

    def analysis_apk(self, log, apkobj):
        # Consultar Actividades en la BD
        mutant_main_activity = apkobj.get_main_activity()
        apk_main_activity = select_Apk_MainActivity()

        # Verificando la cantidad de actividades de las APKs
        main_act_mismatch = apk_main_activity == mutant_main_activity

        result = []

        if not main_act_mismatch:
            result.append(mutant_main_activity)

        insert_WrongMainActivityTest(os.path.basename(log.filename), len(result) == 0,
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
    # The directory `PATH_MUTANTS_DIR` should contain some APK files
    "my": AndroTest(PATH_MUTANTS_DIR),
    # Use the default Logger
    "log": auto.DefaultAndroLog,
    # Use maximum of 20 threads
    "max_fetcher": 5,
}

aa = auto.AndroAuto(settings)
aa.go()
