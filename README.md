# Matlab

## Тестовое задание iFORA

Из-за ограничения Git на бинарные вложения три готовых файла упакованы в один
текстовый Base64-файл:

- [`deliverables_bundle.tar.gz.b64`](deliverables/deliverables_bundle.tar.gz.b64) —
  архив с презентацией в PPTX и PDF, а также аналитической справкой в DOCX;
- `assets/*.svg` — исходники слайдов в векторном формате.

Чтобы восстановить отдельные итоговые файлы:

```bash
base64 --decode deliverables/deliverables_bundle.tar.gz.b64 > deliverables_bundle.tar.gz
tar -xzf deliverables_bundle.tar.gz
```

Для воспроизводимой сборки всех файлов используется:

```bash
python3 generate_deliverables.py
```

Генератор создает только текстовый Base64-файл; промежуточные бинарные файлы
после упаковки удаляются.

Скрипт `build_multiple_conditions.m` собирает `names`, `onsets`, `durations` из `NIRS.mat` + `.evt`.

## Что важно
- Время событий и длительности округляются до 2 знаков (`round(..., 2)`), чтобы значения совпадали с Excel-представлением.
- Добавлены проверки структуры входных данных.

## Запуск
```matlab
build_multiple_conditions('NIRS.mat', 'NIRS-2025-10-03_003.evt', 'multiple_conditions.mat');
```
