import os.path
import sqlite3
import pandas

class cdb:
    """Cinema Database Class

    Class that loads, verifies and manages access to a Cinema Database
    """

    def __init__(self, path):
        self.tablename = "CINEMA"
        self.path      = path
        self.datapath  = os.path.join(self.path, "data.csv")
        self.extracts  = {} 
        self.parameternames = []
        self.extractnames   = []

    def read(self):
        """Read in a Cinema database.

        Returns true on success, false on failure
        """
        result = self.check_database() 

        if result:
            self.con = sqlite3.connect(":memory:")
            cur = self.con.cursor()
            df = pandas.read_csv(self.datapath, na_filter=False)
            self.parameternames = list(df.columns)
            df.to_sql(self.tablename, self.con, if_exists='append', index=False)

        return result

    def parameter_exists(self, parameter):
        """Check if a parameter exists
        """
        return parameter in self.parameternames

    def extract_parameter_exists(self, parameter):
        """Check if an extract parameter exists
        """
        return parameter in self.extractnames

    def set_extract_parameter_names(self,names):
        """Set the parameter names that are considered extracts
        """
        for n in names:
            self.parameternames.remove(n)
            self.extractnames.append(n)

    def __get_extract_pathname(self): 
        """Get the form for the extract paths 
        """
        return "/" + "/".join(str(elem) for elem in self.parameternames) 
 
#   def __get_extract_path(self, parameters):
#       (path, query) = self.__get_extract_paths(parameters)
#       return path

#   def __get_extract_query(self, parameters):
#       (path, query) = self.__get_extract_paths(parameters)
#       return query

    def __get_extract_paths(self, parameters):
        query = "SELECT {} from {} WHERE ".format(", ".join(self.extractnames), self.tablename)
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
        (extract_path, query) = self.__get_extract_paths(parameters)

        cur = self.con.cursor()
        cur.execute(query)

        extract  = None
        fullpath = None
        for row in cur.fetchall():
            fullpath = os.path.join(self.path, row[0])
            self.extracts[extract_path] = fullpath 
            extract = self.extracts[extract_path]

        return extract 

    def check_database(self):
        return os.path.exists(self.path) and os.path.exists(self.datapath)



