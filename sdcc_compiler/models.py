from django.db import models


class File(models.Model):
    name = models.CharField(max_length=50)
    directory = models.ForeignKey('Directory', related_name='files', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Directory(models.Model):
    name = models.CharField(max_length=50)
    # description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def get_tree(self):
        tree = {'name': self.name}
        if not self.parent:
            tree['isRoot'] = True
        if self.children.exists():
            tree['children'] = [child.get_tree() for child in self.children.all()]
        if self.files.exists():
            tree['files'] = [f.name for f in self.files.all()]
        return tree

    def __str__(self):
        return self.name
