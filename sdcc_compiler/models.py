from django.db import models


class File(models.Model):
    name = models.CharField(max_length=50)
    directory = models.ForeignKey('Directory', null=True, blank=True, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/', null=True, blank=True)

    def __str__(self):
        return self.name


class Directory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def get_tree(self):
        tree = {'name': self.name, 'id': self.id}
        if self.children.exists():
            tree['children'] = [child.get_tree() for child in self.children.all()]
        if self.files.exists():
            tree['files'] = [{'name': f.name, 'id': f.id} for f in self.files.all()]
        return tree

    def __str__(self):
        return self.name
