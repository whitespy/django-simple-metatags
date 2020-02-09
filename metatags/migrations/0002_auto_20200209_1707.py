from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metatags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metatag',
            name='url',
            field=models.CharField(blank=True, db_index=True, max_length=100, verbose_name='URL-path'),
        ),
    ]
