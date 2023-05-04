from django.db import models
from django.utils.timezone import now


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
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=50)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name
