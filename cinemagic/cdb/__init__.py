import os.path
import sqlite3
import pandas

class cdb:

    def __init__(self, path):
        self.tablename = "CINEMA"
        self.path      = path
        self.datapath  = os.path.join(self.path, "data.csv")
        self.extracts  = {} 
        self.parameternames = []
        self.extractnames   = []

    def read(self):
        result = os.path.exists(self.path)

        if result:
            self.con = sqlite3.connect(":memory:")
            cur = self.con.cursor()
            df = pandas.read_csv(self.datapath)
            self.parameternames = list(df.columns)
            df.to_sql(self.tablename, self.con, if_exists='append', index=False)

        return result

    def parameter_exists(self, parameter):
        return parameter in self.parameternames

    def extract_parameter_exists(self, parameter):
        return parameter in self.extractnames

    def set_extract_parameter_names(self,names):
        for n in names:
            self.parameternames.remove(n)
            self.extractnames.append(n)

    def get_extract_pathname(self): 
        return "/" + "/".join(str(elem) for elem in self.parameternames) 

    def get_extract_path(self, parameters):
        (path, query) = self.get_extract_paths(parameters)
        return path

    def get_extract_query(self, parameters):
        (path, query) = self.get_extract_paths(parameters)
        return query

    def get_extract_paths(self, parameters):
        query = "SELECT FILE from {} WHERE ".format(self.tablename)
        res = ""
        
        path = "/"
        first = True
        for key in self.parameternames:
            if not first:
                query = query + " AND "
                path = path + "/"
            else:
                first = False

            if key in parameters:
                value = parameters[key]
            else:
                value = Null

            query = query + "{} = \'{}\' ".format(key, value)
            path = path + value  

        return path, query

    def get_extract(self, parameters):
        (extract_path, query) = self.get_extract_paths(parameters)

        cur = self.con.cursor()
        cur.execute(query)

        extract  = None
        fullpath = None
        for row in cur.fetchall():
            fullpath = os.path.join(self.path, row[0])
            self.extracts[extract_path] = fullpath 
            extract = self.extracts[extract_path]

        return extract 
