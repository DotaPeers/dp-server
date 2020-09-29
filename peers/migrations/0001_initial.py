# Generated by Django 3.1 on 2020-09-29 22:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import peers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Avatars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small', models.TextField(max_length=255)),
                ('medium', models.TextField(max_length=255)),
                ('large', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Connections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.TextField(unique=True)),
                ('channel_id', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PeerData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('accountId', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.TextField()),
                ('rank', peers.models.RankType(null=True)),
                ('dotaPlus', models.BooleanField(null=True)),
                ('steamId', models.TextField(max_length=255, null=True)),
                ('profileUrl', models.TextField(max_length=255, null=True)),
                ('countryCode', models.TextField(max_length=8, null=True)),
                ('wins', models.IntegerField(default=0)),
                ('loses', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('peersLoaded', models.BooleanField(default=False)),
                ('avatars', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='peers.avatars')),
            ],
        ),
        migrations.CreateModel(
            name='Peer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peers.peerdata')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_from_peers_set', to='peers.player')),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_to_peers_set', to='peers.player')),
            ],
        ),
    ]
