import reflex as rx
from app.states.browser_state import BrowserState
from app.components.image_viewer import image_viewer


def breadcrumb_item(part: tuple[str, str]) -> rx.Component:
    """A single breadcrumb item."""
    return rx.el.div(
        rx.el.a(
            part[0],
            on_click=lambda: BrowserState.list_files(part[1]),
            href="#",
            class_name="text-sm font-medium text-gray-500 hover:text-purple-600 transition-colors",
        ),
        rx.icon("chevron-right", class_name="h-4 w-4 text-gray-400"),
        class_name="flex items-center gap-2",
    )


def main_view() -> rx.Component:
    """The main view area for displaying content and breadcrumbs."""
    return rx.el.main(
        rx.el.header(
            rx.el.nav(
                rx.el.a(
                    rx.icon("home", class_name="h-5 w-5"),
                    on_click=lambda: BrowserState.list_files("."),
                    href="#",
                    class_name="text-gray-500 hover:text-purple-600",
                ),
                rx.icon("chevron-right", class_name="h-4 w-4 text-gray-400"),
                rx.foreach(BrowserState.path_parts, breadcrumb_item),
                class_name="flex items-center gap-2 flex-wrap",
            ),
            class_name="bg-white border-b border-gray-200 p-4 rounded-t-xl",
        ),
        rx.el.div(
            rx.cond(
                BrowserState.image_data_uri,
                image_viewer(
                    rx.image(
                        src=BrowserState.image_data_uri,
                        class_name="max-w-full max-h-full object-contain transition-transform duration-200 ease-in-out",
                        style={
                            "transform": f"translate({BrowserState.image_pos_x}px, {BrowserState.image_pos_y}px) scale({BrowserState.image_scale}) rotate({BrowserState.image_rotation}deg)"
                        },
                        draggable=False,
                    ),
                    on_wheel=BrowserState.handle_wheel,
                    on_mouse_down=BrowserState.handle_mouse_down,
                    on_mouse_up=BrowserState.handle_mouse_up,
                    on_mouse_leave=BrowserState.handle_mouse_up,
                    on_mouse_move=BrowserState.handle_mouse_move,
                    class_name=rx.cond(
                        BrowserState.is_panning,
                        "w-full h-full flex items-center justify-center overflow-hidden p-4 cursor-grabbing",
                        "w-full h-full flex items-center justify-center overflow-hidden p-4 cursor-grab",
                    ),
                ),
                rx.el.div(
                    rx.icon("image-plus", class_name="h-16 w-16 text-gray-300"),
                    rx.el.h3(
                        "Select a PNG file",
                        class_name="text-xl font-semibold text-gray-500",
                    ),
                    rx.el.p(
                        "Choose a file from the list on the left to view it.",
                        class_name="text-gray-400",
                    ),
                    class_name="flex flex-col items-center justify-center h-full gap-4 text-center p-8",
                ),
            ),
            class_name="flex-1 bg-gray-50 rounded-b-xl relative",
        ),
        rx.cond(
            BrowserState.selected_file,
            rx.el.div(
                rx.el.button(
                    rx.icon("zoom-out", class_name="h-5 w-5"),
                    on_click=BrowserState.zoom_out,
                    class_name="p-2 bg-white border border-gray-300 rounded-md text-gray-700 hover:bg-gray-100 shadow-sm transition-colors",
                ),
                rx.el.button(
                    rx.icon("zoom-in", class_name="h-5 w-5"),
                    on_click=BrowserState.zoom_in,
                    class_name="p-2 bg-white border border-gray-300 rounded-md text-gray-700 hover:bg-gray-100 shadow-sm transition-colors",
                ),
                rx.el.div(class_name="w-px bg-gray-300 h-6"),
                rx.el.button(
                    rx.icon("rotate-ccw", class_name="h-5 w-5"),
                    on_click=BrowserState.rotate_left,
                    class_name="p-2 bg-white border border-gray-300 rounded-md text-gray-700 hover:bg-gray-100 shadow-sm transition-colors",
                ),
                rx.el.button(
                    rx.icon("rotate-cw", class_name="h-5 w-5"),
                    on_click=BrowserState.rotate_right,
                    class_name="p-2 bg-white border border-gray-300 rounded-md text-gray-700 hover:bg-gray-100 shadow-sm transition-colors",
                ),
                rx.el.div(class_name="w-px bg-gray-300 h-6"),
                rx.el.button(
                    rx.icon("refresh-cw", class_name="h-5 w-5"),
                    on_click=BrowserState.reset_view,
                    class_name="p-2 bg-white border border-gray-300 rounded-md text-gray-700 hover:bg-gray-100 shadow-sm transition-colors",
                ),
                class_name="absolute bottom-8 right-1/2 translate-x-1/2 z-10 flex items-center gap-2 p-1.5 bg-white rounded-lg shadow-md border border-gray-200",
            ),
        ),
        class_name="flex-1 flex flex-col m-4 bg-white rounded-xl shadow-sm border border-gray-200",
    )