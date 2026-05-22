from pathlib import Path

p = Path(r"C:\40kAI\app\viewer\app.py")
text = p.read_text(encoding="utf-8")
start = text.index("    def _on_shoot_dice_input_changed")
end = text.index("    def _cancel_shoot_sequence")
new = '''    def _on_shoot_dice_input_changed(self, _text: str) -> None:
        self._update_shoot_input_feedback()

    def _update_shoot_input_feedback(self) -> None:
        if not self._shoot_resolver_active:
            return
        vc = self.viewer_controller
        req = self._pending_request
        stage = self._resolve_shoot_stage(req)
        expects_dice = bool(getattr(req, "kind", "") == "dice" and stage in {"hit", "wound", "save"})
        if not expects_dice:
            vc.update_shoot_ui(dice_counter="0/0", info_text="ℹ На этом шаге ввод кубов не требуется", needs_dice=False)
            return
        count = int(getattr(req, "count", 0) or 0)
        min_v = int(getattr(req, "min_value", 1) or 1)
        max_v = int(getattr(req, "max_value", 6) or 6)
        lock_suffix = ""
        if self._is_shooting_dice_request(req) and self._shoot_locked_target_id is not None:
            lock_suffix = f" • Цель Unit {int(self._shoot_locked_target_id)} зафиксирована"
        entered, has_error, has_tokens = self._count_dice_tokens(
            self._shoot_dice_input_text, min_value=min_v, max_value=max_v
        )
        info = ""
        if has_error:
            info = f"⚠ Только цифры {min_v}–{max_v}: «1 2 3» или слитно «123»"
        elif count <= 0:
            info = f"ℹ Движок не запросил количество кубов{lock_suffix}"
        elif entered < count:
            rest = count - entered
            info = f"ℹ Нужно: {count} d6 • Осталось: {rest}{lock_suffix}" if has_tokens else f"ℹ Нужно: {count} d6{lock_suffix}"
        elif entered > count:
            info = f"⚠ Лишних: {entered - count}. Нужно ровно {count}{lock_suffix}"
        else:
            info = f"ℹ Готово к броску{lock_suffix}"
        vc.update_shoot_ui(dice_counter=f"{entered}/{count}", info_text=info, needs_dice=True)

    def _parse_popover_dice_values(self, request) -> Optional[list[int]]:
        count = int(getattr(request, "count", 0) or 0)
        min_value = int(getattr(request, "min_value", 1) or 1)
        max_value = int(getattr(request, "max_value", 6) or 6)
        raw = self._shoot_dice_input_text.strip()
        if not raw:
            self.viewer_controller.update_shoot_ui(info_text=f"ℹ Нужно: {count} значений d6")
            return None
        try:
            return parse_dice_values(raw, count=count, min_value=min_value, max_value=max_value)
        except ValueError as exc:
            self.viewer_controller.update_shoot_ui(info_text=f"⚠ Ошибка ввода: {exc}")
            return None

    def _update_shoot_popover_ui(self) -> None:
        if not self._shoot_resolver_active or self._shoot_popover_target_id is None:
            self.viewer_controller.set_shoot_popover_open(False)
            return
        attacker = self._shoot_resolver_attacker_id
        request = self._pending_request
        locked_target = self._shoot_locked_target_id
        if self._is_shooting_dice_request(request) and locked_target is not None:
            target = int(locked_target)
            self._shoot_popover_target_id = int(locked_target)
        else:
            target = int(self._shoot_popover_target_id)
        if self._is_shooting_dice_request(request):
            req_target = self._shoot_request_target_id
            if req_target is not None and int(target) != int(req_target):
                self._close_shoot_popover(reset_lock=True, keep_request_target=False)
                self.map_scene.clear_target_selection()
                self._current_target_id = None
                self._shoot_request_flow_active = False
                return
        weapon, weapon_range = "—", None
        if attacker is not None:
            shooter_side = self._side_from_unit_id(int(attacker))
            if shooter_side is not None:
                unit = self._units_by_key.get((shooter_side, int(attacker)))
                if isinstance(unit, dict):
                    weapon, weapon_range = self._resolve_active_weapon(unit)
                    self._remember_active_weapon(attacker, weapon, weapon_range)
        range_text = f"R{weapon_range}" if isinstance(weapon_range, int) and weapon_range > 0 else "—"
        overlay_mode = str(self.map_scene.shooting_overlay_mode_label()) if hasattr(self.map_scene, "shooting_overlay_mode_label") else "Targets"
        stage = self._resolve_shoot_stage(request)
        self._shoot_ui_stage = stage
        self._shoot_resolver_step = self._shoot_stage_to_step(stage)
        dice_mode = getattr(request, "kind", "") == "dice"
        count = int(getattr(request, "count", 0) or 0)
        needs_input = dice_mode and stage in {"hit", "wound", "save"}
        action = "Roll Hit"
        step_title = "STEP 1/5: Hit Roll"
        if stage == "wound":
            action, step_title = "Roll Wound", "STEP 2/5: Wound Roll"
        elif stage == "save":
            action, step_title = "Roll Save", "STEP 4/5: Saving Throw"
        elif stage not in {"target", "hit", "wound", "save"}:
            action, step_title = "Continue", "STEP 5/5: Inflict Damage"
        info = "ℹ Нажмите Roll Hit, чтобы выбрать цель" if stage == "target" else "ℹ Введите кубы и подтвердите"
        self.viewer_controller.set_shoot_popover_open(True)
        self.viewer_controller.update_shoot_ui(
            stage=stage,
            step_title=step_title,
            stepper=self._shoot_stepper_text(),
            target_text=f"Unit {attacker} → Unit {target}",
            meta_text=f"Weapon: {weapon} ({range_text}) • Overlay: {overlay_mode}",
            action_label=action,
            info_text=info,
            needs_dice=needs_input,
        )
        if needs_input:
            self._update_shoot_input_feedback()

    def _open_shoot_popover(self, target_id: int, global_pos: Optional[QtCore.QPoint] = None) -> None:
        if target_id not in self._shoot_targets_valid:
            return
        req = self._pending_request
        if self._is_shooting_dice_request(req) and self._shoot_locked_target_id is not None:
            if int(target_id) != int(self._shoot_locked_target_id):
                self.viewer_dialogs.showToast(
                    f"Цель Unit {target_id} недоступна — зафиксирована Unit {self._shoot_locked_target_id}"
                )
                return
        if not self._shoot_resolver_active:
            self._shoot_resolver_step = 0
        self._shoot_resolver_active = True
        if self._shoot_resolver_attacker_id is None:
            self._shoot_resolver_attacker_id = self._active_unit_id or self._last_shooter_id
        if getattr(req, "kind", "") == "dice" and self._shoot_popover_target_id is not None:
            self._shoot_resolver_step = max(self._shoot_resolver_step, 1)
        self._current_target_id = int(target_id)
        self.map_scene.set_target_unit(int(target_id))
        self._shoot_popover_target_id = int(target_id)
        self._shoot_dice_input_text = ""
        self.viewer_controller.setShootDiceInput("")
        self._update_shoot_popover_ui()

    def _close_shoot_popover(self, *, reset_lock: bool = True, keep_request_target: bool = True) -> None:
        self._shoot_popover_target_id = None
        if reset_lock:
            self._shoot_locked_target_id = None
        self._shoot_resolver_active = False
        self._shoot_resolver_step = 0
        self._shoot_resolver_attacker_id = None
        self._shoot_ui_stage = "target"
        if not keep_request_target:
            self._shoot_request_target_id = None
        self.viewer_controller.set_shoot_popover_open(False)
        if self._is_shooting_target_request(self._pending_request) or self._is_shooting_dice_request(self._pending_request):
            self._set_command_prompt(self._shoot_instruction_text())

'''
p.write_text(text[:start] + new + text[end:], encoding="utf-8")
print("shoot patch ok")
