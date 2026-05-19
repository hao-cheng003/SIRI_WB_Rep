clear; clc; close all;

%% Project path
projectRoot = '/Users/hao/Documents/CodeProject/Python/SIRI_WB_Rep';
cd(projectRoot);

%% Add paths
addpath(genpath(fullfile(projectRoot, 'matlab', 'Balu')));
addpath(genpath(fullfile(projectRoot, 'data', 'filters', 'bsif')));

%% Input and output
labelPath = fullfile(projectRoot, 'data', 'labels.csv');
outDir = fullfile(projectRoot, 'data', 'processed', 'bsif_bits_sweep_nocrop');

if ~exist(outDir, 'dir')
    mkdir(outDir);
end

labels = readtable(labelPath);
n = height(labels);

fprintf('Total samples: %d\n', n);

%% Sweep setting
fixedFilter = 9;
bitList = [5 6 7 8 9 10 11 12];

%% Process each bit length
for bits = bitList
    fprintf('\nExtracting BSIF filter=%dx%d, bits=%d\n', fixedFilter, fixedFilter, bits);

    numFeatures = 2 ^ bits;
    X = zeros(n, numFeatures);

    bsifOpt.vdiv = 1;
    bsifOpt.hdiv = 1;
    bsifOpt.filter = fixedFilter;
    bsifOpt.bits = bits;
    bsifOpt.mode = 'nh';

    for i = 1:n
        relPath = string(labels.relative_path(i));
        imgPath = fullfile(projectRoot, relPath);

        I = imread(imgPath);

        if size(I, 3) > 1
            I = rgb2gray(I);
        end

        % No crop, no resize
        Iuse = I;

        [x_bsif, ~] = Bfx_bsif(Iuse, [], bsifOpt);
        X(i, :) = double(x_bsif(:))';

        if mod(i, 20) == 0 || i == n
            fprintf('Processed %d / %d\n', i, n);
        end
    end

    meta = labels(:, {'filename', 'relative_path', 'sample_id', ...
        'severity', 'binary_label', 'binary_name'});

    outName = sprintf('balu_bsif_%dx%d_%dbit_nocrop.csv', fixedFilter, fixedFilter, bits);
    outPath = fullfile(outDir, outName);

    save_feature_csv(meta, X, sprintf('bsif_%dx%d_%dbit_', fixedFilter, fixedFilter, bits), outPath);

    fprintf('Saved: %s\n', outPath);
end

fprintf('\nBits sweep finished.\n');

%% Local function
function save_feature_csv(meta, X, prefix, outPath)
numFeatures = size(X, 2);

featureNames = strings(1, numFeatures);
for j = 1:numFeatures
    featureNames(j) = sprintf('%s%04d', prefix, j);
end

featureTable = array2table(X, 'VariableNames', cellstr(featureNames));
outTable = [meta, featureTable];

writetable(outTable, outPath);
end