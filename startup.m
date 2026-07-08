toolboxes = {
    'C:\Users\svkeskii\MATLAB Drive\Homer3-master'
    'C:\Users\svkeskii\MATLAB Drive\spm_25.01.02\spm'
    'C:\Users\svkeskii\MATLAB Drive\AtlasViewer-master'
    'C:\Users\svkeskii\MATLAB Drive\mcxlabcl'
};

for i = 1:numel(toolboxes)
    if isfolder(toolboxes{i})
        addpath(genpath(toolboxes{i}));
    else
        warning('Папка не найдена: %s', toolboxes{i});
    end
end

disp('Neuroimaging toolboxes loaded')