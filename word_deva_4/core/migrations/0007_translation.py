# Generated by Django 4.1.5 on 2023-01-27 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_string_remove_term_word_delete_word_term_string'),
    ]

    operations = [
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relevance', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True)),
                ('notes', models.CharField(blank=True, max_length=120, null=True)),
                ('from_string', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_string', to='core.string')),
                ('to_string', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_string', to='core.string')),
            ],
        ),
    ]
