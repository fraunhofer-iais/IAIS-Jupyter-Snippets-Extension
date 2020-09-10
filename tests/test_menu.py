import unittest

from snippetlib.menu import MenuHandler as mh 

class TestMenuHandler(unittest.TestCase):
      def test_menu(self):
          s = mh.menu()
          self.assertIsNotNone(s)

