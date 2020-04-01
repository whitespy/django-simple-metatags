from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metatags', '0002_auto_20200209_1707'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='metatag',
            table='metatags',
        ),
    ]
