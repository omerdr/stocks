%% Load data

data = importdata('/home/omer/code/github/stocks/numeric_recos.csv');
X = data.data;

% If this doesn't return an empty matrix we're in trouble
% (meaning there's a NaN in the data, probably resulting from a
% recommendation that wasn't classified as buy/sell/neutral in the python
% code)
[r,c] = find(isnan(X))
if (~isempty(r) || ~isempty(c))
    fprintf('we''re in trouble\n');
    X(r,c) = 0;
end;

%% Find Clusters
D = pdist(X);
clusterTree = linkage(D,'ward');

for m=3:10;
    clusters = cluster(clusterTree, 'maxclust', m);

    fprintf('Cluster sizes (for m=%d): \n', m);
    uniq = unique(clusters)';
    for i=uniq;
        fprintf('Cluster %2d: %5d elements\n', i, sum(clusters == uniq(i)));
    end;
end;

clusters = cluster(clusterTree, 'maxclust', 3);

%% Principle Component Visualization
%Xreduced = X;
%Xreduced( :, all(~Xreduced,1) ) = [];
%Xreduced( all(~Xreduced,2), : ) = [];
[pc, score] = princomp(X);
top_10_score = score(:,1:10);

