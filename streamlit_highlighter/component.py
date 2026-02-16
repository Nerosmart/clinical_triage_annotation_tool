import os
import streamlit.components.v1 as components

_component_func = components.declare_component(
    "highlighter",
    path=os.path.join(os.path.dirname(__file__), "frontend")
)

def highlighter(text: str, key=None):
    return _component_func(text=text, key=key, default=None)