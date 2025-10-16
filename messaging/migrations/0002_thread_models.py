from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from django.db.models import Q


class Migration(migrations.Migration):

    dependencies = [
        ("messaging", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("listings", "0004_listing_location_indexes"),
    ]

    operations = [
        migrations.CreateModel(
            name="Thread",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_open", models.BooleanField(default=True)),
                ("last_message_at", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("buyer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="threads_as_buyer", to=settings.AUTH_USER_MODEL)),
                ("seller", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="threads_as_seller", to=settings.AUTH_USER_MODEL)),
                ("listing", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="threads", to="listings.listing")),
            ],
            options={"ordering": ["-last_message_at", "-created_at"]},
        ),
        migrations.AddConstraint(
            model_name="thread",
            constraint=models.UniqueConstraint(fields=("listing", "buyer", "seller"), condition=Q(("is_open", True)), name="uniq_open_thread_per_listing_buyer_seller"),
        ),
        migrations.CreateModel(
            name="ThreadMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("raw_text", models.TextField()),
                ("redacted_text", models.TextField(blank=True, null=True)),
                ("has_contact_violation", models.BooleanField(default=False)),
                ("was_rate_limited", models.BooleanField(default=False)),
                ("is_reported", models.BooleanField(default=False)),
                ("read_by_buyer", models.BooleanField(default=False)),
                ("read_by_seller", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("sender", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="thread_messages", to=settings.AUTH_USER_MODEL)),
                ("thread", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="messaging.thread")),
            ],
            options={"ordering": ["created_at"]},
        ),
        migrations.CreateModel(
            name="Block",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reason", models.TextField(blank=True, null=True)),
                ("expires_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("blocked", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="blocks_received", to=settings.AUTH_USER_MODEL)),
                ("blocker", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="blocks_initiated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddIndex(
            model_name="block",
            index=models.Index(fields=["blocker", "blocked"], name="block_pair_idx"),
        ),
    ]


