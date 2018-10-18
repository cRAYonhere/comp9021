# Uses data available at http://data.worldbank.org/indicator
# on Forest area (sq. km) and Agricultural land area (sq. km).
# Prompts the user for two distinct years between 1990 and 2004
# as well as for a strictly positive integer N,
# and outputs the top N countries where:
# - agricultural land area has increased from oldest input year to most recent input year;
# - forest area has increased from oldest input year to most recent input year;
# - the ratio of increase in agricultural land area to increase in forest area determines
#   output order.
# Countries are output from those whose ratio is largest to those whose ratio is smallest.
# In the unlikely case where many countries share the same ratio, countries are output in
# lexicographic order.
# In case fewer than N countries are found, only that number of countries is output.


# Written by *** and Eric Martin for COMP9021


import sys
import os
import csv
from collections import defaultdict


agricultural_land_filename = 'API_AG.LND.AGRI.K2_DS2_en_csv_v2.csv'
if not os.path.exists(agricultural_land_filename):
    print(f'No file named {agricultural_land_filename} in working directory, giving up...')
    sys.exit()
forest_filename = 'API_AG.LND.FRST.K2_DS2_en_csv_v2.csv'
if not os.path.exists(forest_filename):
    print(f'No file named {forest_filename} in working directory, giving up...')
    sys.exit()
try:
    years = {int(year) for year in
                           input('Input two distinct years in the range 1990 -- 2014: ').split('--')
            }
    if len(years) != 2 or any(year < 1990 or year > 2014 for year in years):
        raise ValueError
except ValueError:
    print('Not a valid range of years, giving up...')
    sys.exit()
try:
    top_n = int(input('Input a strictly positive integer: '))
    if top_n < 0:
        raise ValueError
except ValueError:
    print('Not a valid number, giving up...')
    sys.exit()


countries = []
year_1, year_2 = None, None

'''Amruts Code Begins'''
dictionary_agri=defaultdict(list)
info_list=[]
agri_list = []
frst_list = []
store_agri_csv_counter=store_frst_csv_counter=0

with open('API_AG.LND.AGRI.K2_DS2_en_csv_v2.csv', 'rt',encoding = 'utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        if row:
            if store_agri_csv_counter == 2:
                for i in range(len(row)):
                    try:
                        dictionary_agri[int(row[i])]=i
                    except ValueError:
                        dictionary_agri[row[i]]=i
            if store_agri_csv_counter > 2:
                agri_list.append(list(row))
            store_agri_csv_counter+=1
with open('API_AG.LND.FRST.K2_DS2_en_csv_v2.csv', 'rt',encoding = 'utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        if row:
            if store_frst_csv_counter > 2:
                frst_list.append(list(row))
            store_frst_csv_counter+=1
        
start_year=years.pop()
end_year=years.pop()
if start_year > end_year:
    temp=end_year
    end_year=start_year
    start_year=temp

for i in range(len(agri_list)):
    if agri_list[i][dictionary_agri[start_year]] and agri_list[i][dictionary_agri[end_year]] and frst_list[i][dictionary_agri[start_year]] and frst_list[i][dictionary_agri[end_year]]:       
        agri=float(agri_list[i][dictionary_agri[end_year]])-float(agri_list[i][dictionary_agri[start_year]])
        frst=float(frst_list[i][dictionary_agri[end_year]])-float(frst_list[i][dictionary_agri[start_year]])
        if agri >= 0 and frst > 0:
            info_list.append(( agri_list[i][0],round((agri/frst),2)))
    else:
        continue

info_list.sort(key=lambda k: (-k[1],k[0]), reverse=False)

counter=0
for i in info_list:
    if counter < top_n:
        countries.append(str(i[0])+" "+ str(f'({i[1]:.2f})'))
    else:
        break
    counter+=1
year_1, year_2 = start_year, end_year

'''Amruts Code Ends'''

print(f'Here are the top {top_n} countries or categories where, between {year_1} and {year_2},\n'
      '  agricultural land and forest land areas have both strictly increased,\n'
      '  listed from the countries where the ratio of agricultural land area increase\n'
      '  to forest area increase is largest, to those where that ratio is smallest:')
print('\n'.join(country for country in countries))
    
