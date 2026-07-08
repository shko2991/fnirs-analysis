% === автоматически определяем HDR-файл ===
hdrFiles = dir('*.hdr');

if isempty(hdrFiles)
    error('В текущей папке нет .hdr файла. Перейди в папку с NIRx-данными.');

elseif numel(hdrFiles) == 1
    hdrFile = hdrFiles(1).name;
    fprintf('Используется HDR-файл: %s\n', hdrFile);

else
    [idx, ok] = listdlg( ...
        'PromptString', 'Выбери HDR-файл:', ...
        'SelectionMode', 'single', ...
        'ListString', {hdrFiles.name});

    if ~ok
        error('HDR-файл не выбран.');
    end

    hdrFile = hdrFiles(idx).name;
    fprintf('Выбран HDR-файл: %s\n', hdrFile);
end
outputFile = 'multiple_conditions.mat';     % имя итогового файла для SPM

% === читаем hdr как текст ===
txt = fileread(hdrFile);
lines = regexp(txt, '\r\n|\n|\r', 'split');

% === находим секцию [Markers] ===
idxStart = find(strcmp(strtrim(lines), '[Markers]'), 1, 'first');

if isempty(idxStart)
    error('Секция [Markers] не найдена в %s', hdrFile);
end

% === собираем строки внутри [Markers] ===
markerLines = {};

for i = idxStart+1:numel(lines)
    line = strtrim(lines{i});

    if isempty(line)
        continue;
    end

    if startsWith(line, '[') && endsWith(line, ']')
        break;
    end

    markerLines{end+1} = line; %#ok<AGROW>
end

if isempty(markerLines)
    error('В секции [Markers] нет данных.');
end

% === извлекаем события: время, код, sample ===
validEvents = [];

for i = 1:numel(markerLines)
    line = markerLines{i};

    % пропускаем служебные строки
    if contains(line, 'Events=') || startsWith(line, '#') || contains(line, '#"')
        continue;
    end

    nums = sscanf(line, '%f');

    if numel(nums) >= 3
        validEvents = [validEvents; nums(1:3)']; %#ok<AGROW>
    end
end

if isempty(validEvents)
    error('Не удалось извлечь события из секции [Markers].');
end

events = validEvents;

evtTimes = events(:,1);     % времена событий из hdr
codes = events(:,2);        % коды событий

% === вычисляем durations ===
allDurations = [diff(evtTimes); NaN];

% для последнего события берем среднее всех валидных положительных duration
validDur = allDurations(1:end-1);
validDur = validDur(~isnan(validDur));
validDur = validDur(validDur > 0);

if isempty(validDur)
    error('Не удалось вычислить среднюю duration.');
end

meanDur = mean(validDur);
allDurations(end) = round(meanDur, 0);

% округляем
evtTimes = round(evtTimes, 2);
allDurations = round(allDurations, 2);

% === автоматически определяем условия ===
codeMap = unique(codes).';   % например [1 2 3] или [1 2 4 5]

names = cell(1, numel(codeMap));
onsets = cell(1, numel(codeMap));
durations = cell(1, numel(codeMap));

for i = 1:numel(codeMap)
    names{i} = sprintf('Event #%d', codeMap(i));

    idx = (codes == codeMap(i));

    onsets{i} = evtTimes(idx).';
    durations{i} = allDurations(idx).';
end

% === сохраняем файл для SPM ===
save(outputFile, 'names', 'onsets', 'durations');

disp('multiple_conditions.mat saved from HDR times');

% === выводим для проверки ===
for i = 1:numel(codeMap)
    fprintf('--- %s ---\n', names{i});
    disp([onsets{i}' durations{i}']);
end