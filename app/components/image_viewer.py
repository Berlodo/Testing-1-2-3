import reflex as rx


class ImageViewer(rx.Component):
    """A custom component to wrap the image and handle various mouse events."""

    library = "react"
    tag = "div"

    def get_event_triggers(self) -> dict[str, rx.event.EventSpec]:
        """Get the event triggers for the component."""
        return {
            **super().get_event_triggers(),
            "on_wheel": lambda e: [e],
            "on_mouse_down": lambda e: [e],
            "on_mouse_up": lambda e: [e],
            "on_mouse_leave": lambda e: [e],
            "on_mouse_move": lambda e: [e],
            "on_mouse_enter": lambda e: [e],
        }


image_viewer = ImageViewer.create