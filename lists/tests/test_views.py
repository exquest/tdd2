from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List


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
		correct_list = List.objects.create()
		Item.objects.create(text='1flf', list=correct_list)
		Item.objects.create(text='2flf', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other 1flf', list=other_list)
		Item.objects.create(text='other 2flf', list=other_list)
		
		response = self.client.get('/lists/%d/' % (correct_list.id,))
		
		self.assertContains(response, '1flf')
		self.assertContains(response, '2flf')
		self.assertNotContains(response, 'other 1flf')
		self.assertNotContains(response, 'other 2flf')
		
	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'lists/list.html')
		
	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		response = self.client.get('/lists/%d/' % (correct_list.id,))
		
		self.assertEqual(response.context['list'], correct_list)
	
	def test_can_save_POST_request_to_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		self.client.post(
			'/lists/%d/' % (correct_list.id),
			data = {'item_text' : 'List item'},
		)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'List item')
		self.assertEqual(new_item.list, correct_list)
		
	def test_POST_redirects_list_to_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		response = self.client.post(
			'/lists/%d/' % (correct_list.id),
			data = {'item_text' : 'List item'},
		)
		
		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
		
class NewListTests(TestCase):
	
	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		new_list = List.objects.first()
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
		
	def test_validation_errors_are_sent_back_to_home_page_template(self):
		response = self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'lists/home.html')
		expected_error = escape("You can't have an empty list item")
		self.assertContains(response, expected_error)
		
	def test_invalid_list_items_arent_saved(self):
		self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)

