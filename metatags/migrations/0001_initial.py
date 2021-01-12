from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=100, verbose_name='URL-path')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('title', models.CharField(blank=True, max_length=80, verbose_name='title')),
                ('keywords', models.CharField(blank=True, max_length=250, verbose_name='keywords')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                                   to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'meta tags',
                'verbose_name_plural': 'meta tags',
                'db_table': 'meta_tags',
                'ordering': ['id'],
                'unique_together': {('content_type', 'object_id')},
            },
        ),
    ]
