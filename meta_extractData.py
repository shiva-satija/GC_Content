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

arguments = sys.argv
path = arguments[1]
project_link = 'http://metagenomics.anl.gov/metagenomics.cgi?page=MetagenomeOverview&metagenome='
metadata_link= 'http://metagenomics.anl.gov/metagenomics.cgi?page=DownloadMetagenome&action=download_md&filename=mgm'

fileList = []
dataList = []

for infile in glob.glob( os.path.join(path, '*.text') ): #file extension type 'text'
	fileList.append(infile)

for filesL in fileList:
	inputFile = open(filesL, 'r')
	fileReader = inputFile.readlines()

	for reads in fileReader:
		reads = reads.replace('\n', '')
		reads = reads.replace('\t', '')
		reads = reads.replace(' ', '')
		reads = reads + '.txt'
		dataList.append(reads) #The datasets in the file(s)

outputFile_meta = open('Project_Metadata.csv', 'w')
outputFile_meta.write('project_ID\tproject_name\tproject_environment\tproject_feature\tproject_material\tproject_sampleBiome\t' + \
	'project_organization\tproject_PI\tproject_PI_email\tPI_organization_url\tproject_NCBI\tproject_collectionDate\t' + \
	'project_collectionTimeZone\tlocation_coordinates\tproject_location\tproject_sampleCountry\t' + \
	'project_sampleContinent\tproject_depth\tproject_temperature\tproject_pH\tproject_salinity\t' + \
	'project_sequencingMethod\tproject_dataType\tproject_pubMedID\tproject_link\tproject_metatdataLink\tproject_description\n')

print dataList
for files in dataList:
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
	project_pubMedID = 'NA'
	project_environment = 'NA'

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
	project_material = 'NA'

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
				if file == '4440281.3':
					print project_NCBI
			if line.startswith('pubmed_id'):
				project_pubMedID = removeInput(line, 'pubmed_id')

				#Project ncbi_id 17635
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
			if line.startswith('material'):
				project_material = removeInput(line, 'material')
			if line.startswith('env_package'):
				project_environment = removeInput(line, 'env_package')

		if line.startswith('Enviromental'): 
			line = removeInput(line, 'Environmental')
			if line.startswith('Package'):
				line = removeInput(line, 'Package')
				if line.startswith('water'):
					if line.startswith('salinity') and project_salinity == 'NA': 
						line = removeInput(line, 'salinity')
						project_salinity = removeInput(line, 'salinity')
			if line.startswith('env_package'):
				project_environment = removeInput(line, 'env_package')

		if line.startswith('Library:'): 
			line = removeInput(line, 'Library:')
			if line.startswith('metagenome'):
				line = removeInput(line, 'metagenome')		
				if line.startswith('pubmed_id'):
					project_pubMedID = removeInput(line, 'pubmed_id')
				if line.startswith('seq_meth'):
					project_sequencingMethod = removeInput(line, 'seq_meth')
				if line.startswith('project_dataType'):
					project_dataType = line
			if line.startswith('mimarks-survey'):
				line = removeInput(line, 'mimarks-survey')
				if line.startswith('pubmed_id'):
					project_pubMedID = removeInput(line, 'pubmed_id')
				if line.startswith('seq_meth'):
					project_sequencingMethod = removeInput(line, 'seq_meth')
				if line.startswith('project_dataType'):
					project_dataType = line

	outputLink = str(project_link + files + '\t' + metadata_link + files + '.metadata.txt')
	outputFile_meta.write(files + '\t' + project_name + '\t' + project_environment + '\t' + project_feature + '\t' + project_material + '\t' + \
		project_sampleBiome + '\t' + project_organization + '\t' + project_PI_firstName + ' ' + project_PI_lastName + '\t' + project_PI_email + '\t' + \
		project_PI_organization_url + '\t' + project_NCBI + '\t' + project_collectionDate + '\t' + project_collectionTimeZone + '\t' + \
		project_latitude + ',' + project_longitude + '\t' + project_location + '\t' + project_sampleCountry + '\t' + project_sampleContinent + '\t' + \
		project_depth + '\t' + project_temperature  + '\t' + project_pH + '\t' + project_salinity + '\t' + project_sequencingMethod + '\t' + \
		project_dataType + '\t' + project_pubMedID + '\t' + outputLink + '\t' + project_description + '\n')

	inputF.close()

outputFile_meta.close()
inputFile.close()
