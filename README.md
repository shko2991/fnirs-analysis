# Matlab

Скрипт `build_multiple_conditions.m` собирает `names`, `onsets`, `durations` из `NIRS.mat` + `.evt`.

## Что важно
- Время событий и длительности округляются до 2 знаков (`round(..., 2)`), чтобы значения совпадали с Excel-представлением.
- Добавлены проверки структуры входных данных.

## Запуск
```matlab
build_multiple_conditions('NIRS.mat', 'NIRS-2025-10-03_003.evt', 'multiple_conditions.mat');
```
