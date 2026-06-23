from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extended user model with Omni-Guard roles.
    Roles: admin | manager | cashier
    """
    ROLE_CHOICES = [
        ("admin",   "Admin"),
        ("manager", "Store Manager"),
        ("cashier", "Cashier"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="cashier")
    branch = models.ForeignKey(
        "core.Branch",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="staff",
    )
    phone = models.CharField(max_length=20, blank=True)
    is_2fa_enabled = models.BooleanField(default=False)

    def is_admin(self):
        return self.role == "admin"

    def is_manager(self):
        return self.role in ("admin", "manager")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
