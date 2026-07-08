function [names, onsets, durations] = build_multiple_conditions(nirsMatFile, evtFile, outputFile)
%BUILD_MULTIPLE_CONDITIONS Build SPM-style conditions from NIRS events.
%   [names, onsets, durations] = build_multiple_conditions(...)
%   computes onsets/durations in seconds and rounds to 2 decimals
%   (Excel-like presentation precision).
%
%   Inputs (all optional):
%     nirsMatFile - path to NIRS .mat file (default: 'NIRS.mat')
%     evtFile     - path to .evt file      (default: 'NIRS-2025-10-03_003.evt')
%     outputFile  - path to output .mat    (default: 'multiple_conditions.mat')

    if nargin < 1 || isempty(nirsMatFile)
        nirsMatFile = 'NIRS.mat';
    end
    if nargin < 2 || isempty(evtFile)
        evtFile = 'NIRS-2025-10-03_003.evt';
    end
    if nargin < 3 || isempty(outputFile)
        outputFile = 'multiple_conditions.mat';
    end

    data = load(nirsMatFile);

    if isfield(data, 'P') && isfield(data.P, 'fs') && ~isempty(data.P.fs)
        fs = data.P.fs;
    else
        fs = 3.90625;
    end

    if isfield(data, 'Y') && isfield(data.Y, 'hbo') && ~isempty(data.Y.hbo)
        endTime = size(data.Y.hbo, 1) / fs;
    elseif isfield(data, 'y') && ~isempty(data.y)
        endTime = size(data.y, 1) / fs;
    else
        error('Не удалось определить длительность записи (нет Y.hbo и y).');
    end

    evt = readmatrix(evtFile, 'FileType', 'text', 'Delimiter', '\t');
    if size(evt, 2) < 9
        error('Файл %s должен содержать минимум 9 колонок (time + 8 бит).', evtFile);
    end

    evtSamples = evt(:, 1);
    evtBits = evt(:, 2:9);

    evtTimes = evtSamples / fs;

    bitWeights = 2 .^ (0:7)';
    codes = evtBits * bitWeights;

    allDurations = [diff(evtTimes); endTime - evtTimes(end)];

    precisionDigits = 2;
    evtTimes = round(evtTimes, precisionDigits);
    allDurations = round(allDurations, precisionDigits);

    names = {'Event #1', 'Event #2', 'Event #3'};
    codeMap = [1, 2, 3];

    onsets = cell(1, numel(codeMap));
    durations = cell(1, numel(codeMap));

    for i = 1:numel(codeMap)
        idx = (codes == codeMap(i));
        onsets{i} = evtTimes(idx).';
        durations{i} = allDurations(idx).';
    end

    save(outputFile, 'names', 'onsets', 'durations');

    fprintf('✅ %s saved\n', outputFile);

    for i = 1:numel(codeMap)
        fprintf('--- %s ---\n', names{i});
        disp([onsets{i}' durations{i}']);
    end
end
