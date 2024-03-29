import json
import os

from DatabaseConnector import insert_ApkProperties, create_ApkTable
from androguard.core.analysis import auto
import sys

PATH_BASELINE_APK = "G:\DANTE\/baseline"


class AndroTest(auto.DirectoryAndroAnalysis):
    def __init__(self, path):
        super(AndroTest, self).__init__(path)
        self.has_crashed = False

    def analysis_apk(self, log, apkobj):
        # Crear Table de la base de datos
        create_ApkTable()

        # Capturar la información de la APK
        app_name = apkobj.get_app_name()
        main_activity = apkobj.get_main_activity()
        activities_labels = json.JSONEncoder().encode(list(apkobj.get_all_attribute_value("activity", "label")))
        activities_names = json.JSONEncoder().encode(list(apkobj.get_all_attribute_value("activity", "name")))
        services_names = json.JSONEncoder().encode(list(apkobj.get_all_attribute_value("service", "name")))
        permissions_list = json.JSONEncoder().encode(list(apkobj.get_permissions()))
        min_sdk_version = apkobj.get_min_sdk_version()
        target_sdk_version = apkobj.get_target_sdk_version()
        strings_app = json.JSONEncoder().encode(list(apkobj.get_android_resources().get_resolved_strings().values()))

        # Insertar la Información en la BD
        insert_ApkProperties(app_name, main_activity, min_sdk_version, target_sdk_version, activities_labels,
                             activities_names, services_names, permissions_list, strings_app)

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
    # The directory `PATH_BASELINE_APK` should contain some APK files
    "my": AndroTest(PATH_BASELINE_APK),
    # Use the default Logger
    "log": auto.DefaultAndroLog,
    # Use maximum of 1 threads
    "max_fetcher": 1,
}

aa = auto.AndroAuto(settings)
aa.go()
