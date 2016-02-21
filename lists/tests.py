from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List

class ListAndItemModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()
		
		first_item = Item()
		first_item_text = 'First list item'
		first_item.text = 'First list item'
		first_item.list = list_
		first_item.save()
		
		second_item = Item()
		second_item_text = 'Second list item'
		second_item.text = 'Second list item'
		second_item.list = list_
		second_item.save()
		
		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, first_item_text)
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, second_item_text)
		self.assertEqual(second_saved_item.list, list_)

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page(self):
		found = resolve("/")
		self.assertEqual(found.func, home_page)
		
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('lists/home.html')
		self.assertEqual(response.content.decode(), expected_html)
		
		
class ListViewTests(TestCase):
	
	def test_displays_all_items(self):
		list_ = List.objects.create()
		Item.objects.create(text='1flf', list=list_)
		Item.objects.create(text='2flf', list=list_)
		
		response = self.client.get('/lists/the-only-list-in-the-world/')
		
		self.assertContains(response, '1flf')
		self.assertContains(response, '2flf')
		
	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'lists/list.html')
		
class NewListTests(TestCase):
	
	def test_saveing_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_reidrects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
