# Миграция: Lua rules/sim как окружение для Python (вертикальный срез)

## Требования
- **Lua/LuaJIT** установлен и доступен в `PATH`.
- **LuaSocket** для TCP.

### Установка (Windows)
1. Установите Lua или LuaJIT.
   - Пример для Lua: скачайте с https://www.lua.org/ftp/ (Windows binaries) и добавьте путь в `PATH`.
   - Пример для LuaJIT: используйте готовые сборки и добавьте путь в `PATH`.
2. Установите LuaRocks и LuaSocket:
   ```powershell
   luarocks install luasocket
   ```
3. Если `lua` не в `PATH`, задайте переменную окружения `LUA_EXE`:
   ```powershell
   $env:LUA_EXE = "C:\\path\\to\\lua.exe"
   ```

## Запуск smoke test
```powershell
python -m python_env.smoke_test
```

## Что происходит
- Python запускает TCP-host на Lua (`lua_host/host.lua`).
- Lua-host принимает JSON Lines команды `reset/step/close`.
- Python читает `obs/reward/done/info`.

## Troubleshooting
- **Порт занят**: задайте другой порт через `HOST_PORT`.
- **Host не стартует**: проверьте `LUA_EXE`, доступность `lua` и установку `luasocket`.
- **Нет сокетов**: убедитесь, что LuaSocket установлен через LuaRocks.

## Логи
- Lua-host: `HOST_DEBUG=1`
- Python env: `PY_ENV_DEBUG=1`
