clear; clc; close all;

%% Project path
projectRoot = '/Users/hao/Documents/CodeProject/Python/SIRI_WB_Rep';
cd(projectRoot);

%% Add paths
addpath(genpath(fullfile(projectRoot, 'matlab', 'Balu')));
addpath(genpath(fullfile(projectRoot, 'data', 'filters', 'bsif')));

%% Test image
imgPath = fullfile(projectRoot, ...
    'data', 'DemodulatedImages', 'PhaseDifference', ...
    '1Normal', 'Batch01_Normal_S001.tif');

I = imread(imgPath);

fprintf('Image size:\n');
disp(size(I));

fprintf('Image class:\n');
disp(class(I));

if size(I, 3) > 1
    I = rgb2gray(I);
end

%% Foreground crop
mask = I > 0;
[y, x] = find(mask);

if ~isempty(x)
    pad = 10;

    x1 = max(min(x) - pad, 1);
    x2 = min(max(x) + pad, size(I, 2));
    y1 = max(min(y) - pad, 1);
    y2 = min(max(y) + pad, size(I, 1));

    Icrop = I(y1:y2, x1:x2);
else
    Icrop = I;
end

%% Resize
Icrop = imresize(Icrop, [256 256]);

figure;
imshow(Icrop, []);
title('Cropped Phase Difference Image');

%% LBP test: 59 features
lbpOpt.vdiv = 1;
lbpOpt.hdiv = 1;
lbpOpt.semantic = 0;
lbpOpt.samples = 8;
lbpOpt.mappingtype = 'u2';

[X_lbp, Xn_lbp] = Bfx_lbp(Icrop, [], lbpOpt);

fprintf('\nLBP feature size:\n');
disp(size(X_lbp));

%% BSIF default: 5x5, 7-bit
bsifOpt.vdiv = 1;
bsifOpt.hdiv = 1;
bsifOpt.filter = 5;
bsifOpt.bits = 7;
bsifOpt.mode = 'nh';

[X_bsif_5_7, Xn_bsif_5_7] = Bfx_bsif(Icrop, [], bsifOpt);

fprintf('\nBSIF 5x5 7-bit feature size:\n');
disp(size(X_bsif_5_7));

%% BSIF optimized: 7x7, 8-bit
bsifOpt.filter = 7;
bsifOpt.bits = 8;
bsifOpt.mode = 'nh';

[X_bsif_7_8, Xn_bsif_7_8] = Bfx_bsif(Icrop, [], bsifOpt);

fprintf('\nBSIF 7x7 8-bit feature size:\n');
disp(size(X_bsif_7_8));

%% HOG test: 20 x 10 cells, 9 bins = 1800 features
hogOpt.nj = 20;
hogOpt.ni = 10;
hogOpt.B = 9;
hogOpt.show = 0;

[X_hog, Xn_hog] = Bfx_hog(Icrop, hogOpt);

fprintf('\nHOG feature size:\n');
disp(size(X_hog));

fprintf('\nDone.\n');