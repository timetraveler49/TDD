from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item,List

class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_user = List()
        list_user.save()

        first_item = Item()
        first_item.text = 'The first list item'
        first_item.list = list_user
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_user
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list,list_user)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item')
        self.assertEqual(first_saved_item.list,list_user)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_user)


# Create your tests here.
class HomePageTest(TestCase):

    # def test_displays_list_item(self):
    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')
    #     response = self.client.get('/')
    #     self.assertIn('itemey 1', response.content.decode())
    #     self.assertIn('itemey 2', response.content.decode())

    def test_home_page_return_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')



    # def test_only_saves_items_when_necessary(self):
    #     self.client.get('/')
    #     self.assertEqual(Item.objects.count(), 0)

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response,f'/lists/{new_list.id}/')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_user = List.objects.create()
        response = self.client.get(f'/lists/{list_user.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        corrtect_list = List.objects.create()
        Item.objects.create(text='itemey 1',list=corrtect_list)
        Item.objects.create(text='itemey 2',list=corrtect_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1',list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{corrtect_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        corrtect_list = List.objects.create()
        response = self.client.get(f'/lists/{corrtect_list.id}/')
        self.assertEqual(response.context['list'],corrtect_list)

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        corrtect_list = List.objects.create()

        self.client.post(
            f'/lists/{corrtect_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new item for an existing list')
        self.assertEqual(new_item.list, corrtect_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        corrtect_list = List.objects.create()

        response = self.client.post(
            f'/lists/{corrtect_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{corrtect_list.id}/')