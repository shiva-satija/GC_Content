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

project_link = 'http://metagenomics.anl.gov/metagenomics.cgi?page=MetagenomeOverview&metagenome='
metadata_link= 'http://metagenomics.anl.gov/metagenomics.cgi?page=DownloadMetagenome&action=download_md&filename=mgm'

outputFile = open('Project_Metadata.csv', 'w')
inputFile = open('datasetNames.txt', 'r')

lines = inputFile.readlines()

fileList = []
for line in lines:
	line = line.replace('\n', '')
	line = line.replace(' ', '')
	line = line + '.txt'
	fileList.append(line)

outputFile.write('project_ID\tproject_name\tproject_feature\tproject_sampleBiome\t' + \
	'project_organization\tproject_PI\tproject_PI_email\tPI_organization_url\tproject_NCBI\tproject_collectionDate\t' + \
	'project_collectionTimeZone\tlocation_coordinates\tproject_location\tproject_sampleCountry\t' + \
	'project_sampleContinent\tproject_depth\tproject_temperature\tproject_pH\tproject_salinity\t' + \
	'project_sequencingMethod\tproject_dataType\tproject_pubMedID\tproject_link\tproject_metatdataLink\tproject_description\n')

for files in fileList:
	#####Project
	project_name = 'NA'
	project_description = 'NA'
	project_sampleFeature = 'NA'
	project_sampleBiome= 'NA'
	project_organization = 'NA'
	project_organization_url = 'NA'
	project_PI_firstName = 'NA'
	project_PI_lastName = 'NA'
	project_PI_email = 'NA'
	project_PI_organization_url = 'NA'
	project_NCBI = 'NA'

	####Sample
	project_collectionDate = 'NA'
	project_collectionTimeZone = 'NA'
	project_sampleSize = 'NA'
	project_latitude = 'NA'
	project_longitude = 'NA'
	project_location = 'NA'
	project_sampleCountry = 'NA'
	project_sampleContinent = 'NA'
	project_depth = 'NA'
	project_temperature = 'NA'
	project_pH = 'NA'
	project_salinity = 'NA'

	###Library: mimarks-survey seq_meth, Library: metagenome
	project_sequencingMethod = 'NA'
	project_dataType = 'NA'

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
			if line.startswith('PI_organization') and line.startswith('PI_organization_url') == False and line.startswith('PI_organization_address') == False and line.startswith('PI_organization_country') == False:
				project_organization = removeInput(line, 'PI_organization')
			if line.startswith('PI_firstname'):
				project_PI_firstName = removeInput(line, 'PI_firstname')
			if line.startswith('PI_lastname'):
				project_PI_lastName = removeInput(line, 'PI_lastname')
			if line.startswith('PI_email'):
				project_PI_email = removeInput(line, 'PI_email') 
			if line.startswith('PI_organization_url'):
				project_PI_organization_url = removeInput(line, 'PI_organization_url') 
			if line.startswith('ncbi_id'):
				project_NCBI = removeInput(line, 'ncbi_id') 

		####Sample
		if line.startswith('Sample'):
			line = removeInput(line, 'Sample')
			if line.startswith('feature'):
				project_feature = removeInput(line, 'feature')
			if line.startswith('biome'):
				project_sampleBiome = removeInput(line, 'biome')
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
			if line.startswith('country'):
				project_sampleCountry = removeInput(line, 'country')
			if line.startswith('continent'):
				project_sampleContinent = removeInput(line, 'continent')
			if line.startswith('depth'):
				project_depth = removeInput(line, 'depth')
			if line.startswith('temperature'):
				project_temperature = removeInput(line, 'temperature')
			if line.startswith('pH'):
				project_pH = removeInput(line, 'pH')
			if line.startswith('salinity') or line.startswith('misc_param') and project_salinity == 'NA':
				line = removeInput(line, 'misc_param')
				line = removeInput(line, 'salinity')
				project_salinity = line

		if line.startswith('Enviromental Package:'): 
			line = removeInput(line, 'Environmental')
			if line.startswith('water'):
				if line.startswith('salinity') and project_salinity == 'NA': 
					line = removeInput(line, 'salinity')
					project_salinity = removeInput(line, 'salinity')

		###Library: mimarks-survey seq_meth, Library: metagenome
		if line.startswith('Library: metagenome') or line.startswith('Library: mimarks-survey'):
			line = removeInput(line, 'Library: metagnome')
			line = removeInput(line, 'Library: mimarks-survey')
			if line.startswith('pubmed_id'):
				project_pubMedID = removeInput(line, 'pubmed_id')
			if line.startswith('project_sequencingMethod'):
				project_sequencingMethod = line
			if line.startswith('project_dataType'):
				project_dataType = line

	outputLink = str(project_link + files + '\t' + metadata_link + files + '.metadata.txt')
	outputFile.write(files + '\t' + project_name + '\t' + project_feature + '\t' + project_sampleBiome + '\t' + project_organization + '\t' +  \
		project_PI_firstName + ' ' + project_PI_lastName + '\t' + project_PI_email + '\t' + project_PI_organization_url + '\t' + project_NCBI + '\t' + \
		project_collectionDate + '\t' + project_collectionTimeZone + '\t' + project_latitude + ',' + project_longitude + '\t' + \
		project_location + '\t' + project_sampleCountry + '\t' + project_sampleContinent + '\t' + \
		project_depth + '\t' + project_temperature  + '\t' + project_pH + '\t' + project_salinity + '\t' + project_sequencingMethod + '\t' + \
		project_dataType + '\t' + project_pubMedID + '\t' + outputLink + '\t' + project_description + '\n')

	inputF.close()

outputFile.close()
inputFile.close()
