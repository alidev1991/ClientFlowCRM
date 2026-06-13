"""
helpers.py — توابع کمکی مورد استفاده در کل پروژه
"""

import re
import uuid
from datetime import datetime

import streamlit as st

# رنگ اصلی پروژه — در همه‌جا برای هماهنگی بصری استفاده می‌شود
PRIMARY_COLOR = "#2E6F9E"


def page_header(title: str, subtitle: str = ""):
    """
    هدر استاندارد برای هر صفحه را نمایش می‌دهد.
    شامل یک عنوان اصلی و یک زیرعنوان توضیحی است.
    """
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def generate_id() -> str:
    """یک شناسه یکتا ۸ کاراکتری تولید می‌کند."""
    return str(uuid.uuid4())[:8]


def get_current_datetime() -> str:
    """تاریخ و زمان فعلی را به فرمت خوانا برمی‌گرداند."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _gregorian_to_jalali(gy: int, gm: int, gd: int) -> tuple[int, int, int]:
    """
    تاریخ میلادی (سال، ماه، روز) را به تاریخ جلالی تبدیل می‌کند.
    خروجی: تاپل (jy, jm, jd)
    """
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

    if gy > 1600:
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621

    gy2 = gy + 1 if gm > 2 else gy
    days = (
        365 * gy
        + (gy2 + 3) // 4
        - (gy2 + 99) // 100
        + (gy2 + 399) // 400
        - 80
        + gd
        + g_d_m[gm - 1]
    )

    jy += 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461

    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365

    if days < 186:
        jm = 1 + days // 31
        jd = 1 + (days % 31)
    else:
        jm = 7 + (days - 186) // 30
        jd = 1 + ((days - 186) % 30)

    return jy, jm, jd


def format_datetime_display(value: str) -> str:
    """
    رشته تاریخ ذخیره‌شده (مثلاً '2026-06-09 22:17:56') را برای نمایش
    به فرمت خواناتر 'YYYY/MM/DD ساعت HH:MM' با تاریخ جلالی تبدیل می‌کند.
    اگر فرمت نامعتبر بود، مقدار اصلی برگردانده می‌شود.
    """
    try:
        dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        jy, jm, jd = _gregorian_to_jalali(dt.year, dt.month, dt.day)
        return f"{jy}/{jm:02d}/{jd:02d} ساعت {dt.strftime('%H:%M')}"
    except (ValueError, TypeError):
        return value


def validate_first_name(first_name: str) -> bool:
    """
    بررسی می‌کند نام وارد شده باشد.
    خروجی: True اگر حداقل ۲ کاراکتر داشته باشد.
    """
    return len(first_name.strip()) >= 2


def validate_last_name(last_name: str) -> bool:
    """
    بررسی می‌کند نام‌خانوادگی وارد شده باشد.
    خروجی: True اگر حداقل ۲ کاراکتر داشته باشد.
    """
    return len(last_name.strip()) >= 2


def validate_persian_only(text: str) -> bool:
    """
    بررسی می‌کند متن فقط شامل حروف فارسی، فاصله و نیم‌فاصله باشد.
    هیچ حرف انگلیسی (a-z و A-Z) نباید وجود داشته باشد.
    خروجی: True اگر فارسی خالص باشد.
    """
    # اگر هیچ حرف انگلیسی نباشد → معتبر است
    return not bool(re.search(r'[a-zA-Z]', text))


def validate_phone(phone: str) -> bool:
    """
    بررسی می‌کند شماره تلفن فقط شامل اعداد انگلیسی (0-9) باشد.
    اعداد فارسی (۰-۹)، حروف فارسی و انگلیسی مجاز نیستند.
    خروجی: True فقط اگر همه کاراکترها عدد ASCII باشند.
    """
    cleaned = phone.replace("-", "").replace(" ", "")
    # re.fullmatch فقط اعداد 0-9 را قبول می‌کند
    return bool(re.fullmatch(r'[0-9]+', cleaned)) and len(cleaned) >= 8


def validate_email(email: str) -> bool:
    """
    بررسی ساده معتبر بودن فرمت ایمیل.
    خروجی: True اگر @ و . داشته باشد.
    """
    return "@" in email and "." in email


# برای سازگاری با کدهای قدیمی که validate_name را import می‌کنند
def validate_name(name: str) -> bool:
    return len(name.strip()) >= 2
