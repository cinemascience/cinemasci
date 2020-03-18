import os.path
import sqlite3
import pandas

class cdb:
    """Cinema Database Class

    Class that loads, verifies and manages access to a Cinema Database.

    Two important definitions are:
    - parameter path A slash-separated string that defines an ordered set of parameters that designate a set of extracts.
	- Example: `/phi/theta/variable`
    - extract path A specific instance of a *parameter path*, giving values for each parameter.
        - Example: `/0/90/temperature`
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

    def __get_extract_paths(self, parameters):
        """Get an extract path for a set of parameters
        
        An extract path is a string that embodies a set of (key, value) pairs for the
        parameters in a cinema database. For example, if the parameter path is

           /phi/theta
        
        Then some possible extract paths are:

          /10/10
          /20/24.5
          ...

        These can provide a unique hash for the extracts uniquely defined by the set of values
        """
        query = "SELECT {} from {} WHERE ".format(", ".join(self.extractnames), self.tablename)
        res = ""

        # print("query: {}".format(query))
        
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

        # print("extract path: {}".format(path))
        return path, query

    def get_extracts(self, parameters):
        (extract_path, query) = self.__get_extract_paths(parameters)

        cur = self.con.cursor()
        cur.execute(query)

        extracts = [] 
        fullpath = None
        for row in cur.fetchall():
            self.extracts[extract_path] = [] 
            for r in row:
                fullpath = os.path.join(self.path, r)
                self.extracts[extract_path].append(fullpath)
                extracts.append(fullpath)

        return extracts 

    def check_database(self):
        return os.path.exists(self.path) and os.path.exists(self.datapath)

#   def __get_extract_path(self, parameters):
#       (path, query) = self.__get_extract_paths(parameters)
#       return path

#   def __get_extract_query(self, parameters):
#       (path, query) = self.__get_extract_paths(parameters)
#       return query

