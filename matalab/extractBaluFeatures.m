clear; clc; close all;

%% Project path
projectRoot = '/Users/hao/Documents/CodeProject/Python/SIRI_WB_Rep';
cd(projectRoot);

%% Add paths
addpath(genpath(fullfile(projectRoot, 'matlab', 'Balu')));
addpath(genpath(fullfile(projectRoot, 'data', 'filters', 'bsif')));

%% Input and output
labelPath = fullfile(projectRoot, 'data', 'labels.csv');
outDir = fullfile(projectRoot, 'data', 'processed', 'balu_nocrop');

if ~exist(outDir, 'dir')
    mkdir(outDir);
end

labels = readtable(labelPath);
n = height(labels);

fprintf('Total samples: %d\n', n);

%% Feature options

% LBP: 59 features
lbpOpt.vdiv = 1;
lbpOpt.hdiv = 1;
lbpOpt.semantic = 0;
lbpOpt.samples = 8;
lbpOpt.mappingtype = 'u2';

% BSIF default: 5x5, 7-bit
bsif57Opt.vdiv = 1;
bsif57Opt.hdiv = 1;
bsif57Opt.filter = 5;
bsif57Opt.bits = 7;
bsif57Opt.mode = 'nh';

% BSIF optimized: 7x7, 8-bit
bsif78Opt.vdiv = 1;
bsif78Opt.hdiv = 1;
bsif78Opt.filter = 7;
bsif78Opt.bits = 8;
bsif78Opt.mode = 'nh';

%% Allocate
X_lbp = zeros(n, 59);
X_bsif57 = zeros(n, 128);
X_bsif78 = zeros(n, 256);

%% Process all images
for i = 1:n
    relPath = string(labels.relative_path(i));
    imgPath = fullfile(projectRoot, relPath);

    I = imread(imgPath);

    if size(I, 3) > 1
        I = rgb2gray(I);
    end

    % Important: no crop, no resize
    Iuse = I;

    [x_lbp, ~] = Bfx_lbp(Iuse, [], lbpOpt);
    X_lbp(i, :) = double(x_lbp(:))';

    [x_bsif57, ~] = Bfx_bsif(Iuse, [], bsif57Opt);
    X_bsif57(i, :) = double(x_bsif57(:))';

    [x_bsif78, ~] = Bfx_bsif(Iuse, [], bsif78Opt);
    X_bsif78(i, :) = double(x_bsif78(:))';

    if mod(i, 10) == 0 || i == n
        fprintf('Processed %d / %d\n', i, n);
    end
end

%% Metadata
meta = labels(:, {'filename', 'relative_path', 'sample_id', ...
                  'severity', 'binary_label', 'binary_name'});

%% Save
save_feature_csv(meta, X_lbp, 'lbp_', ...
    fullfile(outDir, 'balu_lbp59_nocrop.csv'));

save_feature_csv(meta, X_bsif57, 'bsif57_', ...
    fullfile(outDir, 'balu_bsif_5x5_7bit_nocrop.csv'));

save_feature_csv(meta, X_bsif78, 'bsif78_', ...
    fullfile(outDir, 'balu_bsif_7x7_8bit_nocrop.csv'));

X_lbp_bsif78 = [X_lbp, X_bsif78];

save_feature_csv(meta, X_lbp_bsif78, 'lbp_bsif78_', ...
    fullfile(outDir, 'balu_lbp59_bsif_7x7_8bit_nocrop.csv'));

fprintf('\nAll no-crop Balu features saved to:\n%s\n', outDir);

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

    fprintf('Saved: %s | shape = %d x %d\n', ...
        outPath, size(outTable, 1), size(outTable, 2));
end