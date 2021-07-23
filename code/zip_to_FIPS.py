#!/usr/bin/env python
# encoding: utf-8
"""
zip_to_FIPS.py

restrict data from from zip_city_map.txt to US zipcodes 
where lat/lon is not null, then tie state to state abbrev 
from states.csv, then map that & county to five digit FIPS code from national.txt

zip_city_map.txt
  zip lat long city county state country
  E4Y1R3  (null)  (null)  Adams   Illinois        East Midwest    us
  E4Y1R4  (null)  (null)  Adams   Illinois        East Midwest    us
  E4Y1R5  (null)  (null)  Adams   Illinois        East Midwest    us
  62083   39.3798 -89.1604        Rosamond        Christian       Illinois        us
  62567   39.64   -89.1929        Stonington      Christian       Illinois        us
  62568   39.5489 -89.2945        Taylorville     Christian       Illinois        us

national.txt
  State,State ANSI,County ANSI,County Name,ANSI Cl
  AL,01,001,Autauga County,H1
  AL,01,003,Baldwin County,H1
  AL,01,005,Barbour County,H1
  AL,01,007,Bibb County,H1
  AL,01,009,Blount County,H1
  AL,01,011,Bullock County,H1

states.csv
  "State","Abbreviation"
  "Alabama","AL"
  "Alaska","AK"
  "Arizona","AZ"
  "Arkansas","AR"
  "California","CA"

Created by Peter Skomoroch on 2010-02-26.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import csv

# Geoname counties missing from national file = 

geoname_equivalent = {
'aleutians east borough\talaska':'aleutians east\talaska',
'bristol bay borough\talaska':'bristol bay\talaska',
'bristol city\tvirginia':'bristol\tvirginia',
'dekalb county\talabama':'de kalb\talabama',
'dekalb county\tindiana':'de kalb\tindiana',
'desoto county\tflorida':'de soto\tflorida',
'dewitt county\ttexas':'de witt\ttexas',
'denali borough\talaska':'denali\talaska',
'de witt county\tillinois':'dewitt\tillinois',
'fairbanks north star borough\talaska':'fairbanks north star\talaska',
'haines borough\talaska':'haines\talaska',
'juneau city and borough\talaska':'juneau\talaska',
'kenai peninsula borough\talaska':'kenai peninsula\talaska',
'ketchikan gateway borough\talaska':'ketchikan gateway\talaska',
'kodiak island borough\talaska':'kodiak island\talaska',
'laporte county\tindiana':'la porte\tindiana',
'lasalle county\tillinois':'la salle\tillinois',
'lake and peninsula borough\talaska':'lake and peninsula\talaska',
'matanuska-susitna borough\talaska':'matanuska susitna\talaska',
'north slope borough\talaska':'north slope\talaska',
'northwest arctic borough\talaska':'northwest arctic\talaska',
'prince of wales-hyder census area\talaska':'prince wales ketchikan\talaska',
'radford city\tvirginia':'radford\tvirginia',
'ste. genevieve county\tmissouri':'sainte genevieve\tmissouri',
'salem city\tvirginia':'salem\tvirginia',
'sitka city and borough\talaska':'sitka\talaska',
'skagway municipality\talaska':'skagway hoonah angoon\talaska',
'saint john the baptist parish\tlouisiana':'st john the baptist\tlouisiana',
'saint joseph county\tindiana':'st joseph\tindiana',
'valdez-cordova census area\talaska':'valdez cordova\talaska',
'wrangell city and borough\talaska':'wrangell petersburg\talaska',
'yakutat city and borough\talaska':'yakutat\talaska',
'yukon-koyukuk census area\talaska':'yukon koyukuk\talaska'}


def clean_name(name):
  name = name.replace("'","").replace('St.','Saint')
  return name.lower()


def main():
  # Read in state abbrev
  state_name = {}
  reader = csv.reader(open('../data/states.csv'), delimiter=",")
  reader.next()
  for row in reader:
    state_name[row[1]] = row[0].lower()
  
  # read in FIPS codes
  FIPS = {}
  reader = csv.reader(open('../data/national.txt'), delimiter=",")
  reader.next()
  for row in reader:
    # AL,01,001,Autauga County,H1
    try:
      full_state_name = state_name[row[0]]
      fips_key = clean_name(row[3]) + '\t' + full_state_name
      if geoname_equivalent.has_key(fips_key):
        fips_key = geoname_equivalent[fips_key]       
      # for a subset of counties, we will replace the standard census
      # names with counties from geonames
      FIPS[fips_key] = row[1] + row[2]
    except:
      pass
  
  # read in zip_city_map
  reader = csv.reader(open('../data/zip_city_map.txt'), delimiter="\t")
  reader.next()

  missing = open('missing_zips.txt', 'w')
  missing_counties = open('missing_counties.txt', 'w')
  fips_county_map = open('fips_county_mapping.txt', 'w')
  # zip lat long city county state country
  for row in reader:
    if row[6]=='us' and row[1] != '(null)':
      (zipcode, latitude, longitude, city, county, state) = row[0], row[1], row[2], row[3], row[4], row[5]
      # if row[5] == 'Alabama':
      #   print FIPS[county+ ' County'+'\t'+state], row
      try:
        try:
          if county == 'District of Columbia':
            print(county +'\t'+state)
          fips_code = FIPS[county.lower() +'\t'+state.lower()]

        except:
          try:  
            fips_code = FIPS[county.lower() + ' county'+'\t'+state.lower()]
          except:
            try:
              fips_code = FIPS[county.lower() + ' parish'+'\t'+state.lower()]
            except:
              try:
                fips_code = FIPS[county.lower() + ' municipality'+'\t'+state.lower()]
              except:
                fips_code = FIPS[county.lower() + ' census area'+'\t'+state.lower()]  
        # print zipcode, city, county, state, fips_code
        fips_county_map.write('\t'.join([zipcode, latitude, longitude, city, county, state, fips_code])+'\n')
      except:
        print >> missing, row
        print >> missing_counties, '%s\t%s' % (county, state)      


if __name__ == '__main__':
  main()
