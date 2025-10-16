from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stores", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="store",
            name="rating_avg",
            field=models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2),
        ),
        migrations.AddField(
            model_name="store",
            name="rating_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]


