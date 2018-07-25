# -*- coding: utf-8 -*-
from . import helpers
#dependencies: 
#exiftool https://www.sno.phy.queensu.ca/~phil/exiftool/
#

import subprocess
import os
import sys
import configparser
import os
import datetime
import re
import shutil
import pathlib

#3rd party
from PIL import Image

########################## move these to helpers ##########################
def verify_file_exists(file_loc: str) -> bool:
	return os.path.isfile(file_loc)

def verify_dir_exists(dir_loc: str) -> bool:
	return os.path.isdir(dir_loc)
	
def copy_file(from_file_location: str, to_file_dir: str):
	'''Copies a png file from one folder to another'''
	#only tested for png files!
	if not verify_file_exists(from_file_location):
		raise Exception("File: {} does not exist".format(from_file_location))
	if not verify_dir_exists(to_file_dir):
		raise Exception("File: {} does not exist".format(to_file_dir))
	
	if from_file_location[-4:] != '.png':
		raise Exception("Source file extension must be .png, not {}".format(to_file_location[-3:]))
	
	file_name = os.path.basename(from_file_location)
	shutil.copy2(from_file_location, to_file_dir)

def convert_png_to_jpg(file_location: str, delete_png = True):
	'''Converts a png file to a jpg file and removes the old png file'''
	if not verify_file_exists(file_location):
		raise Exception("File: {} does not exist".format(file_location))
	if file_location[-4:] != '.png':
		raise Exception("Source file extension must be .png, not {}".format(file_location[-3:]))
	#Image.open(file_location).convert('RGB').save(file_location[:-3] + 'jpg')
	Image.open(file_location).convert('RGB').save(file_location[:-3] + 'jpg',"JPEG", quality = 100)
	os.remove(file_location)
########################## move these to helpers ##########################

def get_exiftool_commands(tags_values: dict, image_loc:str):
	if tags_values:
		commands_list = ['-' + key + '=' + str(value) if value else '-' + key for key, value in tags_values.items()]
	else:
		commands_list = []
	commands_list.append(image_loc)
	return commands_list

def run_exiftool(tags_values: dict, image_loc: str):
	'''Runs exiftool with the given tags=value pairs in the tags_value dict'''
	commands_list = get_exiftool_commands(tags_values, image_loc)
	exiftool_location = str(pathlib.Path(os.path.dirname(os.path.abspath(__file__))).joinpath("../bin/exiftool-10.88/exiftool"))
	try:	
		return subprocess.check_output([exiftool_location] + commands_list)
	except Exception as e:
		raise type(e)('Could not run exiftool with commands: {}'.format(commands_list) + str(e)).with_traceback(sys.exc_info()[2])
		
	
def write_exif_gps_data(image_loc: str, gps_lat: float, gps_long: float, gps_alt: float = 32):
	'''Writes exif data to a specified jpg image'''
	return run_exiftool({'GPSLongitude': gps_long, 'GPSLatitude': gps_lat, 
	'GPSAltitude':'"{}"'.format(gps_alt), 'GPSVersionID':'3 2 0 0','gpsaltituderef':'0',
	"-n": None, "GPSLatitudeRef": 'N', "GPSLongitudeRef": "W"}, image_loc)
	
	#subprocess.check_output(["exiftool", '-GPSLongitude={}'.format(gps_long),  '-GPSLatitude={}'.format(gps_lat), '-GPSAltitude="{}"'.format(gps_alt), #'-GPSVersionID=3 2 0 0','-gpsaltituderef=0', "-n", "-GPSLatitudeRef=N", "-GPSLongitudeRef=W",  image_loc])
	
def write_exif_comment(image_loc: str, comment = ""):
	return run_exiftool({'Comment': comment}, image_loc)
	#subprocess.check_output(["exiftool", 'Comment={}'.format(comment), image_loc])
	
def write_exif_date(date: str, image_loc: str):
	'''Writes the date that the image was take at. date should be in the form %Y:%m:%d %H:%M:%S'''
	return run_exiftool({'datetimeoriginal': date}, image_loc)
	#subprocess.check_output(["exiftool", '"-datetimeoriginal={}"'.format(date), image_loc])
	
def write_author(author: str, image_loc):
	'''Writes the date that the image was take at. date should be in the form %Y:%m:%d %H:%M:%S'''
	return run_exiftool({'author': author}, image_loc)
	#subprocess.check_output(["exiftool", '"-datetimeoriginal={}"'.format(date), image_loc])

def process_image(from_loc: str, to_loc: str, comment: str, tags: "list of strings", date: str, 
	gps_lat: float, gps_long: float, gps_alt: float = 32):
	'''Given a raw png image and metadata about that image, copies it to a specified location 
	in jpg format and writes metadata to exif'''
	copy_file(from_loc, to_loc)
	convert_png_to_jpg(to_loc)
	write_exif_gps_data(to_loc, gps_lat, gps_long, gps_alt)
	write_exif_comment(comment)
	write_exif_date(str(date))
	
def get_exif_data(image_loc: str) -> bytes:
	return run_exiftool({}, image_loc)
	
def get_exif_data_json(image_loc: str):
	return {item.split(':')[0].strip():item.split(':')[1].strip() for item in filter(lambda item: item, run_exiftool({}, image_loc).decode().split('\n'))}
	
	