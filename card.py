"""
==============================================================
card.py

کارت استاندارد برنامه

تمام GroupBox های برنامه از این کلاس استفاده می‌کنند.

Author:
Hamed Tirandaz
==============================================================
"""

from PySide6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QLabel,
    QWidget,
)


class Card(QGroupBox):
    """
    کارت استاندارد برنامه
    """

    def __init__(
        self,
        title: str = "",
        parent=None
    ):

        super().__init__(title, parent)

        self._layout = QVBoxLayout()

        self._layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        self._layout.setSpacing(12)

        self.setLayout(self._layout)

    # -------------------------------------------------

    def add_widget(
        self,
        widget: QWidget
    ):

        self._layout.addWidget(widget)

        return widget

    # -------------------------------------------------

    def add_layout(
        self,
        layout
    ):

        self._layout.addLayout(layout)

        return layout

    # -------------------------------------------------

    def add_spacing(
        self,
        value=10
    ):

        self._layout.addSpacing(value)

    # -------------------------------------------------

    def add_stretch(self):

        self._layout.addStretch()