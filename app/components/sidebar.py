import reflex as rx
from app.states.browser_state import BrowserState, FileItem


def file_list_item(item: FileItem) -> rx.Component:
    """A component to display a single file in the list."""
    return rx.el.div(
        rx.el.a(
            rx.image(
                src="/placeholder.svg", class_name="h-10 w-10 rounded-md object-cover"
            ),
            rx.el.div(
                rx.el.p(
                    item["name"],
                    class_name="text-sm font-medium text-gray-800 truncate",
                ),
                class_name="flex-1 min-w-0",
            ),
            on_click=lambda: BrowserState.select_file(item["path"]),
            href="#",
            class_name="flex items-center gap-3 w-full p-2 rounded-lg transition-colors duration-200",
        ),
        class_name=rx.cond(
            BrowserState.selected_file == item["path"],
            "bg-purple-100 border-l-4 border-purple-500",
            "hover:bg-gray-100",
        ),
    )


def directory_list_item(item: FileItem) -> rx.Component:
    """A component to display a single directory in the list."""
    return rx.el.a(
        rx.icon("folder", class_name="h-5 w-5 text-purple-600"),
        rx.el.span(item["name"], class_name="text-sm font-medium text-gray-700"),
        on_click=lambda: BrowserState.list_files(item["path"]),
        href="#",
        class_name="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200",
    )


def sidebar() -> rx.Component:
    """The sidebar component for file and directory navigation."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("image", class_name="h-8 w-8 text-purple-600"),
                rx.el.h2("PNG Browser", class_name="text-xl font-bold text-gray-800"),
                class_name="flex items-center gap-3 p-4 border-b border-gray-200",
            ),
            rx.el.div(
                rx.el.h3(
                    "Folders",
                    class_name="px-4 pt-4 pb-2 text-xs font-semibold uppercase text-gray-500",
                ),
                rx.el.nav(
                    rx.foreach(BrowserState.directories, directory_list_item),
                    class_name="flex flex-col gap-1 px-4",
                ),
                rx.el.h3(
                    "PNG Files",
                    class_name="px-4 pt-6 pb-2 text-xs font-semibold uppercase text-gray-500",
                ),
                rx.el.nav(
                    rx.foreach(BrowserState.png_files, file_list_item),
                    class_name="flex flex-col gap-1 px-4",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="w-80 h-screen bg-white border-r border-gray-200 shadow-sm flex-shrink-0",
    )