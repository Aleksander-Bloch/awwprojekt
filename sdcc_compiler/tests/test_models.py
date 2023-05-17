from django.test import TestCase
from django.contrib.auth.models import User
from sdcc_compiler.models import Directory, File, Section, StatusData, SectionType, SectionStatus


class DirectoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.directory = Directory.objects.create(name='Test Directory', owner=self.user)

    def test_directory_creation(self):
        self.assertEqual(self.directory.name, 'Test Directory')
        self.assertEqual(self.directory.owner, self.user)
        self.assertTrue(self.directory.is_accessible)
        self.assertIsNotNone(self.directory.creation_date)

    def test_directory_string_representation(self):
        self.assertEqual(str(self.directory), 'Test Directory')


class FileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.directory = Directory.objects.create(name='Test Directory', owner=self.user)
        self.file = File.objects.create(name='test_file.txt', owner=self.user, directory=self.directory)

    def test_file_creation(self):
        self.assertEqual(self.file.name, 'test_file.txt')
        self.assertEqual(self.file.owner, self.user)
        self.assertTrue(self.file.is_accessible)
        self.assertIsNotNone(self.file.creation_date)

    def test_file_string_representation(self):
        self.assertEqual(str(self.file), 'test_file.txt')


class SectionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.directory = Directory.objects.create(name='Test Directory', owner=self.user)
        self.file = File.objects.create(name='test_file.txt', owner=self.user, directory=self.directory)
        self.section = Section.objects.create(
            name='Test Section',
            start_line=1,
            end_line=10,
            content='Section content',
            type=SectionType.PROCEDURE,
            status=SectionStatus.OK,
            file=self.file
        )

    def test_section_creation(self):
        self.assertEqual(self.section.name, 'Test Section')
        self.assertEqual(self.section.start_line, 1)
        self.assertEqual(self.section.end_line, 10)
        self.assertEqual(self.section.content, 'Section content')
        self.assertEqual(self.section.type, SectionType.PROCEDURE)
        self.assertEqual(self.section.status, SectionStatus.OK)
        self.assertEqual(self.section.file, self.file)
        self.assertIsNotNone(self.section.creation_date)

    def test_section_string_representation(self):
        expected_string = 'test_file.txt: PROC [1-10]'
        self.assertEqual(str(self.section), expected_string)


class StatusDataModelTest(TestCase):
    def setUp(self):
        self.status_data = StatusData.objects.create(compilation_log='Compilation log', target_line=5)

    def test_status_data_creation(self):
        self.assertEqual(self.status_data.compilation_log, 'Compilation log')
        self.assertEqual(self.status_data.target_line, 5)


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_models(self):
        directory = Directory.objects.create(name='Test Directory', owner=self.user)
        self.assertIsInstance(directory, Directory)

        file = File.objects.create(name='test_file.txt', owner=self.user, directory=directory)
        self.assertIsInstance(file, File)

        section = Section.objects.create(
            name='Test Section',
            start_line=1,
            end_line=10,
            content='Section content',
            type=SectionType.PROCEDURE,
            status=SectionStatus.OK,
            file=file
        )
        self.assertIsInstance(section, Section)

        status_data = StatusData.objects.create(compilation_log='Compilation log', target_line=5)
        self.assertIsInstance(status_data, StatusData)


class SectionTypeModelTest(TestCase):
    def test_section_type_choices(self):
        self.assertEqual(SectionType.PROCEDURE, 'PROC')
        self.assertEqual(SectionType.COMMENT, 'COM')
        self.assertEqual(SectionType.COMPILER_DIRECTIVE, 'DIR')
        self.assertEqual(SectionType.VARIABLE_DECLARATION, 'VAR')
        self.assertEqual(SectionType.INLINE_ASSEMBLY, 'ASM')


class SectionStatusModelTest(TestCase):
    def test_section_status_choices(self):
        self.assertEqual(SectionStatus.OK, 'OK')
        self.assertEqual(SectionStatus.ERROR, 'ERR')
        self.assertEqual(SectionStatus.WARNING, 'WARN')
