"""
dashboard.py — صفحه داشبورد آماری
نمایش آمار کلی مشتریان، نمودارها و آخرین ثبت‌ها
"""

import pandas as pd
import streamlit as st

from utils.helpers import page_header, format_datetime_display
from services.client_service import ClientService


def show():
    """صفحه داشبورد را نمایش می‌دهد."""
    page_header("مدیریت مشتریان", "نمای کلی آمار و وضعیت مشتریان")

    service = ClientService()
    stats = service.get_statistics()
    clients = service.get_all_clients()

    # ─── حالت خالی ────────────────────────────────────────────
    if stats["total"] == 0:
        st.info("هنوز هیچ مشتری‌ای ثبت نشده. ابتدا از منوی «افزودن مشتری» چند مشتری وارد کنید.")
        return

    # ─── کارت‌های آماری ───────────────────────────────────────
    _show_stat_cards(stats)

    st.markdown("---")

    # ─── نمودارها ─────────────────────────────────────────────
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        _show_business_chart(stats)

    with chart_col2:
        _show_status_chart(stats)

    st.markdown("---")

    # ─── آخرین مشتریان ────────────────────────────────────────
    _show_recent_clients(clients)


def _show_stat_cards(stats: dict):
    """
    چهار کارت آماری در یک ردیف نمایش می‌دهد.
    کارت‌ها با HTML/CSS سفارشی (کلاس stat-card) رسم می‌شوند.
    """
    cards = [
        ("کل مشتریان", stats["total"], ""),
        ("🟢 فعال", stats["active"], "success"),
        ("🔴 غیرفعال", stats["inactive"], "danger"),
        ("🟡 در انتظار", stats["pending"], "warning"),
    ]

    columns = st.columns(4)
    for col, (label, value, extra_class) in zip(columns, cards):
        col.markdown(
            f"""
            <div class="stat-card {extra_class}">
                <div class="stat-label">{label}</div>
                <div class="stat-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _show_business_chart(stats: dict):
    """
    نمودار میله‌ای توزیع مشتریان بر اساس نوع کسب‌وکار.
    از st.bar_chart که داخل Streamlit است استفاده می‌کنیم.
    """
    st.subheader("نوع کسب‌وکار")

    if not stats["by_business"]:
        st.caption("داده‌ای برای نمایش وجود ندارد.")
        return

    # تبدیل دیکشنری به DataFrame برای نمودار
    df = pd.DataFrame(
        list(stats["by_business"].items()),
        columns=["نوع کسب‌وکار", "تعداد"]
    ).set_index("نوع کسب‌وکار")

    st.bar_chart(df, height=300, color="#7C3AED")


def _show_status_chart(stats: dict):
    """
    نمودار میله‌ای توزیع وضعیت مشتریان.
    """
    st.subheader("وضعیت مشتریان")

    status_data = {
        "فعال": stats["active"],
        "غیرفعال": stats["inactive"],
        "در انتظار": stats["pending"],
    }
    status_colors = {
        "فعال": "#16a34a",
        "غیرفعال": "#dc2626",
        "در انتظار": "#d97706",
    }

    # فقط وضعیت‌هایی که تعداد بیشتر از صفر دارند نمایش می‌دهیم
    status_data = {k: v for k, v in status_data.items() if v > 0}

    if not status_data:
        st.caption("داده‌ای برای نمایش وجود ندارد.")
        return

    # هر وضعیت یک ردیف جداگانه با ستون رنگ مخصوص خودش
    df = pd.DataFrame([
        {"وضعیت": k, "تعداد": v, "رنگ": status_colors[k]}
        for k, v in status_data.items()
    ])

    st.bar_chart(df, x="وضعیت", y="تعداد", color="رنگ", height=300)


def _show_recent_clients(clients: list):
    """
    جدول ۵ مشتری آخر ثبت‌شده را نمایش می‌دهد.
    مشتریان بر اساس تاریخ ثبت مرتب می‌شوند.
    """
    st.subheader("آخرین مشتریان ثبت‌شده")

    # گرفتن ۵ مشتری آخر (آخر لیست = جدیدترین)
    recent = clients[-5:]
    recent.reverse()  # جدیدترین اول نمایش داده شود

    if not recent:
        return

    # ساخت DataFrame برای نمایش جدول تمیز
    rows = []
    for c in recent:
        status_icon = {"فعال": "🟢", "غیرفعال": "🔴", "در انتظار": "🟡"}.get(c.status, "⚪")
        # ترتیب کلیدها برعکس است تا با direction: rtl ستون «نام» در سمت راست قرار بگیرد
        rows.append({
            "تاریخ ثبت": format_datetime_display(c.created_at),
            "وضعیت": f"{status_icon} {c.status}",
            "نوع کسب‌وکار": c.business_type,
            "تلفن": c.phone,
            "نام‌خانوادگی": c.last_name,
            "نام": c.first_name,
        })

    df = pd.DataFrame(rows)

    # use_container_width جدول را به عرض کامل صفحه می‌کشد
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "تاریخ ثبت": st.column_config.TextColumn("تاریخ ثبت", width="medium"),
            "نوع کسب‌وکار": st.column_config.TextColumn("نوع کسب‌وکار", width="medium"),
        },
    )
