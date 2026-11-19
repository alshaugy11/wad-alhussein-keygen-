import hashlib
import flet as ft

# يجب أن يكون هذا المفتاح مطابقاً تماماً للموجود في ملف logic/license_manager.py
SECRET_KEY = "WadAlHussein_Secure_2024"


def generate_activation_code(machine_id: str, days: int) -> str:
    # دمج معرف الجهاز مع عدد الأيام قبل التشفير
    raw = f"{machine_id}-{days}-{SECRET_KEY}"
    return hashlib.sha256(raw.encode()).hexdigest()[:12].upper()


def main(page: ft.Page):
    page.title = "مولد أكواد التفعيل - مطعم ود الحسين"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.AMBER)
    page.padding = 20
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    machine_id_field = ft.TextField(
        label="معرف الجهاز (Machine ID)",
        hint_text="أدخل المعرف الذي أرسله الزبون...",
        prefix_icon=ft.Icons.DEVICES,
        border_radius=12,
        text_align=ft.TextAlign.LEFT,
        capitalization=ft.TextCapitalization.CHARACTERS,
    )

    days_field = ft.TextField(
        label="مدة التفعيل (بالأيام)",
        value="30",
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix_icon=ft.Icons.CALENDAR_MONTH,
        border_radius=12,
        text_align=ft.TextAlign.CENTER,
    )

    result_text = ft.Text(
        value="---- ---- ----",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.AMBER_400,
        selectable=True,
    )

    def show_snack(message: str, bgcolor: str = ft.Colors.GREEN_700):
        snack = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=bgcolor,
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def set_days(days_val: int):
        days_field.value = str(days_val)
        page.update()

    quick_days_row = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True,
        controls=[
            ft.OutlinedButton("شهر (30)", on_click=lambda _: set_days(30)),
            ft.OutlinedButton("سنة (365)", on_click=lambda _: set_days(365)),
            ft.OutlinedButton("دائم (3650)", on_click=lambda _: set_days(3650)),
        ],
    )

    def on_generate_click(e):
        m_id = (machine_id_field.value or "").strip().upper()
        d_str = (days_field.value or "").strip()

        if not m_id:
            show_snack("❌ الرجاء إدخال معرف الجهاز أولاً!", ft.Colors.RED_700)
            return

        if not d_str.isdigit() or int(d_str) <= 0:
            show_snack("❌ الرجاء إدخال عدد أيام صحيح!", ft.Colors.RED_700)
            return

        days = int(d_str)
        code = generate_activation_code(m_id, days)
        result_text.value = code
        result_card.visible = True
        page.update()

    def copy_code(e):
        if result_text.value != "---- ---- ----":
            page.set_clipboard(result_text.value)
            show_snack("✅ تم نسخ كود التفعيل بنجاح!")

    result_card = ft.Container(
        visible=False,
        padding=20,
        border_radius=15,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        border=ft.border.all(1, ft.Colors.AMBER_700),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            controls=[
                ft.Text("كود التفعيل جاهز:", size=14, color=ft.Colors.GREY_400),
                result_text,
                ft.ElevatedButton(
                    content=ft.Text("نسخ الكود"),
                    icon=ft.Icons.COPY,
                    on_click=copy_code,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.AMBER_700,
                        color=ft.Colors.BLACK,
                    ),
                ),
            ],
        ),
    )

    main_card = ft.Container(
        width=400,
        padding=25,
        border_radius=20,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                ft.Icon(ft.Icons.RESTAURANT_MENU, size=50, color=ft.Colors.AMBER_400),
                ft.Text("مطعم ود الحسين", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("نظام توليد أكواد التفعيل", size=14, color=ft.Colors.GREY_400),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                machine_id_field,
                days_field,
                quick_days_row,
                ft.FilledButton(
                    content=ft.Text("توليد كود التفعيل"),
                    icon=ft.Icons.VPN_KEY,
                    width=350,
                    height=50,
                    on_click=on_generate_click,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                    ),
                ),
                result_card,
            ],
        ),
    )

    page.add(ft.SafeArea(content=main_card))


if __name__ == "__main__":
    ft.app(target=main)
