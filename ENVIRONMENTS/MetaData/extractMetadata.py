'''
Author:	E. Reichenerger
Date:	6.19.2013

Purpose: Given a dataset name (from MG-Rast) from a text file, extract the metatdata from the metatdata files 

e.g. 4440281.3, http://metagenomics.anl.gov/metagenomics.cgi?page=MetagenomeOverview&metagenome=4440281.3
'''

import sys
import os 
import glob 
import sys
import re #regular expressions
  
def removeInput(fileLine, searchWord): #strip word (searchWord) from file (fileLine) & return the new line
	fileLine = fileLine.replace(searchWord, '')
	fileLine = str(fileLine.lstrip())
	fileLine = str(fileLine.rstrip())
	fileLine = fileLine.replace('\n', '')
	return fileLine

#####Project
project_name = ''
project_description = ''
project_sampleFeature = ''
project_sampleBiome= ''
project_organization = ''
project_organization_url = ''
project_PI_firstName = ''
project_PI_lastName = ''
project_PI_email = ''
project_NCBI = ''

####Sample
project_collectionDate = ''
project_collectionTimeZone = ''
project_sampleSize = ''
project_latitude = ''
project_longitude = ''
project_location = ''
project_sampleCountry = ''
project_sampleContinent = ''
project_depth = ''
project_temperature = ''
project_pH = ''
project_salinity = ''

###Library: mimarks-survey seq_meth, Library: metagenome
project_sequencingMethod = ''
#project_sequencingMethod = ''mimarks-survey seq_meth','seq_meth', '']
project_dataType = ''
#project_dataType = ''lib_type', '']
project_link = 'http://metagenomics.anl.gov/metagenomics.cgi?page=MetagenomeOverview&metagenome='
metadata_link= 'http://metagenomics.anl.gov/metagenomics.cgi?page=DownloadMetagenome&action=download_md&filename=mgm'

outputFile = open('Project_Metadata.txt', 'w')
inputFile = open('datasetNames.txt', 'r')

lines = inputFile.readlines()

fileList = []
for line in lines:
	line = line.replace('\n', '')
	line = line.replace(' ', '')
	line = line + '.txt'
	fileList.append(line)

outputFile.write('project_ID\t	project_name\t	project_description\t	project_sampleFeature\t	project_sampleBiome\t' + \
	'project_organization\t	project_PI\t	project_PI_email\t	project_NCBI\t	project_collectionDate\t' + \
	'project_collectionTimeZone\t	location_coordinates\t	project_location\t	project_sampleCountry\t' + \
	'project_sampleContinent\t	project_depth\t	project_temperature\t	project_pH\t	project_salinity\t' + \
	'project_sequencingMethod\t	project_dataType\t	project_pubMedID\t	project_link\t 	project_metatdataLink\n')

for files in fileList:
	inputF = open(files, 'r')
	lines = inputF.readlines()

def removeInput(fileLine, searchWord): #strip word (searchWord) from file (fileLine) & return the new line
	for line in lines:
		#####Project
		if line.startswith('Project'):
			line = removeInput(line, 'Project')
			if line.startswith('project_name'):
				projec
				line = line.replace('project_name', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_name = line
			if line.startswith('project_description'):
				line = line.replace('project_description', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_description = line
			if line.startswith('project_sampleFeature'):
				line = line.replace('project_sampleFeature', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_sampleFeature = line
			if line.startswith('project_sampleBiome'):
				line = line.replace('project_sampleBiome', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_sampleBiome = line
			if line.startswith('project_organization') and line.startswith(project_organization_url[0]) == False and line.startswith('PI_organization_address') == False and line.startswith('PI_organization_country') == False:
				line = line.replace('project_organization', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_organization = line
			if line.startswith('project_PI_firstName'):
				line = line.replace('project_PI_firstName', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_PI_firstName = line
			if line.startswith('project_PI_lastName'):
				line = line.replace('project_PI_lastName', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_PI_lastName = line
			if line.startswith('project_PI_email'):
				line = line.replace('project_PI_email', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_PI_email = line

		####Sample
		if line.startswith('Sample'):
			line = str(line.replace('Sample', ''))
			line = str(line.lstrip())
			line = str(line.rstrip())
			line = line.replace('\n', '')
			if line.startswith('feature'):
				line = line.replace('feature', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_feature = line
			if line.startswith('collection_date'):
				line = line.replace('collection_date', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_collectionDate = line
			if line.startswith('collection_timezone'):
				line = line.replace('collection_timezone', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_collectionTimeZone = line
			if line.startswith('project_sampleSize'):
				line = line.replace('projecct_sampleSize', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_sampleSize = line
			if line.startswith('latitude'):
				line = line.replace('latitude', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_latitude = line
			if line.startswith('longitude'):
				line = line.replace('longitude', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_longitude = line
			if line.startswith('location'):
				line = line.replace('location', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_location = line
			if line.startswith('continent'):
				line = line.replace('continent', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_sampleContinent = line
			if line.startswith('depth'):
				line = line.replace('depth', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_depth = line
			if line.startswith('temperature'):
				line = line.replace('temperature', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_temperature = line
			if line.startswith('pH'):
				line = line.replace('pH', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_pH = line
			if line.startswith('salinity') or line.startswith('misc_param'):
				line = line.replace('misc_param', '')
				line = str(line.lstrip())
				line = line.replace('salinity', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_salinity = line
			Enviromental Package: water       salinity        27-30%
			Sample    salinity        9
			Sample    misc_param      salinity: 6-8 ; Percent

		if line.startswith('Enviromental Package:') or line.startswith('Sample'):
			line = line.replace('Environmental', '')
			line = line.replace('Sample', '')
			line = str(line.lstrip())
			if line.startswith('salinity') or line.startswith('misc_param'):
				line = line.replace('misc_param', '')
				line = str(line.lstrip())
				line = line.replace('salinity', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_salinity = line

		###Library: mimarks-survey seq_meth, Library: metagenome
		if line.startswith('Library: metagenome') or line.startswith('Library: mimarks-survey'):
			line = str(line.replace('Library: metagnome', ''))
			line = str(line.replace('Library: mimarks-survey', ''))
			line = str(line.lstrip())
			line = str(line.rstrip())
			line = line.replace('\n', '')
			if line.startswith('pubmed_id'):
				line = line.replace('pubmed_id', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_pubMedID = line
			if line.startswith('project_sequencingMethod'):
				project_sequencingMethod = line
			if line.startswith('project_dataType'):
				project_dataType = line

	outputLink = str(project_link + files + '\t' + metadata_link + files + '.metadata.txt\n')
	outputFile.write(files + '\t' + project_name + '\t' + project_description + '\t' + project_sampleFeature + '\t' + project_sampleBiome + '\t' + \
		project_organization + '\t' +  project_PI_firstName + ' ' + project_PI_lastName + '\t' + project_PI_email + '\t' + project_NCBI + '\t' + \
		project_collectionDate + '\t' + project_collectionTimeZone + '\t' + project_latitude + ',' + project_longitude + '\t' + \
		project_location + '\t' + project_sampleCountry + '\t' + project_sampleContinent + '\t' + \
		project_depth + '\t' + project_temperature  + '\t' + project_pH + '\t' + project_salinity + '\t' + project_sequencingMethod + '\t' + \
		project_dataType + '\t' + project_pubMedID + '\t' + outputLink)

	inputF.close()

outputFile.close()
inputFile.close()
