

```markdown
# De'Longhi Coffee Link for Home Assistant

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Davud77/delonghi_coffeelink?style=for-the-badge)](https://github.com/Davud77/delonghi_coffeelink/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/Davud77/delonghi_coffeelink?style=for-the-badge)](LICENSE)

> **Note:** This repository (`Davud77/delonghi_coffeelink`) is an enhanced fork of the original [actabi/delonghi_coffeelink](https://github.com/actabi/delonghi_coffeelink). It introduces full support for Eletta Explore specific features (Cold Brew, Iced drinks), nested JSON telemetry parsing, state caching to prevent sensor dropouts during cloud timeouts, and full Russian localization.

Home Assistant custom integration for DeLonghi PrimaDonna Soul, Eletta Explore, and other Ayla-based DeLonghi coffee machines, controlled through the Coffee Link cloud.

## Supported machines

Any DeLonghi coffee machine exposed by the Coffee Link mobile app through Ayla Networks IoT. Tested and optimized for:
- Eletta Explore ECAM450.86.T and other ECAM450.xx (Wi-Fi models with Cold Brew support)
- PrimaDonna Soul ECAM610.xx, ECAM612.xx, ECAM613.xx
- Other Coffee Link Wi-Fi machines

## Features

- **30+ beverage buttons** including standard hot drinks (Espresso, Cappuccino, etc.) and exclusive Eletta Explore drinks (Cold Brew, Iced drinks, Mug to Go).
- **Advanced Counters & Sensors**: Total beverages, per-drink counters, grounds counter, descale status, and nested telemetry extraction.
- **Sensor Caching (New)**: Prevents entities from becoming "Unknown" or "Unavailable" when the machine goes to deep sleep or the Ayla cloud times out.
- **Full RU / EN Localization**.
- Generic Stop and Wake buttons.
- Services for raw binary command injection (advanced use).

## IMPORTANT - Coffee Link mobile app must be closed

The machine prioritizes LAN connections over cloud. As long as the Coffee Link mobile app is running on a phone on the same Wi-Fi network, it holds a LAN session (30s keep-alive) and the machine ignores cloud commands.

**Close the Coffee Link app completely** (swipe from recents) before using Home Assistant. If you want to regain control from the app, just reopen it.

## Installation

### Via HACS (recommended)

1. In HACS, click the 3-dots menu > **Custom repositories**
2. Add `https://github.com/Davud77/delonghi_coffeelink` as category **Integration**
3. Install "De'Longhi Coffee Link"
4. Restart Home Assistant
5. Add integration via **Settings > Devices & Services**
6. Enter your Coffee Link email and password (same as the mobile app)

### Manual

1. Copy `custom_components/delonghi_coffeelink/` to your HA `config/custom_components/`
2. Restart Home Assistant
3. Add integration via Settings > Devices & Services

## Services

```yaml
# Start a beverage
service: delonghi_coffeelink.start_beverage
data:
  beverage: cold_coffee  # espresso, cappuccino, brew_over_ice, cold_coffee, etc.

# Stop a beverage
service: delonghi_coffeelink.stop_beverage
data:
  beverage: hot_water

# Send a raw binary command (advanced)
service: delonghi_coffeelink.send_raw_command
data:
  value_base64: DQ2D8BABDwD6GwEGgSRp6Myg
```

## Technical details

This integration implements the Coffee Link authentication and command protocol:

1. Authenticate to Gigya (SAP Customer Data Cloud) identity service
2. Request a signed JWT (HMAC-SHA1 over the Gigya session)
3. Exchange the JWT for an Ayla Networks SSO token
4. Poll Ayla Networks IoT cloud for 312 device properties
5. Send binary commands via the `data_request` property (base64-encoded)

Command format (18 bytes):

```
byte  0-1  : 0x0d 0x0d       prefix + length
byte  2-3  : 0x83 0xf0       command family: beverage
byte  4    : beverage_id     0x01 = espresso, 0x78 = cold brew, etc.
byte  5    : action          0x01 = start, 0x02 = stop
byte  6-11 : recipe params   temperature, quantity, aroma
byte 12-13 : CRC16 AUG-CCITT over bytes 0..11
byte 14-17 : Unix timestamp (big-endian)
```

## Credits

- Fork enhancements (Eletta Explore, Cold Brew, State Caching): @Davud77
- Original integration & reverse engineering: @actabi (2026) - [actabi/delonghi_coffeelink](https://github.com/actabi/delonghi_coffeelink)
- Based on the Ayla Networks LAN protocol research from [jakecrowley/AylaLocalAPI](https://github.com/jakecrowley/AylaLocalAPI)
- DeLonghi BLE protocol research from [Arbuzov/home_assistant_delonghi_primadonna](https://github.com/Arbuzov/home_assistant_delonghi_primadonna)

## License

MIT

---

# De'Longhi Coffee Link для Home Assistant (RU)

> **Примечание:** Данный репозиторий (`Davud77/delonghi_coffeelink`) является расширенным форком оригинального проекта [actabi/delonghi_coffeelink](https://github.com/actabi/delonghi_coffeelink). В эту версию добавлена поддержка уникальных функций серии Eletta Explore (напитки Cold Brew и со льдом), умный парсинг вложенной телеметрии, кэширование состояний сенсоров для защиты от тайм-аутов облака и полная русская локализация.

Пользовательская интеграция Home Assistant для кофемашин DeLonghi Eletta Explore, PrimaDonna Soul и других моделей на базе Ayla, управляемых через облако Coffee Link.

## Поддерживаемые кофемашины

Любая кофемашина DeLonghi, которая работает с мобильным приложением Coffee Link через платформу Ayla Networks IoT. Протестировано и оптимизировано для:
- Eletta Explore ECAM450.86.T и другие модели ECAM450.xx (Wi-Fi версии с поддержкой Cold Brew)
- PrimaDonna Soul ECAM610.xx, ECAM612.xx, ECAM613.xx
- Другие кофемашины с поддержкой Wi-Fi и Coffee Link

## Особенности

- **Более 30 кнопок управления напитками**, включая стандартные горячие напитки (Эспрессо, Капучино и т.д.) и эксклюзивные напитки Eletta Explore (Cold Brew, Iced-напитки, термокружка).
- **Продвинутая телеметрия и сенсоры**: Общие счетчики, счетчики конкретных напитков, счетчик контейнера для гущи, статус очистки от накипи.
- **Кэширование состояний (Новое)**: Предотвращает переход сенсоров в статус «Неизвестно» (Unknown) или «Недоступно» при переходе машины в глубокий сон или обрывах связи с облаком Ayla.
- **Полная локализация на русский и английский языки**.
- Кнопки Пробуждения (Wake) и экстренной остановки (Stop).
- Службы для отправки сырых бинарных команд (для продвинутых пользователей).

## ВАЖНО - Мобильное приложение Coffee Link должно быть закрыто

Кофемашина отдает приоритет локальному LAN-соединению перед облачным. Пока оригинальное приложение Coffee Link открыто на телефоне в той же Wi-Fi сети, оно удерживает активную LAN-сессию (keep-alive 30 сек), и машина полностью игнорирует команды из облака (Home Assistant).

**Полностью закройте приложение Coffee Link** (смахните из недавних) перед использованием кнопок в Home Assistant. Чтобы вернуть управление смартфону — просто откройте приложение снова.

## Установка

### Через HACS (Рекомендуется)

1. В HACS нажмите на меню (три точки) в правом верхнем углу > **Пользовательские репозитории** (Custom repositories)
2. Добавьте ссылку `https://github.com/Davud77/delonghi_coffeelink`, выбрав категорию **Интеграция** (Integration)
3. Нажмите **Скачать** (Download) на карточке "De'Longhi Coffee Link"
4. Перезагрузите Home Assistant (Настройки -> Система -> Перезапуск)
5. Добавьте интеграцию через **Настройки > Устройства и службы > Добавить интеграцию**
6. Введите ваш Email и пароль от Coffee Link (те же, что и в мобильном приложении)

### Вручную

1. Скопируйте папку `custom_components/delonghi_coffeelink/` в директорию `config/custom_components/` вашего Home Assistant.
2. Перезагрузите Home Assistant.
3. Добавьте интеграцию через Настройки > Устройства и службы.

## Использование служб (Services)
```yaml
# Запуск приготовления напитка
service: delonghi_coffeelink.start_beverage
data:
  beverage: cold_coffee  # espresso, cappuccino, brew_over_ice, cold_coffee и т.д.

# Остановка приготовления
service: delonghi_coffeelink.stop_beverage
data:
  beverage: hot_water

# Отправка сырой бинарной команды
service: delonghi_coffeelink.send_raw_command
data:
  value_base64: DQ2D8BABDwD6GwEGgSRp6Myg
```

## Лицензия

MIT
```