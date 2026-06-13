"""
client.py — کلاس Client
این کلاس ساختار داده یک مشتری را تعریف می‌کند.
"""

from utils.helpers import generate_id, get_current_datetime


class Client:
    """
    نمایش‌دهنده یک مشتری در سیستم CRM.
    نام و نام‌خانوادگی به صورت جداگانه ذخیره می‌شوند.
    """

    BUSINESS_TYPES = [
        "وکیل",
        "مشاور املاک",
        "آموزشگاه",
        "فروشگاه",
        "پزشک / کلینیک",
        "سایر",
    ]

    STATUS_OPTIONS = ["فعال", "غیرفعال", "در انتظار"]

    def __init__(
        self,
        first_name: str,
        last_name: str,
        phone: str,
        email: str,
        business_type: str,
        status: str = "فعال",
        notes: str = "",
        client_id: str = None,
        created_at: str = None,
    ):
        self.id = client_id if client_id else generate_id()
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.phone = phone.strip()
        self.email = email.strip()
        self.business_type = business_type
        self.status = status
        self.notes = notes.strip()
        self.created_at = created_at if created_at else get_current_datetime()

    @property
    def full_name(self) -> str:
        """
        نام کامل را از ترکیب نام و نام‌خانوادگی برمی‌گرداند.
        property یعنی مثل یک ویژگی فراخوانی می‌شود: client.full_name
        """
        return f"{self.first_name} {self.last_name}"

    def to_dict(self) -> dict:
        """شیء Client را به دیکشنری تبدیل می‌کند (برای ذخیره در CSV)."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "business_type": self.business_type,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Client":
        """یک ردیف CSV را به شیء Client تبدیل می‌کند."""
        return cls(
            client_id=data.get("id", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            business_type=data.get("business_type", "سایر"),
            status=data.get("status", "فعال"),
            notes=data.get("notes", ""),
            created_at=data.get("created_at", ""),
        )

    def __repr__(self) -> str:
        return f"Client(id={self.id}, name={self.full_name}, status={self.status})"
