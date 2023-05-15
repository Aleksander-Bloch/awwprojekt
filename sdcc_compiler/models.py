from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    name = models.CharField(max_length=50)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Directory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(default=now)
    owner = models.ForeignKey('User', null=True, blank=True, related_name='directories', on_delete=models.CASCADE)
    is_accessible = models.BooleanField(default=True)
    access_change = models.DateTimeField(default=now)
    last_modification = models.DateTimeField(default=now)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def get_tree(self):
        tree = {'name': self.name, 'id': self.id, 'is_accessible': self.is_accessible}
        if self.children.exists():
            tree['children'] = [child.get_tree() for child in self.children.all()]
        if self.files.exists():
            tree['files'] = [{'name': f.name, 'id': f.id, 'is_accessible': self.is_accessible}
                             for f in self.files.all()]
        return tree

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(default=now)
    owner = models.ForeignKey('User', null=True, blank=True, related_name='files', on_delete=models.CASCADE)
    is_accessible = models.BooleanField(default=True)
    access_change = models.DateTimeField(default=now)
    last_modification = models.DateTimeField(default=now)
    directory = models.ForeignKey('Directory', null=True, blank=True, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.name


class SectionType(models.TextChoices):
    PROCEDURE = 'PROC', _('Procedure')
    COMMENT = 'COM', _('Comment')
    COMPILER_DIRECTIVE = 'DIR', _('Compiler directive')
    VARIABLE_DECLARATION = 'VAR', _('Variable declaration')
    INLINE_ASSEMBLY = 'ASM', _('Inline assembly')


class SectionStatus(models.TextChoices):
    OK = 'OK', _('Compiles without warnings')
    ERROR = 'ERR', _('Does not compile')
    WARNING = 'WARN', _('Compiles with warnings')


class StatusData(models.Model):
    compilation_log = models.TextField()
    target_line = models.IntegerField()


class Section(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(default=now)
    start_line = models.IntegerField()
    end_line = models.IntegerField()
    content = models.TextField()
    type = models.CharField(max_length=4, choices=SectionType.choices)
    status = models.CharField(max_length=4, choices=SectionStatus.choices, default=SectionStatus.OK)
    status_data = models.OneToOneField('StatusData', null=True, blank=True, on_delete=models.CASCADE)
    file = models.ForeignKey('File', related_name='sections', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='sections', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.file.name}: {self.type} [{self.start_line}-{self.end_line}]"
