# Generated by Django 4.1.5 on 2023-01-24 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='text',
            name='language',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.language'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField()),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.text')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.word')),
            ],
        ),
    ]
