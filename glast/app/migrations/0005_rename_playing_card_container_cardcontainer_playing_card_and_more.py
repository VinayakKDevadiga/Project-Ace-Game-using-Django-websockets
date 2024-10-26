# Generated by Django 5.0.6 on 2024-07-13 17:21

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_game_created_cardcontainer_username_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cardcontainer',
            old_name='playing_card_container',
            new_name='playing_card',
        ),
        migrations.AddField(
            model_name='game',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cardcontainer',
            name='group_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.game'),
        ),
        migrations.AlterField(
            model_name='cardcontainer',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.users'),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_starting_player',
            field=models.CharField(max_length=100),
        ),
    ]
