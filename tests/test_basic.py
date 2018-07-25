# -*- coding: utf-8 -*-

#from .context import sample
import os
import pathlib
import collections

from ExifUtils.core import (copy_file, convert_png_to_jpg, get_exiftool_commands,
run_exiftool, write_exif_gps_data, write_exif_comment, write_exif_date,
write_author, process_image, verify_file_exists, verify_dir_exists, get_exif_data, get_exif_data_json)

import unittest

class BasicTestSuite(unittest.TestCase):
	"""Basic test cases."""
	
	def setUp(self):
		self.base_path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
		self.jpg_dir = self.base_path.joinpath("TestImages").joinpath("JPGImages")
		
		self.png_one_loc = self.base_path.joinpath("TestImages/PNGImages/Dice.png")
		self.png_two_loc = self.base_path.joinpath("TestImages/PNGImages/Mario.png")
		
		self.jpg_one_loc = self.base_path.joinpath("TestImages/JPGImages/Mario.png")
		self.jpg_two_loc = self.base_path.joinpath("TestImages/JPGImages/Dice.png")
		
		copy_file(str(self.png_one_loc), str(self.jpg_dir))
		copy_file(str(self.png_two_loc), str(self.jpg_dir))
		
	def test_copy_file(self):		
		print('testing if ',str(self.jpg_one_loc), ' exists')
		self.assertTrue(verify_file_exists(str(self.jpg_one_loc)))
		self.assertTrue(verify_file_exists(str(self.jpg_two_loc)))

	def test_convert_png_to_jpg(self):
		convert_png_to_jpg(str(self.jpg_one_loc))
		convert_png_to_jpg(str(self.jpg_two_loc))
		
		self.assertTrue(verify_file_exists(str(self.base_path.joinpath("TestImages/JPGImages/Mario.jpg"))))
		self.assertTrue(verify_file_exists(str(self.base_path.joinpath("TestImages/JPGImages/Dice.jpg"))))
		
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
		write_exif_gps_data(str(self.base_path.joinpath("TestImages/JPGImages/Dice.jpg")), 15.12345, 1.12345, 50)
		self.assertTrue(get_exif_data_json(str(self.base_path.joinpath("TestImages/JPGImages/Dice.jpg")))['GPS Longitude'] == '1 deg 7\' 24.42" W')
		self.assertTrue(get_exif_data_json(str(self.base_path.joinpath("TestImages/JPGImages/Dice.jpg")))['GPS Latitude'] == '15 deg 7\' 24.42" N')
		
	def test_write_exif_date(self):
		pass
		
	def test_write_exif_comment(self):
		pass

	def test_write_exif_author(self):
		pass
		
	def test_process_image(self):
		pass
		
	def test_get_exif_data(self):
		#print(get_exif_data(str(self.base_path.joinpath("TestImages/JPGImages/Dice.jpg"))).decode())
		pass
		
	def test_get_exif_data_json(self):
		print(sorted(get_exif_data_json(str(self.base_path.joinpath("TestImages/JPGImages/Dice.jpg")))))
		self.assertEqual(sorted(get_exif_data_json(str(self.base_path.joinpath("TestImages/JPGImages/Dice.jpg")))),
		sorted({'Image Width': '800', 'Directory': 'C', 'File Access Date/Time': '2018', 'File Name': 'Dice.jpg', 'Bits Per Sample': '8', 'Y Resolution': '1', 'File Type Extension': 'jpg', 'File Type': 'JPEG', 'File Modification Date/Time': '2018', 'Megapixels': '0.480', 'File Creation Date/Time': '2018', 'Color Components': '3', 'File Permissions': 'rw-rw-rw-', 'Resolution Unit': 'None', 'X Resolution': '1', 'Encoding Process': 'Baseline DCT, Huffman coding', 'Image Height': '600', 'Image Size': '800x600', 'ExifTool Version Number': '10.88', 'File Size': '152 kB', 'MIME Type': 'image/jpeg', 'Y Cb Cr Sub Sampling': 'YCbCr4', 'JFIF Version': '1.01'}))
	
if __name__ == '__main__':
	unittest.main()