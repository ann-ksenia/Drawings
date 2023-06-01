from django.db import models

class User(models.Model):
    st1 = 'Creator'
    st2 = 'Editor'
    st3 = 'Witness'
    STATUSES = [
        (st1, 'Creator'),
        (st2, 'Editor'),
        (st3, 'Witness')
    ]

    name = models.CharField(blank=False, null = False, verbose_name='Username', max_length=50)
    status = models.CharField(choices=STATUSES, default=st2, null=False, blank=False, verbose_name='status', max_length=20)
    room = models.ForeignKey('Room', on_delete= models.CASCADE, null=False, blank=False, verbose_name='room name')

class Room(models.Model):
    name = models.CharField(unique=True, blank=False, null=False, verbose_name='room name', max_length=200)

    def delete(self, *args, **kwargs):
        for i in User.objects.filter(room = self):
            i.delete()
        super(Room,self).delete(*args,**kwargs)