import glob
import mutagen
import os
from tabulate import tabulate
import re

from funcs import *

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
                    if field.upper() in file:
                        file[field] = file[field.upper()]
                    elif field == "text" and "COMMENTS" in file:
                        file["text"] = file["COMMENTS"]
                    else:
                        file[field] = input("{} missing in file {}, please enter value: ".format(field,os.path.basename(file.filename)))
                    file.save()
                    file.tags.pprint()

    def list_files(self, files=None):
        if files == None:
            files = self.files

        field_table = {"filename":[]}
        for path,file in files.items():
            field_table["filename"].append(os.path.basename(file.filename))
            for field,value in file.items():
                if field not in field_table:
                    field_table[field] = [None]*(len(field_table["filename"])-1)
                field_table[field] += value

            w_l = len(field_table["filename"])
            for field in field_table:
                if len(field_table[field]) < w_l:
                    field_table[field].append(None)

        headers = sorted(list(field_table), key=lambda x:"0" if x == "filename" else x)
        table = [headers]
        table_rows = []
        for i in range(len(field_table["filename"])):
            row = [field_table[field][i] for field in headers]
            table_rows.append(row)

        table += sorted(table_rows, key=lambda x: x[0])

        if len(table) > 1:
            print(tabulate(table, headers="firstrow", tablefmt="psql"))
        else:
            print("No files")

    def search(self, query=None):
        if not query:
            query = input("Query: ")

        query_re = re.compile(query, flags=re.IGNORECASE)

        matches = {}

        for path,file in self.files.items():
            for field,value in file.items():
                if query_re.search(value[0]):
                    matches[path] = file


        self.list_files(files=matches)

    def select_file(self,cb, files=None):
        if files == None:
            files = self.files
        file_menu = [[os.path.basename(x),cb,v] for x,v in files.items()]
        print(file_menu)

    def edit_file(self,file=None):
        if file==None:
            file = self.select_file(self.edit_file)
        else:
            pass
