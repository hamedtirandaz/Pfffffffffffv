"""
==============================================================
base_page.py

کلاس پایه تمام صفحات Wizard

تمام صفحات پروژه از این کلاس ارث‌بری می‌کنند.

وظایف این کلاس:

✔ ساخت Header
✔ ساخت Title
✔ ساخت Description
✔ ساخت Body
✔ ساخت Footer Status
✔ متدهای کمکی برای ساخت صفحات

Author:
Hamed Tirandaz
==============================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (

    QLabel,

    QWidget,

    QWizardPage,

    QVBoxLayout,

    QHBoxLayout,

    QSizePolicy,

    QSpacerItem,

    QFrame,

    QGroupBox,

    QFormLayout,

    QPushButton,

    QProgressBar,

)

# ==========================================================
# Base Page
# ==========================================================


class BasePage(QWizardPage, ABC):

    """
    کلاس پایه تمام صفحات Wizard

    هر صفحه فقط باید build_body()
    را پیاده‌سازی کند.
    """

    # ------------------------------------------------------
    # Override در کلاس فرزند
    # ------------------------------------------------------

    TITLE = ""

    DESCRIPTION = ""

    SUBTITLE = ""

    # ------------------------------------------------------

    def __init__(self, parent=None):

        super().__init__(parent)

        self.main_layout = None

        self.body_layout = None

        self.status_label = None

        self.progress = None

        self._build_ui()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(self):

        """
        ساخت ساختار اصلی صفحه
        """

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(

            24,

            24,

            24,

            24

        )

        self.main_layout.setSpacing(

            18

        )

        # ---------------------------------------------
        # Header
        # ---------------------------------------------

        self._build_header()

        # ---------------------------------------------
        # Body
        # ---------------------------------------------

        self.body_layout = QVBoxLayout()

        self.body_layout.setSpacing(

            14

        )

        self.main_layout.addLayout(

            self.body_layout

        )

        # صفحه فرزند اینجا ویجت‌های خودش را ایجاد می‌کند

        self.build_body()

        self.main_layout.addStretch()

        # ---------------------------------------------
        # Footer
        # ---------------------------------------------

        self._build_footer()

    # ======================================================
    # Header
    # ======================================================

    def _build_header(self):
        """
        ساخت Header صفحه
        """

        # -----------------------------
        # Title
        # -----------------------------

        if self.TITLE:

            title = QLabel(self.TITLE)

            title.setObjectName("pageTitle")

            title.setWordWrap(True)

            self.main_layout.addWidget(title)

        # -----------------------------
        # Subtitle
        # -----------------------------

        if self.SUBTITLE:

            subtitle = QLabel(self.SUBTITLE)

            subtitle.setObjectName("pageSubtitle")

            subtitle.setWordWrap(True)

            self.main_layout.addWidget(subtitle)

        # -----------------------------
        # Description
        # -----------------------------

        if self.DESCRIPTION:

            description = QLabel(self.DESCRIPTION)

            description.setObjectName("pageDescription")

            description.setWordWrap(True)

            description.setTextFormat(Qt.RichText)

            self.main_layout.addWidget(description)

        # -----------------------------
        # Separator
        # -----------------------------

        line = QFrame()

        line.setFrameShape(QFrame.HLine)

        line.setFrameShadow(QFrame.Sunken)

        self.main_layout.addWidget(line)

    # ======================================================
    # Footer
    # ======================================================

    def _build_footer(self):
        """
        Footer صفحه
        """

        footer = QHBoxLayout()

        footer.setSpacing(10)

        # -----------------------------
        # Status
        # -----------------------------

        self.status_label = QLabel("Ready")

        self.status_label.setObjectName("pageStatus")

        footer.addWidget(self.status_label)

        footer.addStretch()

        # -----------------------------
        # Progress
        # -----------------------------

        self.progress = QProgressBar()

        self.progress.setVisible(False)

        self.progress.setFixedWidth(180)

        self.progress.setRange(0, 0)

        footer.addWidget(self.progress)

        self.main_layout.addLayout(footer)

    # ======================================================
    # Override
    # ======================================================

    @abstractmethod
    def build_body(self):
        """
        این متد باید در کلاس فرزند
        پیاده‌سازی شود.
        """
        ...

    # ======================================================
    # Status
    # ======================================================

    def set_status(self, text: str):

        self.status_label.setText(text)

    def clear_status(self):

        self.status_label.setText("Ready")

    # ======================================================
    # Progress
    # ======================================================

    def show_busy(self, text="Working..."):

        self.set_status(text)

        self.progress.setVisible(True)

    def hide_busy(self):

        self.progress.setVisible(False)

        self.clear_status()

    # ======================================================
    # Message Helpers
    # ======================================================

    def show_success(self, text):

        self.progress.setVisible(False)

        self.status_label.setText(f"✅ {text}")

    def show_error(self, text):

        self.progress.setVisible(False)

        self.status_label.setText(f"❌ {text}")

    def show_warning(self, text):

        self.progress.setVisible(False)

        self.status_label.setText(f"⚠ {text}")

    def show_info(self, text):

        self.progress.setVisible(False)

        self.status_label.setText(text)


    # ======================================================
    # Layout Helpers
    # ======================================================

    def add_widget(self, widget: QWidget):
        """
        اضافه کردن یک ویجت به بدنه صفحه
        """
        self.body_layout.addWidget(widget)

        return widget

    def add_layout(self, layout):
        """
        اضافه کردن Layout به بدنه صفحه
        """
        self.body_layout.addLayout(layout)

        return layout

    def add_spacing(self, value: int = 10):
        """
        ایجاد فاصله عمودی
        """
        self.body_layout.addSpacing(value)

    def add_stretch(self):
        """
        اضافه کردن Stretch
        """
        self.body_layout.addStretch()

    def add_separator(self):
        """
        ایجاد یک خط جداکننده
        """

        line = QFrame()

        line.setFrameShape(QFrame.HLine)

        line.setFrameShadow(QFrame.Sunken)

        self.body_layout.addWidget(line)

        return line

    # ======================================================
    # Widget Factory
    # ======================================================

    def create_group(
        self,
        title: str,
        flat: bool = False
    ) -> QGroupBox:
        """
        ساخت GroupBox استاندارد
        """

        group = QGroupBox(title)

        group.setFlat(flat)

        layout = QVBoxLayout()

        layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        layout.setSpacing(12)

        group.setLayout(layout)

        return group

    def create_form(self) -> QFormLayout:
        """
        ساخت فرم استاندارد
        """

        form = QFormLayout()

        form.setContentsMargins(
            0,
            0,
            0,
            0
        )

        form.setHorizontalSpacing(20)

        form.setVerticalSpacing(12)

        return form

    def create_button_row(
        self,
        *buttons: QPushButton
    ) -> QHBoxLayout:
        """
        ساخت ردیف دکمه‌ها
        """

        row = QHBoxLayout()

        row.addStretch()

        for button in buttons:

            row.addWidget(button)

        return row

    # ======================================================
    # Validation
    # ======================================================

    def validatePage(self) -> bool:
        """
        متد استاندارد QWizard

        در صفحات فرزند Override می‌شود.
        """

        return True

    # ======================================================
    # Initialize
    # ======================================================

    def initializePage(self):
        """
        هنگام ورود به صفحه
        """

        super().initializePage()

    # ======================================================
    # Cleanup
    # ======================================================

    def cleanupPage(self):
        """
        هنگام برگشت از صفحه
        """

        super().cleanupPage()

    # ======================================================
    # Complete
    # ======================================================

    def isComplete(self) -> bool:
        """
        وضعیت تکمیل صفحه
        """

        return True

    # ======================================================
    # Wizard Context
    # ======================================================

    @property
    def context(self):
        """
        دسترسی به Context اصلی Wizard
        """

        wizard = self.wizard()

        if wizard and hasattr(wizard, "context"):

            return wizard.context

        return None

    # ======================================================
    # Config
    # ======================================================

    @property
    def config(self):
        """
        دسترسی به Config برنامه
        """

        wizard = self.wizard()

        if wizard and hasattr(wizard, "config"):

            return wizard.config

        return None