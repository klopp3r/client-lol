# Сборка форка Telegram (arm64, рядом с официальным)

Собирать локально нельзя: Android SDK и NDK Google выдают только под x86-64,
а хост — aarch64. Сборка идёт в GitHub Actions на x86-64-раннере.

## Что здесь

- `.github/workflows/build-apk.yml` — сборка `:TMessagesProj_App:assembleAfatRelease`
- `fork.patch` — два изменения, без которых конфигурация падает:
  - `TMessagesProj/build.gradle`: `buildFeatures { buildConfig = true }` — требует AGP 8.13
  - `TMessagesProj_App/build.gradle`: `abiFilters "arm64-v8a"` вместо четырёх ABI

## Параметры сборки

| Параметр | Значение |
|---|---|
| applicationId | `org.telegram.messenger.fork` — встанет рядом с официальным |
| ABI | только `arm64-v8a` |
| Подпись | keystore из репозитория: пароль `android`, alias `androidkey` |
| API-ключи | `APP_ID = 4` из `BuildVars.java` — официальные ключи Telegram |

## Как запустить

1. Создай пустой публичный репозиторий на GitHub.
2. Скопируй в него `.github/workflows/build-apk.yml` и `fork.patch`.
3. Actions → Build telegram fork → Run workflow.
4. Скачай `telegram-fork-apk` из артефактов.

## Про API-ключи

Сборка использует официальные `APP_ID`/`APP_HASH` из исходников. Это нарушает
условия Telegram API, и такие сборки рано или поздно упираются в rate limit.
Свои ключи с my.telegram.org надёжнее: положить их в secrets и подставить
в `TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java`.

## Установка

Официальный Telegram не затрагивается — `applicationId` другой. Обе версии
работают одновременно, но входят в Telegram раздельно.

```bash
adb install -r telegram-fork.apk
```

Без кабеля: телефон → Настройки → Для разработчиков → Отладка по Wi-Fi,
затем `adb pair` и `adb connect`. Либо установить через Shizuku.
