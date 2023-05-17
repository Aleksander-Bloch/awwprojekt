from django.contrib.auth.models import User
from django.test import TestCase

from sdcc_compiler.forms import AddDirectoryForm, AddFileForm, AddSectionForm
from sdcc_compiler.models import Directory, File


class AddDirectoryFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_form_valid(self):
        form_data = {'name': 'Test Directory'}
        form = AddDirectoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {'name': ''}
        form = AddDirectoryForm(data=form_data)
        self.assertFalse(form.is_valid())


class AddFileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.directory = Directory.objects.create(name='Test Directory', owner=self.user)

    def test_form_invalid1(self):
        form_data = {'name': 'test_file.txt'}
        form = AddFileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid2(self):
        form_data = {'name': ''}
        form = AddFileForm(data=form_data)
        self.assertFalse(form.is_valid())


class AddSectionFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.directory = Directory.objects.create(name='Test Directory', owner=self.user)
        self.file = File.objects.create(name='test_file.txt', owner=self.user, directory=self.directory)

    def test_form_valid(self):
        form_data = {
            'name': 'Test Section',
            'description': 'Section description',
            'type': 'PROC',
            'start_line': 1,
            'end_line': 10,
            'content': 'Section content',
            'file': self.file.id,
        }
        form = AddSectionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            'name': '',
            'description': '',
            'type': 'PROC',
            'start_line': 1,
            'end_line': 10,
            'content': '',
            'file': self.file.id,
        }
        form = AddSectionForm(data=form_data)
        self.assertFalse(form.is_valid())
