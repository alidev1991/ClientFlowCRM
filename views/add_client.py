"""
add_client.py — صفحه افزودن مشتری جدید
"""

import streamlit as st
from models.client import Client
from services.client_service import ClientService
from utils.helpers import (
    page_header,
    validate_first_name,
    validate_last_name,
    validate_persian_only,
    validate_phone,
    validate_email,
)


def show():
    """صفحه افزودن مشتری جدید را نمایش می‌دهد."""
    page_header("افزودن مشتری جدید", "اطلاعات مشتری را با دقت وارد کنید")

    service = ClientService()

    st.caption("فیلدهای ستاره‌دار ( * ) اجباری هستند.")

    _, form_col, _ = st.columns([1, 3, 1])

    with form_col:
        with st.form("add_client_form", clear_on_submit=True):

            with st.container(border=True):
                st.subheader("📋 اطلاعات پایه")

                # ردیف اول: نام و نام‌خانوادگی جداگانه
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("نام *", placeholder="مثال: علی")
                with col2:
                    last_name = st.text_input("نام‌خانوادگی *", placeholder="مثال: احمدی")

                # ردیف دوم: تلفن و ایمیل
                col3, col4 = st.columns(2)
                with col3:
                    phone = st.text_input(
                        "شماره تماس *",
                        placeholder="مثال: 09121234567",
                        help="فقط اعداد انگلیسی وارد شود"
                    )
                with col4:
                    email = st.text_input("ایمیل", placeholder="مثال: ali@example.com")

                # ردیف سوم: نوع کسب‌وکار و وضعیت
                col5, col6 = st.columns(2)
                with col5:
                    business_type = st.selectbox("نوع کسب‌وکار *", options=Client.BUSINESS_TYPES)
                with col6:
                    status = st.selectbox("وضعیت", options=Client.STATUS_OPTIONS)

            st.write("")  # فاصله بین دو بخش

            with st.container(border=True):
                st.subheader("📝 توضیحات")
                notes = st.text_area(
                    "توضیحات (اختیاری)",
                    placeholder="هر نکته‌ای درباره این مشتری...",
                    height=100,
                    label_visibility="collapsed",
                )

            st.write("")
            submitted = st.form_submit_button("✅ ثبت مشتری", use_container_width=True, type="primary")

    if submitted:
        _process_form(service, first_name, last_name, phone, email, business_type, status, notes)


def _process_form(service, first_name, last_name, phone, email, business_type, status, notes):
    """اعتبارسنجی و ذخیره داده‌های فرم."""
    errors = []

    # ── اعتبارسنجی نام ──────────────────────────────────────
    if not validate_first_name(first_name):
        errors.append("نام را وارد کنید (حداقل ۲ حرف).")
    elif not validate_persian_only(first_name):
        errors.append("نام باید فارسی باشد. از حروف انگلیسی استفاده نکنید.")

    # ── اعتبارسنجی نام‌خانوادگی ─────────────────────────────
    if not validate_last_name(last_name):
        errors.append("نام‌خانوادگی را وارد کنید (حداقل ۲ حرف).")
    elif not validate_persian_only(last_name):
        errors.append("نام‌خانوادگی باید فارسی باشد. از حروف انگلیسی استفاده نکنید.")

    # ── اعتبارسنجی تلفن ─────────────────────────────────────
    if not phone.strip():
        errors.append("شماره تماس را وارد کنید.")
    elif not validate_phone(phone):
        errors.append("شماره تماس فقط باید شامل اعداد انگلیسی (0-9) باشد.")

    # ── اعتبارسنجی ایمیل ────────────────────────────────────
    if email and not validate_email(email):
        errors.append("فرمت ایمیل صحیح نیست.")

    # نمایش خطاها
    if errors:
        for error in errors:
            st.error(f"⚠️ {error}")
        return

    # ساخت و ذخیره مشتری
    new_client = Client(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        business_type=business_type,
        status=status,
        notes=notes,
    )

    if service.add_client(new_client):
        st.success(f"✅ مشتری «{new_client.full_name}» با موفقیت ثبت شد.")
        st.balloons()
    else:
        st.error("خطا در ذخیره‌سازی. لطفاً دوباره تلاش کنید.")
