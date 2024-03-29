# Generated by Django 5.0.2 on 2024-03-13 17:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mistakes', '0007_alter_maxsulot_name_alter_problem_name'),
        ('User', '0005_alter_bolim_user_alter_xodim_bulimi'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='hisobot',
            name='mahsulot',
            field=models.ForeignKey(default="o'chirilgan mahsulot", on_delete=django.db.models.deletion.SET_DEFAULT, related_name='maxsulot', to='Mistakes.maxsulot'),
        ),
        migrations.AlterField(
            model_name='hisobot',
            name='user',
            field=models.ForeignKey(default="o'chirilgan user", on_delete=django.db.models.deletion.SET_DEFAULT, related_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hisobot',
            name='xato',
            field=models.ForeignKey(blank=True, default="o'chirilgan xato", null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='problem', to='Mistakes.problem'),
        ),
        migrations.AlterField(
            model_name='hisobot',
            name='xodim',
            field=models.ForeignKey(default="o'chirilgan xodim", on_delete=django.db.models.deletion.SET_DEFAULT, related_name='xodim', to='User.xodim'),
        ),
    ]
