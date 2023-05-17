from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from sdcc_compiler.models import Directory, File, Section


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sdcc_compiler/index.html')

        self.assertIn('file_tree', response.context)
        self.assertIn('root_files', response.context)
        self.assertIn('add_dir_form', response.context)
        self.assertIn('add_file_form', response.context)
        self.assertIn('add_section_form', response.context)


class AddDirectoryViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_add_directory_view(self):
        response = self.client.post(reverse('add_directory'), {'name': 'New Directory'})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Directory.objects.count(), 1)
        new_directory = Directory.objects.first()
        self.assertEqual(new_directory.name, 'New Directory')


class AddFileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.directory = Directory.objects.create(name='Test Directory', owner=self.user)

    def test_add_file_view(self):
        with open('sdcc_compiler/tests/test_file.c', 'rb') as file:
            file_content = file.read().decode('utf-8')
        file = SimpleUploadedFile('test_file.c', file_content.encode('utf-8'), content_type='text/plain')
        response = self.client.post(reverse('add_file'),
                                    {'name': 'Test File', 'directory': self.directory.id, 'file': file})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(File.objects.count(), 1)
        new_file = File.objects.first()
        self.assertEqual(new_file.name, 'Test File')
        self.assertEqual(new_file.directory, self.directory)


class ViewFileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        with open('sdcc_compiler/tests/test_file.c', 'rb') as file:
            file_content = file.read().decode('utf-8')
        file = SimpleUploadedFile('test_file.c', file_content.encode('utf-8'), content_type='text/plain')
        self.file = File.objects.create(name='Test File', owner=self.user, file=file)

    def test_view_file_view(self):
        response = self.client.get(reverse('view_file', kwargs={'file_id': self.file.id}))
        self.assertEqual(response.status_code, 200)

        self.assertIn('file_content', response.json())
        self.assertIn('sections', response.json())


class DeleteDirectoryViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.directory = Directory.objects.create(name='Test Directory', owner=self.user)

    def test_delete_directory_view(self):
        response = self.client.post(reverse('delete_directory', kwargs={'directory_id': self.directory.id}))
        self.assertEqual(response.status_code, 200)

        self.directory.refresh_from_db()
        self.assertFalse(self.directory.is_accessible)


class DeleteFileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.file = File.objects.create(name='Test File', owner=self.user)

    def test_delete_file_view(self):
        response = self.client.post(reverse('delete_file', kwargs={'file_id': self.file.id}))
        self.assertEqual(response.status_code, 200)
        self.file.refresh_from_db()
        self.assertFalse(self.file.is_accessible)


class CompileFileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        with open('sdcc_compiler/tests/test_file.c', 'rb') as file:
            file_content = file.read().decode('utf-8')
        file = SimpleUploadedFile('test_file.c', file_content.encode('utf-8'), content_type='text/plain')
        self.file = File.objects.create(name='Test File', owner=self.user, file=file)

    def test_compile_file_view(self):
        response = self.client.post(reverse('compile_file', kwargs={'file_id': self.file.id}),
                                    {'standard_choice': '--std-sdcc11',
                                     'optimization_choice': ['--nooverlay', '--opt-code-speed'],
                                     'processor_choice': '-mmcs51', 'mcs51_dependent_choice': '--model-small'
                                     })
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('asm_sections', data)


class DownloadASMViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_download_asm_view(self):
        response = self.client.get(reverse('download_asm'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="output.asm"')
        self.assertEqual(response['Content-Type'], 'text/plain')


class AddSectionViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.file = File.objects.create(name='Test File', owner=self.user)

    def test_add_section_view(self):
        response = self.client.post(reverse('add_section'),
                                    {'name': 'Test Section', 'description': 'Section description',
                                     'type': 'PROC', 'start_line': 1, 'end_line': 10, 'content': 'Section content',
                                     'file': self.file.id})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Section.objects.count(), 1)
        new_section = Section.objects.first()
        self.assertEqual(new_section.name, 'Test Section')
