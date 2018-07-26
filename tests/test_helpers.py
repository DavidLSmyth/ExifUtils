#stdlib
import unittest
import pathlib
import os

#user defined
from ExifUtils.helpers import copy_file, convert_png_to_jpg, verify_file_exists, verify_dir_exists

class HelpersTestSuite(unittest.TestCase):
	"""Basic test cases."""
	
	def test_copy_file(self):

		self.base_path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
		self.jpg_dir = self.base_path.joinpath("TestImages").joinpath("JPGImages")
		try:
			os.remove(str(self.base_path.joinpath("TestImages/JPGImages/Mario.png")))
		except Exception as e: 
			print(e)

		try:
			os.remove(str(self.base_path.joinpath("TestImages/JPGImages/Dice.png")))
		except Exception as e: 
			print(e)
			
		self.png_one_loc = self.base_path.joinpath("TestImages/PNGImages/Dice.png")
		self.png_two_loc = self.base_path.joinpath("TestImages/PNGImages/Mario.png")
		
		self.copied_png_one_loc = self.base_path.joinpath("TestImages/JPGImages/Dice.png")
		self.copied_png_two_loc = self.base_path.joinpath("TestImages/JPGImages/Mario.png")
		
		self.jpg_one_loc = self.base_path.joinpath("TestImages/JPGImages/Dice.jpg")
		self.jpg_two_loc = self.base_path.joinpath("TestImages/JPGImages/Mario.jpg")
		
		copy_file(str(self.png_one_loc), str(self.jpg_dir))
		copy_file(str(self.png_two_loc), str(self.jpg_dir))
			
		print('testing if ',str(self.base_path.joinpath("TestImages/JPGImages/Dice.png")), ' exists')
		print('testing if ',str(self.base_path.joinpath("TestImages/JPGImages/Mario.png")), ' exists')
		self.assertTrue(verify_file_exists(str(self.copied_png_one_loc)))
		self.assertTrue(verify_file_exists(str(self.copied_png_two_loc)))

	def test_convert_png_to_jpg(self):
		self.base_path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
		self.jpg_dir = self.base_path.joinpath("TestImages").joinpath("JPGImages")
		try:
			os.remove(str(self.base_path.joinpath("TestImages/JPGImages/Mario.png")))
		except Exception as e: 
			print(e)

		try:
			os.remove(str(self.base_path.joinpath("TestImages/JPGImages/Dice.png")))
		except Exception as e: 
			print(e)
			
		self.png_one_loc = self.base_path.joinpath("TestImages/PNGImages/Dice.png")
		self.png_two_loc = self.base_path.joinpath("TestImages/PNGImages/Mario.png")
		
		self.copied_png_one_loc = self.base_path.joinpath("TestImages/JPGImages/Dice.png")
		self.copied_png_two_loc = self.base_path.joinpath("TestImages/JPGImages/Mario.png")
		
		self.jpg_one_loc = self.base_path.joinpath("TestImages/JPGImages/Dice.jpg")
		self.jpg_two_loc = self.base_path.joinpath("TestImages/JPGImages/Mario.jpg")
		
		if not verify_file_exists(str(self.copied_png_one_loc)):
			copy_file(str(self.png_one_loc), str(self.jpg_dir))
			
		if not verify_file_exists(str(self.copied_png_two_loc)):
			copy_file(str(self.png_two_loc), str(self.jpg_dir))
			
		convert_png_to_jpg(str(self.copied_png_one_loc))
		convert_png_to_jpg(str(self.copied_png_two_loc))
		
		self.assertTrue(verify_file_exists(str(self.jpg_one_loc)))
		self.assertTrue(verify_file_exists(str(self.jpg_two_loc)))
	
if __name__ == '__main__':
	unittest.main()