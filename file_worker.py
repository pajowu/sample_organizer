import glob
import mutagen
import os
from tabulate import tabulate

class FileWorker():
    def __init__(self,config, path_prefix=""):
            self.config = config
            self.path_prefix = path_prefix

            self.files = {}
            for i in glob.glob(self.path_prefix + "*.ogg"):
                self.files[i] = mutagen.File(i)

            self.required_fields = [n for n,v in self.config["fields"].items() if type(v) == dict and "required" in v and v["required"]]


    def check_fields(self,file=None,fields=None):
        if not fields:
            fields = self.required_fields
        if not file:
            for path,file in self.files.items():
                self.check_fields(file=file,fields=fields)
        else:
            missing_fields = set(fields) - set(file)
            if len(missing_fields) != 0:
                for field in missing_fields:
                    file[field] = input("{} missing in file {}, please enter value: ".format(field,os.path.basename(file.filename)))
                    file.save()
                    file.tags.pprint()

    def list_files(self):
        field_table = {"filename":[]}
        for path,file in self.files.items():
            field_table["filename"].append(os.path.basename(file.filename))
            for field,value in file.items():
                if field not in field_table:
                    field_table[field] = [None]*(len(field_table["filename"])-1)
                field_table[field] += value

            w_l = len(field_table["filename"])
            for field in field_table:
                if len(field_table[field]) < w_l:
                    field_table[field].append(None)

        print(field_table)

        headers = sorted(list(field_table), key=lambda x:"0" if x == "filename" else x)
        table = [headers]
        table_rows = []
        for i in range(len(field_table["filename"])):
            print(headers)
            row = [field_table[field][i] for field in headers]
            table_rows.append(row)

        table += sorted(table_rows, key=lambda x: x[0])

        print(tabulate(table, headers="firstrow"))
