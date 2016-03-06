from .base import FunctionalTest

from unittest import skip

from lists.forms import EMPTY_ITEM_ERROR

class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):
		# Edith goes to the home page and accidentally tries to submit
		# an empty list item. She hits Enter on the empty input box
		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('\n')

		# The home page refreshes, and there is an error message saying
		# that list items cannot be blank
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, EMPTY_ITEM_ERROR)

		# She tries again with some text for the item, which now works
		self.get_item_input_box().send_keys('Buy milk\n')
		self.check_for_row_in_list_table('1: Buy milk')

		# Perversely, she now decides to submit a second blank list item
		self.get_item_input_box().send_keys('\n')

		# She receives a similar warning on the list page
		self.check_for_row_in_list_table('1: Buy milk')
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, EMPTY_ITEM_ERROR)

		# And she can correct it by filling some text in
		self.get_item_input_box().send_keys('Buy tea\n')
		self.check_for_row_in_list_table('1: Buy milk')
		self.check_for_row_in_list_table('2: Buy tea')
		
	def test_cannot_add_duplicate_items(self):
		# Edith goes to the home page and starts a new list
		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('buy\n')
		self.check_for_row_in_list_table('1: buy')
		
		# she tries to enter a duplicate item
		self.get_item_input_box().send_keys('buy\n')
		
		# she sees an error message
		self.check_for_row_in_list_table('1: buy')
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "You've already got this in your list")
		
		
