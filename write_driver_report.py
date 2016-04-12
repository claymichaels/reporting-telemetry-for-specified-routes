#!/usr/bin/env python
# Clay Michaels

from sys import argv, exit
import MySQLdb
import openpyxl
from os import listdir
import logging

logger = logging.getLogger('puller')
handler = logging.FileHandler('log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# FM credentials
DB_IP = '<SNIPPED IP>'
DB_USER = '<SNIPPED USER>'
DB_PW = '<SNIPPED PASS>'
DB_NAME = '<SNIPPED DB>'


routes_to_pull = ['<SNIPPED LIST OF ROUTES>']

train_translation = {'<SNIPPED DICT OF CAR# TO TRAINSET>'}

gps_square = {'lat1':'<SNIPPED>', 'lat2':'<SNIPPED>', 'long1':'<SNIPPED>', 'long2':'<SNIPPED>3'}

for filename in listdir('schedules_from_customer'):
    try:
        workbook = openpyxl.load_workbook('schedules_from_customer/%s' % filename)
        worksheet = workbook['Sheet1']
        logger.info('Opened schedule %s' % filename)
        if worksheet['A7'].value in train_translation:
            ccu = train_translation[worksheet['A7'].value]
        else:
            ccu = worksheet['A7'].value
        i =7 # start on 7th row to skip the headers etc
        while worksheet['A%i' % i].value: # ends when it hits a blank line
            if worksheet['G%i' % i].value in routes_to_pull:
                route = str(worksheet['G%i' % i].value)
                day   = str(worksheet['D%i' % i].value)[8:10]
                month = str(worksheet['D%i' % i].value)[5:7]
                date  = '%s%s' % (month, day)
                logger.info('Found CCU:%s, ROUTE:%s, MMDD:%s' % (ccu, route, date))
                filename = '/home/automation/scripts/clayScripts/dev/telemetry_puller/telemetry_files/Telemetry_Route-%s_CCU-%s_Date-%s-%s-2015.csv' % (route, ccu, month, day)
                print(int(date))
                if int(date) >= 206 and int(date) <= 304:
                    print('pulling')
                    try:
                        query = 'SELECT * FROM t_ccu_15%s%s WHERE ccu_desig LIKE \'%s\' AND gps_lat>%s AND gps_long>%s AND gps_lat<%s AND gps_long<%s;' % (month, day, ccu, gps_square['lat1'], gps_square['long1'], gps_square['lat2'], gps_square['long2'])
                        connection = MySQLdb.connect(DB_IP, DB_USER, DB_PW, DB_NAME)
                        cursor = connection.cursor()
                        cursor.execute(query)
                        sql_response = cursor.fetchall()
                        column_list = []
                        for column_name in cursor.description:
                            column_list.append(str(column_name[0]))
                        try:
                            with open(filename, 'w') as outfile:
                                outfile.write(','.join(column_list) + '\n')
                                for row in sql_response:
                                    row_list = []
                                    for column in row:
                                        row_list.append(str(column))
                                    outfile.write(','.join(row_list) + '\n')
                        except:
                            logger.error('Unable to write Telemetry file! %s' % e)
                        else:
                            logger.info('Wrote file %s' % filename)
                    except:
                        logger.warning('Manually pull CCU:%s, ROUTE:%s, MMDD:%s' % (ccu, route, date))
                else:
                    logger.warning('Manually pull CCU:%s, ROUTE:%s, MMDD:%s' % (ccu, route, date))
            i = i + 1
    except IOError:
        pass

exit()
