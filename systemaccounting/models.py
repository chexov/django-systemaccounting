from django.db import models

class Accounting(models.Model):
    unixuser = models.CharField(max_length=10)
    number_of_commands = models.IntegerField()
    cputime = models.FloatField()
    io_operaions = models.IntegerField()
    cpu_integral = models.IntegerField()
    server = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    

    def __unicode__(self):
        return "%s: %s, %scpu, %s" % (self.server, self.unixuser, self.cputime)


class Quota(models.Model):
    #   Filesystem  KBytes    quota   limit   grace    files   quota   limit   grace
    #         /var  616984   600000  700000    none     170        0       0        
    unixuser = models.CharField(max_length=10)
    filesystem = models.CharField(max_length=255)
    kbytes = models.IntegerField()
    quota = models.IntegerField()
    limit = models.IntegerField()
    files = models.IntegerField()
    server = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s, %sKBytes, %s" % (self.unixuser, self.kbytes, self.limit)
