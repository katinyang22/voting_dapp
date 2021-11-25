# Generated by Django 3.2.9 on 2021-11-25 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elections', '0005_alter_election_vote_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='candidate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidate', to=settings.AUTH_USER_MODEL, verbose_name='Candidate'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.election', verbose_name='Election'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='voter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voter', to=settings.AUTH_USER_MODEL, verbose_name='Voter'),
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(fields=('voter', 'election'), name='each_user_can_have_one_vote_for_an_election'),
        ),
    ]
