import reflex as rx
from app.components.sidebar import sidebar
from app.components.main_view import main_view
from app.states.browser_state import BrowserState


def index() -> rx.Component:
    return rx.el.main(
        sidebar(),
        main_view(),
        on_mount=BrowserState.on_load,
        class_name="font-['Inter'] flex h-screen bg-gray-100",
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="purple"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")