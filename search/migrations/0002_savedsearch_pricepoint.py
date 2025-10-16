from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("search", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("listings", "0004_listing_location_indexes"),
    ]

    operations = [
        migrations.CreateModel(
            name="SavedSearch",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80)),
                ("querystring", models.TextField()),
                ("frequency", models.CharField(choices=[("daily", "Daily"), ("weekly", "Weekly")], db_index=True, default="daily", max_length=10)),
                ("active", models.BooleanField(db_index=True, default=True)),
                ("last_run_at", models.DateTimeField(blank=True, null=True)),
                ("qhash", models.CharField(blank=True, db_index=True, default="", max_length=32)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="saved_searches", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
                "unique_together": {("user", "name")},
            },
        ),
        migrations.CreateModel(
            name="PricePoint",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("kind", models.CharField(choices=[("list", "List"), ("sale", "Sale")], db_index=True, max_length=10)),
                ("price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("currency", models.CharField(default="TRY", max_length=3)),
                ("at", models.DateTimeField(db_index=True)),
                ("source", models.CharField(default="created", max_length=20)),
                ("listing", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="price_points", to="listings.listing")),
            ],
            options={
                "ordering": ["-at"],
            },
        ),
        migrations.AddIndex(
            model_name="savedsearch",
            index=models.Index(fields=["user", "active", "frequency"], name="saved_user_active_freq_idx"),
        ),
        migrations.AddIndex(
            model_name="pricepoint",
            index=models.Index(fields=["listing", "at"], name="pp_listing_at_idx"),
        ),
        migrations.AddIndex(
            model_name="pricepoint",
            index=models.Index(fields=["listing", "kind", "at"], name="pp_listing_kind_at_idx"),
        ),
    ]


