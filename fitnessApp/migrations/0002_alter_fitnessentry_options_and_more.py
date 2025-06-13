from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitnessApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fitnessentry',
            options={},
        ),
        migrations.AlterField(
            model_name='fitnessentry',
            name='activity_type',
            field=models.CharField(choices=[('Running', 'Running'), ('Walking', 'Walking'), ('Cycling', 'Cycling'), ('Gym', 'Gym')], max_length=20),
        ),
        migrations.AlterField(
            model_name='fitnessentry',
            name='date_recorded',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='fitnessentry',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
