# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 18:31:59 2021

@author: shirc
"""

from sqlalchemy import create_engine
import mysql.connector
from datetime import datetime
import pandas as pd


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="shir"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE engineer (id INT, name VARCHAR(45) , seniority VARCHAR(45), PRIMARY KEY (id))")
mycursor.execute("CREATE TABLE department (number_id INT NOT NULL,name VARCHAR(45) NULL, PRIMARY KEY (`number_id`))")
mycursor.execute("CREATE TABLE medical_equiment (number_id INT NOT NULL,name VARCHAR(45) NULL,maintennance_data DATE NULL,department_number_id INT NULL, PRIMARY KEY (`number_id`))")
mycursor.execute("ALTER TABLE shir.medical_equiment ADD FOREIGN KEY (department_number_id)REFERENCES department(number_id)")
mycursor.execute("CREATE TABLE chip (number_chip INT, placement_date DATE , battery_life INT,number_equiment INT, PRIMARY KEY (number_chip))")
mycursor.execute("ALTER TABLE shir.chip ADD FOREIGN KEY (number_equiment)REFERENCES medical_equiment(number_id)")
mycursor.execute("CREATE TABLE inspection (date_inspection DATE, number_equiment INT , id_engineer INT,condition_ VARCHAR(45), PRIMARY KEY (date_inspection,number_equiment,id_engineer))")
mycursor.execute("ALTER TABLE `shir`.`inspection` ADD CONSTRAINT `namber_equiment` FOREIGN KEY (`number_equiment`) REFERENCES `shir`.`medical_equiment` (`number_id`) ON DELETE NO ACTION ON UPDATE NO ACTION, ADD CONSTRAINT `id_engineer` FOREIGN KEY (`id_engineer`) REFERENCES `shir`.`engineer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION")

mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)