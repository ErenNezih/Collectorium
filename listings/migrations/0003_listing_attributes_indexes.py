from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0002_favorite"),
    ]

    operations = [
        # TrigramExtension() removed for SQLite compatibility
        migrations.AddField(
            model_name="listing",
            name="attributes",
            field=models.JSONField(default=dict, blank=True),
        ),
        migrations.AddIndex(
            model_name="listing",
            index=models.Index(fields=["is_active", "created_at"], name="list_active_created_idx"),
        ),
        migrations.AddIndex(
            model_name="listing",
            index=models.Index(fields=["price"], name="list_price_idx"),
        ),
        migrations.AddIndex(
            model_name="listing",
            index=models.Index(fields=["condition"], name="list_condition_idx"),
        ),
    ]



