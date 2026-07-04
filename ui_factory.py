"""
==============================================================
ui_factory.py

Factory ساخت Widget های استاندارد برنامه

تمام صفحات Wizard باید Widget های خود را
از طریق این کلاس ایجاد کنند.

Author:
Hamed Tirandaz
==============================================================
"""

from __future__ import annotations

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (

    QLabel,

    QWidget,

    QFrame,

    QGroupBox,

    QVBoxLayout,

    QHBoxLayout,

    QFormLayout,

    QPushButton,

    QSizePolicy,

    QSpacerItem,

    QProgressBar,

)

# ==========================================================
# UI Factory
# ==========================================================


class UIFactory:
    """
    Factory ساخت تمام Widget های مشترک برنامه
    """

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):
        pass

    # ======================================================
    # Labels
    # ======================================================

    @staticmethod
    def title(text: str) -> QLabel:
        """
        عنوان اصلی صفحه
        """

        label = QLabel(text)

        label.setObjectName("pageTitle")

        label.setWordWrap(True)

        return label

    @staticmethod
    def subtitle(text: str) -> QLabel:
        """
        زیرعنوان صفحه
        """

        label = QLabel(text)

        label.setObjectName("pageSubtitle")

        label.setWordWrap(True)

        return label

    @staticmethod
    def description(text: str) -> QLabel:
        """
        توضیحات صفحه
        """

        label = QLabel(text)

        label.setObjectName("pageDescription")

        label.setWordWrap(True)

        label.setTextFormat(Qt.RichText)

        return label

    @staticmethod
    def status(text="Ready") -> QLabel:
        """
        Status Label
        """

        label = QLabel(text)

        label.setObjectName("pageStatus")

        return label

    # ======================================================
    # Separator
    # ======================================================

    @staticmethod
    def separator() -> QFrame:
        """
        ایجاد خط جداکننده
        """

        line = QFrame()

        line.setFrameShape(QFrame.HLine)

        line.setFrameShadow(QFrame.Sunken)

        return line

    # ======================================================
    # Spacer
    # ======================================================

    @staticmethod
    def spacer(height: int = 10):
        """
        فاصله عمودی
        """

        return QSpacerItem(

            0,

            height,

            QSizePolicy.Minimum,

            QSizePolicy.Fixed

        )

    # ======================================================
    # Stretch
    # ======================================================

    @staticmethod
    def stretch(layout):

        layout.addStretch()

        return layout


    # ======================================================
    # Layouts
    # ======================================================

    @staticmethod
    def v_layout(
        spacing: int = 12,
        margins=(0, 0, 0, 0)
    ) -> QVBoxLayout:
        """
        ایجاد QVBoxLayout استاندارد
        """

        layout = QVBoxLayout()

        layout.setSpacing(spacing)

        layout.setContentsMargins(*margins)

        return layout

    @staticmethod
    def h_layout(
        spacing: int = 10,
        margins=(0, 0, 0, 0)
    ) -> QHBoxLayout:
        """
        ایجاد QHBoxLayout استاندارد
        """

        layout = QHBoxLayout()

        layout.setSpacing(spacing)

        layout.setContentsMargins(*margins)

        return layout

    # ======================================================
    # Form
    # ======================================================

    @staticmethod
    def form() -> QFormLayout:
        """
        ایجاد فرم استاندارد
        """

        form = QFormLayout()

        form.setContentsMargins(0, 0, 0, 0)

        form.setHorizontalSpacing(20)

        form.setVerticalSpacing(12)

        return form

    # ======================================================
    # Card
    # ======================================================

    @staticmethod
    def card(
        title: str,
        flat: bool = False
    ) -> QGroupBox:
        """
        ایجاد کارت استاندارد برنامه
        """

        group = QGroupBox(title)

        group.setFlat(flat)

        layout = UIFactory.v_layout(
            spacing=12,
            margins=(15, 15, 15, 15)
        )

        group.setLayout(layout)

        return group

    # ======================================================
    # Button Row
    # ======================================================

    @staticmethod
    def button_row(
        *buttons: QPushButton,
        align_right: bool = True
    ) -> QHBoxLayout:
        """
        ایجاد ردیف دکمه‌ها
        """

        row = UIFactory.h_layout()

        if align_right:
            row.addStretch()

        for button in buttons:
            row.addWidget(button)

        return row

    # ======================================================
    # Progress
    # ======================================================

    @staticmethod
    def progress() -> QProgressBar:
        """
        ProgressBar استاندارد
        """

        bar = QProgressBar()

        bar.setVisible(False)

        # Busy Indicator
        bar.setRange(0, 0)

        bar.setFixedWidth(180)

        return bar

    # ======================================================
    # Helpers
    # ======================================================

    @staticmethod
    def add_widget(layout, widget: QWidget):
        """
        اضافه کردن Widget به Layout
        """

        layout.addWidget(widget)

        return widget

    @staticmethod
    def add_layout(layout, child_layout):
        """
        اضافه کردن Layout به Layout
        """

        layout.addLayout(child_layout)

        return child_layout

    @staticmethod
    def add_spacing(layout, value: int = 10):
        """
        ایجاد فاصله
        """

        layout.addSpacing(value)

    @staticmethod
    def add_stretch(layout):
        """
        ایجاد Stretch
        """

        layout.addStretch()

    # ======================================================
    # Common Widgets
    # ======================================================

    @staticmethod
    def label(
        text: str = "",
        rich_text: bool = False,
        word_wrap: bool = True
    ) -> QLabel:
        """
        QLabel استاندارد
        """

        lbl = QLabel(text)

        lbl.setWordWrap(word_wrap)

        if rich_text:
            lbl.setTextFormat(Qt.RichText)

        return lbl

    @staticmethod
    def section(title: str):
        """
        ایجاد Section استاندارد
        """

        group = UIFactory.card(title)

        return group

    # ======================================================
    # Utilities
    # ======================================================

    @staticmethod
    def clear_layout(layout):
        """
        حذف تمام Widget های Layout
        """

        while layout.count():

            item = layout.takeAt(0)

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

            elif item.layout():

                UIFactory.clear_layout(item.layout())

    # ======================================================
    # Page Builder
    # ======================================================

    @staticmethod
    def page_layout(parent=None):
        """
        Layout استاندارد صفحات Wizard
        """

        layout = QVBoxLayout(parent)

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        layout.setSpacing(18)

        return layout