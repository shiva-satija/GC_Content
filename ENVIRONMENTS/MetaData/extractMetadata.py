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
project_PI_organization_url = ''
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
	'project_organization\t	project_PI\t	project_PI_email\t	PI_organization_url\t	project_NCBI\t	project_collectionDate\t' + \
	'project_collectionTimeZone\t	location_coordinates\t	project_location\t	project_sampleCountry\t' + \
	'project_sampleContinent\t	project_depth\t	project_temperature\t	project_pH\t	project_salinity\t' + \
	'project_sequencingMethod\t	project_dataType\t	project_pubMedID\t	project_link\t 	project_metatdataLink\n')

for files in fileList:
	inputF = open(files, 'r')
	lines = inputF.readlines()

	for line in lines:
		#####Project
		if line.startswith('Project'):
			line = removeInput(line, 'Project')
			if line.startswith('project_name'):
				project_name = removeInput(line, 'project_name') 
			if line.startswith('project_description'):
				project_description = removeInput(line, 'project_description')
			if line.startswith('project_sampleFeature'):
				project_sampleFeature = removeInput(line, 'project_sampleFeature')
			if line.startswith('project_sampleBiome'):
				project_sampleBiome = removeInput(line, 'project_sampleBiome')
			if line.startswith('project_organization') and line.startswith(project_organization_url[0]) == False and line.startswith('PI_organization_address') == False and line.startswith('PI_organization_country') == False:
				project_organization = removeInput(line, 'project_organization')
			if line.startswith('PI_firstname'):
				project_PI_firstName = removeInput(line, 'PI_firstname')
			if line.startswith('PI_lastname'):
				project_PI_lastName = removeInput(line, 'PI_lastname')
			if line.startswith('PI_email'):
				project_PI_email = removeInput(line, 'PI_email') 
			if line.startswith('PI_organization_url'):
				project_PI_organization_url = removeInput(line, 'PI_organization_url') 

		####Sample
		if line.startswith('Sample'):
			line = removeInput(line, 'Sample')
			if line.startswith('feature'):
				line = line.replace('feature', '')
				line = str(line.lstrip())
				line = str(line.rstrip())
				project_feature = line
			if line.startswith('collection_date'):
				project_collectionDate = removeInput(line, 'collection_date')
			if line.startswith('collection_timezone'):
				project_collectionTimeZone = removeInput(line, 'collection_timezone')
			if line.startswith('project_sampleSize'):
				project_sampleSize = removeInput(line, 'project_sampleSize')
			if line.startswith('latitude'):
				project_latitude = removeInput(line, 'latitude')
			if line.startswith('longitude'):
				project_longitude = removeInput(line, 'longitude') 
			if line.startswith('location'):
				project_location = removeInput(line, 'location')
			if line.startswith('continent'):
				project_sampleContinent = removeInput(line, 'continent')
			if line.startswith('depth'):
				project_depth = removeInput(line, 'depth')
			if line.startswith('temperature'):
				project_temperature = removeInput(line, 'temperature')
			if line.startswith('pH'):
				project_pH = removeInput(line, 'pH')
			if line.startswith('salinity') or line.startswith('misc_param'):
				line = removeInput(line, 'misc_param')
				line = removeInput(line, 'salinity')
				project_salinity = line

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
		project_organization + '\t' +  project_PI_firstName + ' ' + project_PI_lastName + '\t' + project_PI_email + '\t' + project_PI_organization_url + '\t' + project_NCBI + '\t' + \
		project_collectionDate + '\t' + project_collectionTimeZone + '\t' + project_latitude + ',' + project_longitude + '\t' + \
		project_location + '\t' + project_sampleCountry + '\t' + project_sampleContinent + '\t' + \
		project_depth + '\t' + project_temperature  + '\t' + project_pH + '\t' + project_salinity + '\t' + project_sequencingMethod + '\t' + \
		project_dataType + '\t' + project_pubMedID + '\t' + outputLink)

	inputF.close()

outputFile.close()
inputFile.close()
