# Generated by Django 5.1.2 on 2024-10-17 22:17

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="groupproduct",
            name="level",
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="groupproduct",
            name="lft",
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="groupproduct",
            name="rght",
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="groupproduct",
            name="tree_id",
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="groupproduct",
            name="is_show_name",
            field=models.BooleanField(default=False, help_text="Отображать название группы?"),
        ),
        migrations.AlterField(
            model_name="groupproduct",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                help_text="Родительская группа (если есть)",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="children",
                to="product.groupproduct",
            ),
        ),
    ]
