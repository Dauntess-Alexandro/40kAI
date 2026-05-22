"""One-off patch script for viewer app.py GUI migration."""
from __future__ import annotations

import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "app" / "viewer" / "app.py"
text = p.read_text(encoding="utf-8")

repls = [
    ("self.command_prompt.setText", "self._set_command_prompt"),
    ("self.command_hint.setText", "self._set_command_hint"),
    ("self.shoot_popover_dice_input.text()", "self._shoot_dice_input_text"),
    ("self.shoot_popover_dice_input.clear()", "self._shoot_dice_input_text = \"\""),
    ("self.command_input.text()", "self._last_command_text"),
    ("self.command_input.clear()", "self._last_command_text = \"\""),
    ("self.choice_combo.currentText()", "self._last_choice_text"),
    ("self.int_spin.value()", "self._int_spin_value"),
]
for a, b in repls:
    text = text.replace(a, b)

for pat in [
    r"\s*self\.command_stack\.setEnabled\([^\n]+\n",
    r"\s*self\.command_stack\.setVisible\([^\n]+\n",
    r"\s*self\.command_stack\.setCurrentIndex\([^\n]+\n",
    r"\s*self\.command_input\.setPlaceholderText\([^\n]+\n",
    r"\s*self\.int_spin\.setRange\([^\n]+\n",
    r"\s*self\.int_spin\.setValue\([^\n]+\n",
    r"\s*self\.choice_combo\.addItems\([^\n]+\n",
]:
    text = re.sub(pat, "", text)

p.write_text(text, encoding="utf-8")
print("patched", p)
