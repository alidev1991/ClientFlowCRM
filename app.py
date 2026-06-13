"""
app.py — نقطه ورودی اصلی برنامه ClientFlow CRM
برنامه با دستور زیر اجرا می‌شود:
    streamlit run app.py
"""

import streamlit as st

# ─── تنظیمات صفحه ─────────────────────────────────────────────
# این دستور باید اولین دستور Streamlit در برنامه باشد
st.set_page_config(
    page_title="ClientFlow CRM",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.helpers import PRIMARY_COLOR

# ─── وارد کردن صفحات ──────────────────────────────────────────
# هر صفحه در یک فایل جداگانه در پوشه views قرار دارد
from views import add_client
from views import client_list
from views import dashboard


# ─── استایل سفارشی ────────────────────────────────────────────
def apply_custom_style():
    """استایل CSS اضافی برای بهبود ظاهر برنامه"""
    st.markdown(
        f"""
        <style>
        /* فونت فارسی Vazirmatn */
        @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700&display=swap');
        html, body, [class*="css"], .stApp, .stApp * {{
            font-family: 'Vazirmatn', sans-serif !important;
        }}

        /* راست‌چین کردن متن‌های فارسی */
        .stApp {{ direction: rtl; }}
        .stTextInput label, .stSelectbox label,
        .stTextArea label, .stForm label {{ font-weight: bold; }}
        /* حذف پیام "PRESS ENTER TO SUBMIT FORM" از تکست باکس‌ها */
        [data-testid="InputInstructions"] {{ display: none !important; }}

        /* کارت‌های آماری سفارشی داشبورد */
        .stat-card {{
            background-color: #ffffff;
            border: 1px solid #e6e6e6;
            border-radius: 10px;
            padding: 18px 16px;
            border-right: 4px solid {PRIMARY_COLOR};
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            text-align: right;
        }}
        .stat-card .stat-label {{
            font-size: 14px;
            color: #6b7280;
            margin-bottom: 6px;
        }}
        .stat-card .stat-value {{
            font-size: 28px;
            font-weight: 700;
            color: #1f2937;
        }}
        .stat-card.success {{
            border-right: 4px solid #16a34a;
        }}
        .stat-card.danger {{
            border-right: 4px solid #dc2626;
        }}
        .stat-card.warning {{
            border-right: 4px solid #d97706;
        }}

        /* هدر صفحات */
        .page-title {{
            font-size: 28px;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 0;
            text-align: right;
        }}
        .page-subtitle {{
            font-size: 15px;
            color: #6b7280;
            margin-top: 4px;
            margin-bottom: 16px;
            text-align: right;
        }}

        /* راست‌چین کردن تیترها و زیرتیترها در محتوای اصلی (بدون سایدبار) */
        section[data-testid="stMain"] h1,
        section[data-testid="stMain"] h2,
        section[data-testid="stMain"] h3,
        section[data-testid="stMain"] h4 {{
            text-align: right;
        }}

        /* راست‌چین کردن جدول‌ها */
        section[data-testid="stMain"] [data-testid="stDataFrame"] {{
            direction: rtl;
        }}

        /* راست‌چین کردن متن‌های کم‌رنگ (caption) */
        section[data-testid="stMain"] [data-testid="stCaptionContainer"] {{
            text-align: right;
        }}

        /* جلوگیری از به‌هم‌ریختگی برچسب‌های نمودار به دلیل rtl کلی صفحه */
        section[data-testid="stMain"] [data-testid="stVegaLiteChart"] {{
            direction: ltr;
        }}

        /* پس‌زمینه بخش اصلی محتوا */
        section[data-testid="stMain"] {{
            background-color: #f7f8fa;
        }}

        /* دکمه اصلی با رنگ هماهنگ */
        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"],
        [data-testid="stBaseButton-primary"],
        [data-testid="stBaseButton-primaryFormSubmit"] {{
            background-color: {PRIMARY_COLOR};
            border-color: {PRIMARY_COLOR};
        }}
        .stButton > button[kind="primary"]:hover,
        .stFormSubmitButton > button[kind="primary"]:hover,
        [data-testid="stBaseButton-primary"]:hover,
        [data-testid="stBaseButton-primaryFormSubmit"]:hover {{
            background-color: #275e86;
            border-color: #275e86;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ─── منوی ناوبری کناری ────────────────────────────────────────
def show_sidebar() -> str:
    """
    منوی کناری را نمایش می‌دهد و صفحه انتخاب‌شده را برمی‌گرداند.
    """
    with st.sidebar:
        st.markdown("## 👥 ClientFlow CRM")
        st.caption("سیستم مدیریت مشتریان")
        st.markdown("---")

        # منوی اصلی
        page = st.radio(
            "صفحه",
            options=["📊 داشبورد", "➕ افزودن مشتری", "👥 لیست مشتریان"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.caption("نسخه ۱.۵.۰")

    return page


# ─── اجرای اصلی برنامه ────────────────────────────────────────
def main():
    """
    تابع اصلی برنامه — صفحه مناسب را بر اساس انتخاب کاربر نمایش می‌دهد.
    """
    apply_custom_style()
    selected_page = show_sidebar()

    # نمایش صفحه انتخاب‌شده
    if selected_page == "📊 داشبورد":
        dashboard.show()
    elif selected_page == "➕ افزودن مشتری":
        add_client.show()
    elif selected_page == "👥 لیست مشتریان":
        client_list.show()


# این شرط تضمین می‌کند main() فقط هنگام اجرای مستقیم فراخوانی شود
if __name__ == "__main__":
    main()
