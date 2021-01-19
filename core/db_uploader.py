import os
import django
import csv
import sys


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shabang.settings")
django.setup()

from facility.models import School, SchoolGrade, Subway, SubwayLine, ConvenientStore, Cafe

def insert_school_grades():
        CSV_PATH_PRODUCTS = 'grade.csv'
        with open(CSV_PATH_PRODUCTS) as in_file:
                data_reader = csv.reader(in_file)
                next(data_reader, None)
                for row in data_reader:
                        SchoolGrade.objects.create(grade=row[0])
        print("==========================update: school_grades")

def insert_schools_elementary():
        CSV_PATH_PRODUCTS = 'elementary.csv'
        with open(CSV_PATH_PRODUCTS) as in_file:
                data_reader = csv.reader(in_file)
                next(data_reader, None)
                for row in data_reader:
                        school_grade = SchoolGrade.objects.get(grade='초등학교')

                        School.objects.create(name=row[0], longitude=row[1], latitude=row[2], school_grade=school_grade)
        print("==========================update: schools_elementary")

def insert_schools_middle():
        CSV_PATH_PRODUCTS = 'middle.csv'
        with open(CSV_PATH_PRODUCTS) as in_file:
                data_reader = csv.reader(in_file)
                next(data_reader, None)
                for row in data_reader:
                        school_grade = SchoolGrade.objects.get(grade='중학교')

                        School.objects.create(name=row[0], longitude=row[1], latitude=row[2], school_grade=school_grade)
        print("==========================update: schools_middle")

def insert_schools_high():
        CSV_PATH_PRODUCTS = 'high.csv'
        with open(CSV_PATH_PRODUCTS) as in_file:
                data_reader = csv.reader(in_file)
                next(data_reader, None)
                for row in data_reader:
                        school_grade = SchoolGrade.objects.get(grade='고등학교')

                        School.objects.create(name=row[0], longitude=row[1], latitude=row[2], school_grade=school_grade)
        print("==========================update: schools_high")

def insert_subway_lines():
        CSV_PATH_PRODUCTS = 'line.csv'
        with open(CSV_PATH_PRODUCTS) as in_file:
                data_reader = csv.reader(in_file)
                next(data_reader, None)
                for row in data_reader:
                        SubwayLine.objects.create(line=row[0])
        print("==========================update: subway_lines")

def insert_subways():
        CSV_PATH_PRODUCTS = 'subway.csv'
        with open(CSV_PATH_PRODUCTS) as in_file:
                data_reader = csv.reader(in_file)
                next(data_reader, None)
                for row in data_reader:
                        subway_line = SubwayLine.objects.get(line=row[3])
                        Subway.objects.create(name=row[0], longitude=row[1], latitude=row[2], subway_line=subway_line)
        print("==========================update: subways")

def insert_convenient_stores():
        CSV_PATH_PRODUCTS = 'store.csv'
        with open(CSV_PATH_PRODUCTS) as in_file:
                data_reader = csv.reader(in_file)
                next(data_reader, None)
                for row in data_reader:
                        ConvenientStore.objects.create(name=row[0], longitude=row[1], latitude=row[2])
        print("==========================update: convenient_stores")

def insert_cafes():
        CSV_PATH_PRODUCTS = 'cafe.csv'
        with open(CSV_PATH_PRODUCTS) as in_file:
                data_reader = csv.reader(in_file)
                next(data_reader, None)
                for row in data_reader:
                        Cafe.objects.create(name=row[0], longitude=row[1], latitude=row[2])
        print("==========================update: convenient_cafes")

### uploader 실행문
#insert_school_grades()
#insert_schools_elementary()
#insert_schools_middle()
#insert_schools_high()
#insert_subway_lines()
#insert_subways()
#insert_convenient_stores()
#insert_cafes()
