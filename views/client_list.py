"""
client_list.py — صفحه لیست مشتریان
شامل: نمایش جدول، جستجو، ویرایش و حذف
"""

import pandas as pd
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
    """صفحه اصلی لیست مشتریان"""
    page_header("لیست مشتریان", "مشاهده، جستجو، ویرایش و حذف مشتریان")

    service = ClientService()

    with st.container(border=True):
        # ─── نوار جستجو ───────────────────────────────────────
        search_query = st.text_input(
            "جستجو",
            placeholder="🔍  نام، شماره تماس یا نوع کسب‌وکار...",
            label_visibility="collapsed",
        )

        clients = service.search_clients(search_query) if search_query else service.get_all_clients()
        st.caption(f"تعداد مشتریان: {len(clients)}")

        if not clients:
            st.info("هیچ مشتری‌ای یافت نشد." if search_query else "هنوز مشتری‌ای ثبت نشده.")
            return

        # ─── جدول st.dataframe ────────────────────────────────
        status_icon = {"فعال": "🟢 فعال", "غیرفعال": "🔴 غیرفعال", "در انتظار": "🟡 در انتظار"}

        rows = []
        for c in clients:
            # ترتیب کلیدها برعکس است تا با direction: rtl ستون «نام» در سمت راست قرار بگیرد
            rows.append({
                "توضیحات": c.notes or "—",
                "وضعیت": status_icon.get(c.status, c.status),
                "نوع کسب‌وکار": c.business_type,
                "ایمیل": c.email or "—",
                "تلفن": c.phone,
                "نام‌خانوادگی": c.last_name,
                "نام": c.first_name,
            })

        df = pd.DataFrame(rows)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "نام": st.column_config.TextColumn("نام", width="small"),
                "نام‌خانوادگی": st.column_config.TextColumn("نام‌خانوادگی", width="small"),
                "تلفن": st.column_config.TextColumn("تلفن", width="medium"),
                "ایمیل": st.column_config.TextColumn("ایمیل", width="medium"),
                "نوع کسب‌وکار": st.column_config.TextColumn("نوع کسب‌وکار", width="medium"),
                "وضعیت": st.column_config.TextColumn("وضعیت", width="small"),
                "توضیحات": st.column_config.TextColumn("توضیحات", width="large"),
            },
        )

    st.write("")  # فاصله بین دو بخش

    with st.container(border=True):
        # ─── بخش عملیات: انتخاب مشتری برای ویرایش یا حذف ─────
        st.subheader("✏️ ویرایش / حذف مشتری")

        # لیست نام‌ها برای انتخاب
        client_names = [f"{c.first_name} {c.last_name} — {c.phone}" for c in clients]
        selected_label = st.selectbox(
            "مشتری مورد نظر را انتخاب کنید:",
            options=["— انتخاب کنید —"] + client_names,
            label_visibility="collapsed",
        )

        if selected_label == "— انتخاب کنید —":
            return

        # پیدا کردن مشتری انتخاب‌شده
        selected_index = client_names.index(selected_label)
        selected_client = clients[selected_index]

        # دکمه‌های عملیات
        col_edit, col_delete, col_empty = st.columns([1, 1, 4])
        edit_clicked = col_edit.button("✏️ ویرایش", use_container_width=True)
        delete_clicked = col_delete.button("🗑️ حذف", use_container_width=True, type="secondary")

        if edit_clicked:
            st.session_state["editing_id"] = selected_client.id
            st.session_state.pop("deleting_id", None)

        if delete_clicked:
            st.session_state["deleting_id"] = selected_client.id
            st.session_state.pop("editing_id", None)

        # ─── فرم ویرایش ───────────────────────────────────────
        if st.session_state.get("editing_id") == selected_client.id:
            _show_edit_form(selected_client, service)

        # ─── تأیید حذف ──────────────────────────────────────────
        if st.session_state.get("deleting_id") == selected_client.id:
            _show_delete_confirm(selected_client, service)


def _show_edit_form(client: Client, service: ClientService):
    """فرم ویرایش اطلاعات مشتری"""
    st.markdown("---")
    st.subheader(f"ویرایش: {client.full_name}")

    with st.form(f"edit_form_{client.id}"):
        col1, col2 = st.columns(2)
        with col1:
            new_first = st.text_input("نام", value=client.first_name)
        with col2:
            new_last = st.text_input("نام‌خانوادگی", value=client.last_name)

        col3, col4 = st.columns(2)
        with col3:
            new_phone = st.text_input("تلفن", value=client.phone)
        with col4:
            new_email = st.text_input("ایمیل", value=client.email)

        col5, col6 = st.columns(2)
        with col5:
            new_business = st.selectbox(
                "نوع کسب‌وکار",
                options=Client.BUSINESS_TYPES,
                index=Client.BUSINESS_TYPES.index(client.business_type)
                if client.business_type in Client.BUSINESS_TYPES else 0,
            )
        with col6:
            new_status = st.selectbox(
                "وضعیت",
                options=Client.STATUS_OPTIONS,
                index=Client.STATUS_OPTIONS.index(client.status)
                if client.status in Client.STATUS_OPTIONS else 0,
            )

        new_notes = st.text_area("توضیحات", value=client.notes, height=80)

        save_col, cancel_col = st.columns(2)
        save_btn = save_col.form_submit_button("💾 ذخیره تغییرات", use_container_width=True)
        cancel_btn = cancel_col.form_submit_button("❌ انصراف", use_container_width=True)

    if cancel_btn:
        st.session_state.pop("editing_id", None)
        st.rerun()

    if save_btn:
        errors = []
        if not validate_first_name(new_first):
            errors.append("نام را وارد کنید.")
        elif not validate_persian_only(new_first):
            errors.append("نام باید فارسی باشد.")
        if not validate_last_name(new_last):
            errors.append("نام‌خانوادگی را وارد کنید.")
        elif not validate_persian_only(new_last):
            errors.append("نام‌خانوادگی باید فارسی باشد.")
        if not validate_phone(new_phone):
            errors.append("شماره تماس فقط باید شامل اعداد انگلیسی باشد.")
        if new_email and not validate_email(new_email):
            errors.append("فرمت ایمیل صحیح نیست.")

        if errors:
            for e in errors:
                st.error(f"⚠️ {e}")
        else:
            updated = Client(
                first_name=new_first,
                last_name=new_last,
                phone=new_phone,
                email=new_email,
                business_type=new_business,
                status=new_status,
                notes=new_notes,
                client_id=client.id,
                created_at=client.created_at,
            )
            service.update_client(updated)
            st.session_state.pop("editing_id", None)
            st.success("✅ اطلاعات بروزرسانی شد.")
            st.rerun()


def _show_delete_confirm(client: Client, service: ClientService):
    """دیالوگ تأیید حذف"""
    st.markdown("---")
    st.warning(f"⚠️ آیا از حذف «{client.full_name}» مطمئن هستید؟ این عمل برگشت‌پذیر نیست.")

    col1, col2, _ = st.columns([1, 1, 4])
    if col1.button("🗑️ بله، حذف شود", type="primary", use_container_width=True):
        service.delete_client(client.id)
        st.session_state.pop("deleting_id", None)
        st.success(f"مشتری «{client.full_name}» حذف شد.")
        st.rerun()

    if col2.button("انصراف", use_container_width=True):
        st.session_state.pop("deleting_id", None)
        st.rerun()
