# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 13:28:13 2021

@author: hadas
"""

from sqlalchemy import create_engine
import mysql.connector
from datetime import datetime
import pandas as pd

# Create Connection, save user, passward into privates
class server:
    def __init__(self,user,passward,ip='127.0.0.1',port=3306,host = "localhost"):
        self.MYSQL_USER = user
        self.MYSQL_PASSWORD = passward
        self.MYSQL_HOST_IP = ip
        self.MYSQL_PORT	= port
        self.MYSQL_HOST = host
        self.tablesStruct = tableStruct()
    
    def connect2server(self):
        self.mydb = mysql.connector.connect(host=self.MYSQL_HOST,user=self.MYSQL_USER,passwd=self.MYSQL_PASSWORD)
        self.mycursor = self.mydb.cursor()
        return 
    
    def showDBs(self):
        self.mycursor.execute("SHOW DATABASES")
        print("Databases in server:")
        for x in self.mycursor:
            print(x)

    def createDB(self,dbname):
        self.connect2server()
        self.mycursor.execute(f"DROP DATABASE IF EXISTS {dbname.upper()}");
        # create a new database
        self.mycursor.execute(f"CREATE DATABASE {dbname.upper()}")
        # showing that the database has been created
        self.showDBs()
        return
    
    def connect2serverDB(self,db):
        # reconnect to database from server
        self.mydb = mysql.connector.connect(host=self.MYSQL_HOST,
                                            user=self.MYSQL_USER,
                                            passwd=self.MYSQL_PASSWORD,
                                            database=db.upper())
        self.mycursor = self.mydb.cursor()
        return self.mycursor
    
    def showTables(self):
        self.mycursor.execute("show tables")
        print("Tables in DB:")
        for i in self.mycursor:
             print(i)
             
    def createNewTable(self,tableName,dbname="",features = [],fname=""):
        if dbname!="":
            self.connect2serverDB(dbname)
        if fname !="":
            self.tablesStruct.importCSV2table(fname)
        if len(features):
            headers = features
        else:
            headers = self.tablesStruct.tables[fname].columns
        
        self.mycursor.execute(f"drop table if exists {tableName.lower()}")
        
        tbl_ftrs = f"CREATE TABLE {tableName.lower()} ({headers[0]} TIMESTAMP, "
        for i in headers[1:]:
                tbl_ftrs+=f"{i} VARCHAR(255), "
        tbl_ftrs+=f"primary key ({headers[0]},{headers[1]}))"
        # print(tbl_ftrs)
        self.mycursor.execute(tbl_ftrs)
        self.showTables()
     
    def insertData2Table(self,fname,tableName,dbName):
        self.con = create_engine('mysql+pymysql://'+self.MYSQL_USER+':'+self.MYSQL_PASSWORD+'@'+self.MYSQL_HOST_IP+':'+str(self.MYSQL_PORT)+'/'+dbName)
        # change Nans to Nones as used by mysql
        self.tablesStruct.tables[fname] = self.tablesStruct.tables[fname].where(pd.notnull(self.tablesStruct.tables[fname]),None) # where changes false values to None, instead of NANs
        self.tablesStruct.tables[fname].to_sql(name=tableName.lower(), con=self.con,index=False, if_exists="append")


class tableStruct:
    def __init__(self):
        # allocate a dataframe
        self.tables = {}
    def importCSV2table(self, fname):
        try:
            # read csv file into table variable
            self.tables[fname] = pd.read_csv(fname)
            # convert time-stamp format to mysql readable one
            if "Timestamp" in self.tables[fname].columns:
                for i in range(self.tables[fname].shape[0]):
                    self.tables[fname].loc[i,"Timestamp"] = datetime.strptime(self.tables[fname].loc[i,"Timestamp"][:-6], '%Y/%m/%d %I:%M:%S %p')
        except FileNotFoundError:
            print("incorrect file name")
        except:
            print("table importing went wrong")

def main():
    s = server('root','12345')
    s.createDB("shir")
    s.tablesStruct.importCSV2table('engineer.csv')
    mycursor = s.mycursor
    mycursor.execute("CREATE TABLE shir.engineer (id INT, name VARCHAR(45) , seniority VARCHAR(45), PRIMARY KEY (id))")
    #mycursor.execute("CREATE TABLE shir.department (number_id INT NOT NULL,name VARCHAR(45) NULL, PRIMARY KEY (`number_id`))")
    #mycursor.execute("CREATE TABLE shir.medical_equiment (number_id INT NOT NULL,name VARCHAR(45) NULL,maintennance_data DATE NULL,department_number_id INT NULL, PRIMARY KEY (`number_id`))")
    #mycursor.execute("ALTER TABLE shir.medical_equiment ADD FOREIGN KEY (department_number_id)REFERENCES department(number_id)")
    #mycursor.execute("CREATE TABLE chip (number_chip INT, placement_date DATE , battery_life INT,number_equiment INT, PRIMARY KEY (number_chip))")
    #mycursor.execute("ALTER TABLE shir.chip ADD FOREIGN KEY (number_equiment)REFERENCES medical_equiment(number_id)")
    #mycursor.execute("CREATE TABLE inspection (date_inspection DATE, number_equiment INT , id_engineer INT,condition_ VARCHAR(45), PRIMARY KEY (date_inspection,number_equiment,id_engineer))")
    #mycursor.execute("ALTER TABLE `shir`.`inspection` ADD CONSTRAINT `namber_equiment` FOREIGN KEY (`number_equiment`) REFERENCES `shir`.`medical_equiment` (`number_id`) ON DELETE NO ACTION ON UPDATE NO ACTION, ADD CONSTRAINT `id_engineer` FOREIGN KEY (`id_engineer`) REFERENCES `shir`.`engineer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION")
    s.insertData2Table('engineer.csv','engineer','shir')
    return
if __name__=="__main__":
    main()
    

