from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("moderation", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("target_type", models.CharField(choices=[("listing", "Listing"), ("message", "Message"), ("user", "User")], db_index=True, max_length=20)),
                ("target_id", models.PositiveIntegerField(db_index=True)),
                ("reason", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True, null=True)),
                ("status", models.CharField(choices=[("open", "Open"), ("actioned", "Actioned"), ("closed", "Closed")], db_index=True, default="open", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("reporter", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="reports", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddIndex(
            model_name="report",
            index=models.Index(fields=["target_type", "target_id", "status"], name="report_target_status_idx"),
        ),
        migrations.CreateModel(
            name="ModerationAction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action", models.CharField(choices=[("hide_listing", "Hide Listing"), ("delete_message", "Delete Message"), ("warn_user", "Warn User"), ("ban_user", "Ban User"), ("no_action", "No Action")], max_length=30)),
                ("severity", models.CharField(choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")], default="low", max_length=10)),
                ("notes", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("actor", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="moderation_actions", to=settings.AUTH_USER_MODEL)),
                ("report", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="actions", to="moderation.report")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="RiskSignal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("entity_type", models.CharField(db_index=True, max_length=20)),
                ("entity_id", models.PositiveIntegerField(db_index=True)),
                ("type", models.CharField(choices=[("velocity", "Velocity"), ("high_amount", "High Amount"), ("first_order", "First Order"), ("contact_leak", "Contact Leak")], max_length=20)),
                ("severity", models.CharField(choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")], db_index=True, default="low", max_length=10)),
                ("meta", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddIndex(
            model_name="risksignal",
            index=models.Index(fields=["entity_type", "entity_id", "type"], name="risk_entity_type_idx"),
        ),
        migrations.AddIndex(
            model_name="risksignal",
            index=models.Index(fields=["created_at"], name="risk_created_idx"),
        ),
    ]


