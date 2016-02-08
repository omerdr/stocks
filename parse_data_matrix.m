clear all; close all;

%% Parse data file, retrieving Z,y
RESPONSE_STRING = '_response_';
load('data/data_matrix.mat');

% data = [Z|y] where y is labeled '_response_'. Separate Z and y:
labels_tickers = cellstr(row_labels);
labels_analysts = cellstr(column_labels); 

% Some Function Handles
get_analyst_index = @(analyst) find(strncmp(labels_analysts, {analyst}, length(analyst)));
get_stock_index = @(ticker) find(strncmp(labels_tickers, {ticker}, length(ticker)));

response_index = get_analyst_index(RESPONSE_STRING);
y = data(:, response_index);
Z = data; Z(:, response_index) = [];
idxs = 1:size(data,2); idxs = idxs(idxs~=response_index);
labels_analysts = labels_analysts(idxs,:);

clear row_labels column_labels RESPONSE_STRING response_index data idxs;

%% Show data
figure('Name', 'Data Plot');
h = subplot(121);
imagesc(Z); colorbar;
ax = gca; 
ax.XTickLabel = labels_analysts; ax.XTickLabelRotation = 90;
ax.YTickLabel = labels_tickers; ax.YTick = 1:size(Z,1);

h = subplot(122);
barh(y); grid on; axis tight;
ax = gca; ax.YTick = 1:length(y); ax.YTickLabel = labels_tickers;

% clear ax h

%% Get dense matrix Z
MIN_NUM_ANALYST_RECOMMENDATIONS_FOR_A_STOCK = 10;
MIN_NUM_ANALYST_RECOMMENDATIONS_IN_TOTAL = 5;
popular_stock_idxs = sum(Z ~= 0, 2) > MIN_NUM_ANALYST_RECOMMENDATIONS_FOR_A_STOCK;
relevant_analyst_idxs = sum(Z(popular_stock_idxs,:) ~= 0) > MIN_NUM_ANALYST_RECOMMENDATIONS_IN_TOTAL;
Z_dense = Z(popular_stock_idxs, relevant_analyst_idxs);
