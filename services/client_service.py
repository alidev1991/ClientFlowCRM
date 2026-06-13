"""
client_service.py — لایه سرویس (منطق کسب‌وکار)
این فایل تمام عملیات روی داده مشتریان را مدیریت می‌کند:
خواندن، نوشتن، ویرایش، حذف و جستجو از فایل CSV.
"""

import os
import pandas as pd
from models.client import Client


# مسیر فایل CSV نسبت به پوشه اصلی پروژه
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "clients.csv")

# ستون‌های فایل CSV — باید با کلیدهای to_dict() یکی باشند
CSV_COLUMNS = ["id", "first_name", "last_name", "phone", "email", "business_type", "status", "notes", "created_at"]


class ClientService:
    """
    این کلاس تمام عملیات CRUD روی مشتریان را انجام می‌دهد.
    CRUD = Create, Read, Update, Delete
    داده‌ها در فایل clients.csv ذخیره می‌شوند.
    """

    def __init__(self):
        """
        هنگام ساخته شدن سرویس، اگر فایل CSV وجود نداشت، آن را می‌سازد.
        """
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """
        متد خصوصی (private) — با _ شروع می‌شود.
        بررسی می‌کند فایل CSV وجود دارد، اگر نه آن را می‌سازد.
        """
        if not os.path.exists(DATA_FILE):
            # ساخت یک DataFrame خالی با ستون‌های مشخص
            df = pd.DataFrame(columns=CSV_COLUMNS)
            df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

    def _load_dataframe(self) -> pd.DataFrame:
        """
        فایل CSV را می‌خواند و به DataFrame تبدیل می‌کند.
        encoding="utf-8-sig" برای پشتیبانی از فارسی در ویندوز لازم است.
        """
        return pd.read_csv(DATA_FILE, encoding="utf-8-sig", dtype=str).fillna("")

    def _save_dataframe(self, df: pd.DataFrame):
        """
        DataFrame را در فایل CSV ذخیره می‌کند.
        """
        df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

    # ─── CREATE ───────────────────────────────────────────────

    def add_client(self, client: Client) -> bool:
        """
        یک مشتری جدید به فایل CSV اضافه می‌کند.
        ورودی: شیء Client
        خروجی: True اگر موفق باشد
        """
        df = self._load_dataframe()
        new_row = pd.DataFrame([client.to_dict()])
        df = pd.concat([df, new_row], ignore_index=True)
        self._save_dataframe(df)
        return True

    # ─── READ ─────────────────────────────────────────────────

    def get_all_clients(self) -> list[Client]:
        """
        تمام مشتریان را از CSV می‌خواند و لیستی از اشیاء Client برمی‌گرداند.
        """
        df = self._load_dataframe()
        clients = []
        for _, row in df.iterrows():
            clients.append(Client.from_dict(row.to_dict()))
        return clients

    def search_clients(self, query: str) -> list[Client]:
        """
        جستجو در نام، تلفن و ایمیل مشتریان.
        ورودی: متن جستجو
        خروجی: لیست مشتریانی که شامل متن جستجو می‌شوند
        """
        query = query.strip().lower()
        if not query:
            return self.get_all_clients()

        df = self._load_dataframe()

        # جستجو در ستون‌های مختلف به صورت همزمان
        mask = (
            df["name"].str.lower().str.contains(query, na=False)
            | df["phone"].str.contains(query, na=False)
            | df["email"].str.lower().str.contains(query, na=False)
            | df["business_type"].str.lower().str.contains(query, na=False)
        )
        filtered = df[mask]

        return [Client.from_dict(row.to_dict()) for _, row in filtered.iterrows()]

    # ─── UPDATE ───────────────────────────────────────────────

    def update_client(self, updated_client: Client) -> bool:
        """
        اطلاعات یک مشتری موجود را بروزرسانی می‌کند.
        ورودی: شیء Client با اطلاعات جدید (ID باید همان قبلی باشد)
        خروجی: True اگر پیدا و بروزرسانی شد، False اگر پیدا نشد
        """
        df = self._load_dataframe()
        idx = df.index[df["id"] == updated_client.id].tolist()

        if not idx:
            return False

        # بروزرسانی ردیف مربوطه
        for key, value in updated_client.to_dict().items():
            df.at[idx[0], key] = value

        self._save_dataframe(df)
        return True

    # ─── DELETE ───────────────────────────────────────────────

    def delete_client(self, client_id: str) -> bool:
        """
        یک مشتری را با ID از CSV حذف می‌کند.
        خروجی: True اگر پیدا و حذف شد، False اگر پیدا نشد
        """
        df = self._load_dataframe()
        original_len = len(df)
        df = df[df["id"] != client_id]

        if len(df) == original_len:
            return False  # مشتری پیدا نشد

        self._save_dataframe(df)
        return True

    # ─── STATISTICS ───────────────────────────────────────────

    def get_statistics(self) -> dict:
        """
        آمار کلی مشتریان را برمی‌گرداند.
        برای داشبورد استفاده می‌شود.
        """
        df = self._load_dataframe()

        if df.empty:
            return {
                "total": 0,
                "active": 0,
                "inactive": 0,
                "pending": 0,
                "by_business": {},
            }

        return {
            "total": len(df),
            "active": len(df[df["status"] == "فعال"]),
            "inactive": len(df[df["status"] == "غیرفعال"]),
            "pending": len(df[df["status"] == "در انتظار"]),
            "by_business": df["business_type"].value_counts().to_dict(),
        }
