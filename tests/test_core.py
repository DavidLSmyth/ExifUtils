# -*- coding: utf-8 -*-

#from .context import sample
import os
import pathlib
import collections
import datetime
import time

from ExifUtils.core import (get_exiftool_commands,
run_exiftool, write_exif_gps_data, write_exif_comment, write_exif_date_original, write_exif_date_modified,
write_author, process_image, verify_file_exists, verify_dir_exists, get_exif_data, get_exif_data_json)

from ExifUtils.helpers import copy_file, convert_png_to_jpg, verify_file_exists, verify_dir_exists

import unittest

class CoreTestSuite(unittest.TestCase):
	"""Basic test cases."""
	
	def setUp(self):
		self.base_path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
		self.jpg_dir = self.base_path.joinpath("TestImages").joinpath("JPGImages")
		
		try:
			os.remove(str(self.base_path.joinpath("TestImages/JPGImages/Mario.jpg")))
		except Exception as e: 
			print(e)

		try:
			os.remove(str(self.base_path.joinpath("TestImages/JPGImages/Dice.jpg")))
		except Exception as e: 
			print(e)

		self.png_dice_loc = self.base_path.joinpath("TestImages/PNGImages/Dice.png")
		self.png_mario_loc = self.base_path.joinpath("TestImages/PNGImages/Mario.png")
		
		self.copied_png_dice_loc = self.base_path.joinpath("TestImages/JPGImages/Dice.png")
		self.copied_png_mario_loc = self.base_path.joinpath("TestImages/JPGImages/Mario.png")
		
		self.jpg_dice_loc = self.base_path.joinpath("TestImages/JPGImages/Dice.jpg")
		self.jpg_mario_loc = self.base_path.joinpath("TestImages/JPGImages/Mario.jpg")
		
		if not verify_file_exists(str(self.base_path.joinpath("TestImages/JPGImages/Mario.jpg"))):
			copy_file(str(self.png_dice_loc), str(self.jpg_dir))
			convert_png_to_jpg(str(self.copied_png_dice_loc))
			
		if not verify_file_exists(str(self.base_path.joinpath("TestImages/JPGImages/Mario.jpg"))):
			copy_file(str(self.png_mario_loc), str(self.jpg_dir))
			convert_png_to_jpg(str(self.copied_png_mario_loc))
			
	def test_get_exiftool_commands(self):
		d1 = {'GPSLongitude': 53.12526, 'GPSLatitude': 9.32432, 
		'GPSAltitude':'"{}"'.format(50), 'GPSVersionID':'3 2 0 0','gpsaltituderef':'0',
		"n": None, "GPSLatitudeRef": 'N', "GPSLongitudeRef": "W"}
		
		d2 = {"Comment": "this is a test"}
		#check that all tags are present in both strings
		self.assertEqual(set(' '.join(get_exiftool_commands(d1, str(self.base_path.joinpath("TestImages/test.png")))).split(' ')),
		set('''-GPSLongitude=53.12526 -GPSLatitude=9.32432 -GPSAltitude="50" -GPSVersionID=3 2 0 0 -gpsaltituderef=0 -n -GPSLatitudeRef=N -GPSLongitudeRef=W {}'''.format(str(self.base_path.joinpath("TestImages/test.png"))).split(' ')))
		
		self.assertEqual(set(' '.join(get_exiftool_commands(d2, str(self.base_path.joinpath("TestImages/test.png")))).split(' ')),
		set('''-Comment=this is a test {}'''.format(str(self.base_path.joinpath("TestImages/test.png"))).split(' ')))
		
	def test_run_exiftool(self):
		pass
		
	def test_write_exif_gps_data(self):
		write_exif_gps_data(str(self.jpg_dice_loc), 15.12345, 1.12345, 50)
		self.assertTrue(get_exif_data_json(str(self.jpg_dice_loc))['GPS Longitude'] == '1 deg 7\' 24.42" W')
		self.assertTrue(get_exif_data_json(str(self.jpg_dice_loc))['GPS Latitude'] == '15 deg 7\' 24.42" N')
		
	def test_write_exif_date(self):
		#print('Writing new date: ', str(datetime.datetime.now() - datetime.timedelta(days=7)))
		write_exif_date_original(str(self.jpg_dice_loc), str(datetime.datetime.now() - datetime.timedelta(days=7)))
		write_exif_date_modified(str(self.jpg_dice_loc), str(datetime.datetime.now() - datetime.timedelta(days=7)))
		#print(get_exif_data_json(str(self.jpg_dice_loc)))
		self.assertEqual(get_exif_data_json(str(self.jpg_dice_loc))['File Modification Date/Time'], str(datetime.datetime.now() - datetime.timedelta(days=7)))
		self.assertEqual(get_exif_data_json(str(self.jpg_dice_loc))['File Creation Date/Time'], str(datetime.datetime.now() - datetime.timedelta(days=7)))
		
	def test_write_exif_comment(self):
		write_exif_comment(str(self.jpg_mario_loc), comment = "This is a test comment")
		self.assertEqual(get_exif_data_json(str(self.jpg_mario_loc))['Comment'], "This is a test comment")

	def test_write_exif_author(self):
		write_author(str(self.jpg_mario_loc), "Test author")
		self.assertEqual(get_exif_data_json(str(self.jpg_mario_loc))['Author'], "Test author")
		
	def test_process_image(self):
		process_image(str(self.png_dice_loc), str(self.jpg_dir), comment = "test comment", tags= "list of strings", date=str(datetime.datetime.now()), 
		gps_lat = 20.324234, gps_long = -2.45, gps_alt = 200)
		print(get_exif_data_json(str(self.jpg_mario_loc)))
		
	def test_get_exif_data(self):
		#print(get_exif_data(str(self.base_path.joinpath("TestImages/JPGImages/Dice.jpg"))).decode())
		pass
		
	def test_get_exif_data_json(self):
		#print(sorted(get_exif_data_json(str(self.jpg_dice_loc))))
		self.assertEqual(sorted(get_exif_data_json(str(self.jpg_dice_loc))),
		sorted({'Image Width': '800', 'Directory': 'C', 'File Access Date/Time': '2018', 'File Name': 'Dice.jpg', 'Bits Per Sample': '8', 'Y Resolution': '1', 'File Type Extension': 'jpg', 'File Type': 'JPEG', 'File Modification Date/Time': '2018', 'Megapixels': '0.480', 'File Creation Date/Time': '2018', 'Color Components': '3', 'File Permissions': 'rw-rw-rw-', 'Resolution Unit': 'None', 'X Resolution': '1', 'Encoding Process': 'Baseline DCT, Huffman coding', 'Image Height': '600', 'Image Size': '800x600', 'ExifTool Version Number': '10.88', 'File Size': '152 kB', 'MIME Type': 'image/jpeg', 'Y Cb Cr Sub Sampling': 'YCbCr4', 'JFIF Version': '1.01'}))
	
if __name__ == '__main__':
	unittest.main()