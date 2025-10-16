from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("stores", "0003_store_rating_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="StorePolicy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("return_policy_text", models.TextField(blank=True, null=True)),
                ("shipping_policy_text", models.TextField(blank=True, null=True)),
                ("contact_hours", models.CharField(blank=True, max_length=120, null=True)),
                ("handling_time_days", models.PositiveIntegerField(blank=True, null=True)),
                ("extra_notes", models.TextField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("store", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="policy", to="stores.store")),
            ],
            options={"ordering": ["-updated_at"]},
        ),
    ]


