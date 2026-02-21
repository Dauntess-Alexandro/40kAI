# PERF ROADMAP (TRAIN)

## 3.3. Опционально: Cython/Numba для hot loops

- [x] Выполнено.
- Реализовано опциональное ускорение hot loops для PER через `numba.njit` в `model/memory.py`.
- Добавлен безопасный fallback без Numba и флаг `WARHAMMER_DISABLE_NUMBA` для принудительного отключения JIT.
- Добавлены стабилизационные проверки для sampling/priority update, чтобы избежать silent-ошибок на edge-case значениях.
