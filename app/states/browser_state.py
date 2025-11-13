import reflex as rx
from typing import TypedDict
import os
import pathlib
import logging
import base64


class FileItem(TypedDict):
    name: str
    path: str
    is_dir: bool


class BrowserState(rx.State):
    """Manages the state for the file browser."""

    current_path: str = os.path.abspath(".")
    selected_file: str | None = None
    files_and_dirs: list[FileItem] = []
    image_data_uri: str | None = None
    image_scale: float = 1.0
    image_pos_x: int = 0
    image_pos_y: int = 0
    image_rotation: int = 0
    is_panning: bool = False
    pan_start_x: int = 0
    pan_start_y: int = 0

    @rx.var
    def path_parts(self) -> list[tuple[str, str]]:
        """Returns the parts of the current path for breadcrumbs."""
        parts = pathlib.Path(self.current_path).parts
        paths = []
        for i in range(1, len(parts) + 1):
            paths.append((" / ".join(parts[i - 1 : i]), str(pathlib.Path(*parts[:i]))))
        return paths

    @rx.var
    def png_files(self) -> list[FileItem]:
        """Filters for PNG files only."""
        return [
            item
            for item in self.files_and_dirs
            if not item["is_dir"] and item["name"].lower().endswith(".png")
        ]

    @rx.var
    def directories(self) -> list[FileItem]:
        """Filters for directories only."""
        return [item for item in self.files_and_dirs if item["is_dir"]]

    @rx.event
    def on_load(self):
        """Load the file list for the current path on page load."""
        return BrowserState.list_files(self.current_path)

    @rx.event
    def list_files(self, path: str):
        """Lists files and directories at a given path."""
        try:
            if not os.path.isdir(path):
                path = os.path.dirname(path)
            self.current_path = os.path.abspath(path)
            items: list[FileItem] = []
            for item_name in sorted(os.listdir(self.current_path)):
                item_path = os.path.join(self.current_path, item_name)
                if os.path.isdir(item_path):
                    items.append({"name": item_name, "path": item_path, "is_dir": True})
                elif item_name.lower().endswith(".png"):
                    items.append(
                        {"name": item_name, "path": item_path, "is_dir": False}
                    )
            self.files_and_dirs = items
            self.selected_file = None
        except PermissionError as e:
            logging.exception(f"Permission denied: {e}")
            yield rx.toast("Permission denied.", duration=3000)
        except Exception as e:
            logging.exception(f"Error listing files: {e}")
            yield rx.toast(f"An unexpected error occurred: {e}", duration=3000)

    @rx.event
    def select_file(self, file_path: str):
        """Selects a file, reads it, and prepares it for display."""
        try:
            self.selected_file = file_path
            with open(file_path, "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode("utf-8")
                self.image_data_uri = f"data:image/png;base64,{encoded_string}"
            self.image_scale = 1.0
            self.image_pos_x = 0
            self.image_pos_y = 0
            self.image_rotation = 0
        except Exception as e:
            logging.exception(f"Error selecting or reading file: {e}")
            self.selected_file = None
            self.image_data_uri = None
            yield rx.toast("Could not read the selected file.", duration=3000)

    @rx.event
    def reset_view(self):
        """Resets image zoom, pan, and rotation."""
        self.image_scale = 1.0
        self.image_pos_x = 0
        self.image_pos_y = 0
        self.image_rotation = 0

    @rx.event
    def handle_wheel(self, event: dict):
        """Handles mouse wheel events for zooming."""
        delta = event["deltaY"]
        self.image_scale = max(0.1, self.image_scale - delta * 0.01)
        return rx.call_script("event.preventDefault()")

    @rx.event
    def handle_mouse_down(self, event: dict):
        """Handles mouse down events to start panning."""
        self.is_panning = True
        self.pan_start_x = event["clientX"] - self.image_pos_x
        self.pan_start_y = event["clientY"] - self.image_pos_y

    @rx.event
    def handle_mouse_up(self):
        """Handles mouse up events to stop panning."""
        self.is_panning = False

    @rx.event
    def handle_mouse_move(self, event: dict):
        """Handles mouse move events to pan the image."""
        if self.is_panning:
            self.image_pos_x = event["clientX"] - self.pan_start_x
            self.image_pos_y = event["clientY"] - self.pan_start_y

    @rx.event
    def rotate_left(self):
        """Rotates the image to the left."""
        self.image_rotation -= 90

    @rx.event
    def rotate_right(self):
        """Rotates the image to the right."""
        self.image_rotation += 90

    @rx.event
    def zoom_in(self):
        """Zooms in on the image."""
        self.image_scale = min(5.0, self.image_scale + 0.1)

    @rx.event
    def zoom_out(self):
        """Zooms out of the image."""
        self.image_scale = max(0.1, self.image_scale - 0.1)