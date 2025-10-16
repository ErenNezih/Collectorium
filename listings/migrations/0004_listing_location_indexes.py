from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0003_listing_attributes_indexes"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="city",
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name="listing",
            name="district",
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddIndex(
            model_name="listing",
            index=models.Index(fields=["city", "district"], name="list_city_dist_idx"),
        ),
    ]



