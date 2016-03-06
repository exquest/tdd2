from django.test import TestCase

from lists.forms import(
	ItemForm, EMPTY_ITEM_ERROR,
	DUPLICATE_ITEM_ERROR, ExistingListItemForm
)
from lists.models import List, Item


class ItemFormTest(TestCase):
		
	def test_form_input_has_placeholder_and_css_classes(self):
		form = ItemForm()
		self.assertIn('placeholder="Enter a To-Do item"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())
		
	def test_form_validation_for_blank_item(self):
		form = ItemForm(data={'text': ''})
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['text'],
			[EMPTY_ITEM_ERROR]
		)
	def test_form_save_handles_saving_form_to_list(self):
		list_ = List.objects.create()
		form = ItemForm(data={'text': 'do me'})
		new_item = form.save(for_list=list_)
		self.assertEqual(new_item, Item.objects.first())
		self.assertEqual(new_item.text, 'do me')
		self.assertEqual(new_item.list, list_)
		
class ExistingItemFormTest(TestCase):
		
	def test_form_renders_item_text_input(self):
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_)
		self.assertIn('placeholder="Enter a To-Do item"', form.as_p())
		
	def test_form_validation_for_blank_item(self):
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_, data={'text': '',})
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['text'],
			[EMPTY_ITEM_ERROR]
		)
	def test_form_validation_for_duplicate_items(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='txt')
		form = ExistingListItemForm(for_list=list_, data={'text': 'txt'})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])
		
	def test_form_save(self):
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
		new_item = form.save()
		self.assertEqual(new_item, Item.objects.all()[0])
