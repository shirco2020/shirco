# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 19:49:55 2021

@author: shir cohen
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 20:37:41 2021

@author: hadas
"""
from serverController import * # this includes server and tableStruct classes

class DBBuildup(server):
    def __init__(self,user,passward,dbname,ip='127.0.0.1',port=3306,host = "localhost"):
        super().__init__(user,passward)
        super().connect2serverDB(dbname)
        return
    def deleteTable(self,tableName):
        self.mycursor.execute(f"drop table if exists {tableName.lower()}")
        return
    def createNewTable(self,tableName,features = [], feature_types = [],pks = [],fks = [],reference_table = "",references = [],fname=""):
        if fname !="":
            self.tablesStruct.importCSV2table(fname)
            if not len(features):
                features = self.tablesStruct.tables[fname].columns
            if not len(feature_types):
                feature_types =["TIMESTAMP"]+["VARCHAR(255)"]*(len(features)-1)
        
        tbl_ftrs = f"CREATE TABLE {tableName.lower()} ("
        for f,t in zip(features,feature_types):
            tbl_ftrs+=f"{f} {t}, "
        # adding primary keys to the table creation command:
        if len(pks):
            tbl_ftrs+="primary key ("
            for i,k in enumerate(pks):
                if i==len(pks)-1:
                    if len(fks):
                        tbl_ftrs+=f"{k}), "
                    else:
                        tbl_ftrs+=f"{k})"
                else:
                    tbl_ftrs+=f"{k}, "

        # adding foreign keys to the table creation command:
            print("FKS:" + str(len(fks)))
        if len(fks):
            if any(isinstance(x, list) for x in fks):
                for i,l in enumerate(fks):
                    tbl_ftrs+="foreign key ("
                    for j,k in enumerate(l):
                        if j==len(l)-1:
                            tbl_ftrs+=f"{k}) "
                        else:
                            tbl_ftrs+=f"{k},"
                    # adding referencing to the table FKs:
                    tbl_ftrs+=f"references {reference_table[i]}("
                    for j,k in enumerate(references[i]):
                        if j==len(l)-1:
                            tbl_ftrs+=f"{k}"
                        else:
                            tbl_ftrs+=f"{k},"
                    if i==len(fks)-1:
                        tbl_ftrs+=")"
                    else:
                        tbl_ftrs+="), "
            else:
                tbl_ftrs+="foreign key ("
                for i,k in enumerate(fks):
                    if i==len(fks)-1:
                        tbl_ftrs+=f"{k}) "
                    else:
                        tbl_ftrs+=f"{k},"
                # adding referencing to the table FKs:
                tbl_ftrs+=f"references {reference_table}("
                for i,k in enumerate(references):
                    if i==len(references)-1:
                        tbl_ftrs+=f"{k})"
                    else:
                        tbl_ftrs+=f"{k},"
        tbl_ftrs+=")"
        print(tbl_ftrs)
        self.mycursor.execute(tbl_ftrs)
        self.showTables()
        
db = DBBuildup('root','12345',"shir")
db.deleteTable("MEDICAL_EQUIMENT")
db.deleteTable("AsthmaSOAP")
#db.createNewTable("AsthmaSOAP",fname = "Asthma EMR.csv",pks = ["Timestamp","FirstName","LastName"])
#db.insertData2Table("Asthma EMR.csv","AsthmaSOAP","shir")
# and build rest of tables according to the model diagram:
tablesNames = ["DEPARTMENT","ENGINEER","MEDICAL_EQUIMENT","INSPECTION","CHIP"]
fnames = ["DEPARTMENT.csv","ENGINEER.csv","MEDICAL_EQUIMENT.csv","INSPECTION.csv","CHIP.csv"]
featureNames = [["number_ID","name"],
                ["ID","Name","Seniority"],
                ["Number_ID","Name","Maintennance_Date","Department_Number_ID"],
                ["date_inspecion","number_equiment","id_engineer","condition"],
                ["number_chip","placement_date","battery_life","number_equiment"]]
featureTypes = [["INT"]*1+["VARCHAR(255)"]*1,
                 ["INT"]*1+["VARCHAR(255)"]*1+["INT"]*1,
                 ["INT"]*1+["VARCHAR(255)"]*1+["date"]*1+["INT"]*1,
                 ["date"]*1+["INT"]*2+["VARCHAR(255)"]*1,
                 ["INT"]*1+["date"]*1+["INT"]*2]
primaryKeys = [["number_ID"],
               ["ID"],
               ["Number_ID"],
               ["date_inspecion","number_equiment","id_engineer"],
               ["number_chip"]]
foreignKeys = [[],
               [],
               ["Department_Number_ID"],
               [["number_equiment"],["id_engineer"]],
               ["number_equiment"]]
references = [[],
              [],
              ["number_ID"],
              ["Number_ID"],
              [["Number_ID"],["ID"]]]
referenceTables = ["",
                   "",
                   "DEPARTMENT",
                   ["MEDICAL_EQUIMENT","ENGINEER"],
                   "MEDICAL_EQUIMENT"]
db.deleteTable("DEPARTMENT")
db.deleteTable("ENGINEER")
db.deleteTable("MEDICAL_EQUIMENT")
db.deleteTable("INSPECTION")
db.deleteTable("CHIP")

for i in range(len(tablesNames)):
    db.createNewTable(tablesNames[i],
                      features = featureNames[i], 
                      feature_types = featureTypes[i],
                      pks = primaryKeys[i],
                      fks = foreignKeys[i],
                      reference_table = referenceTables[i],
                      references = references[i],
                      fname = fnames[i])
# insert data to tables from csv files
for i in range(len(tablesNames)):
    db.insertData2Table(fnames[i],tablesNames[i],"shir")
