myCatalogue = 'artiax_21tomos';

% Get the list of .tbl files ./tbls and sort them alphabetically
files = dir('*.tbl');
% files = sort(files,1);
% print the list of files
for i = 1:length(files)
    disp(files(i).name);
end
% For each file, load it into a dynamo table
for i = 1:length(files)
    % Get the file name
    file_name = files(i).name;
    
    % Import the model
    m = dynamo_model_import('table', file_name);
    
    % Assign the model to the tomogram in the catalogue
    dcm('-c', myCatalogue, '-i', i, '-am', m);
end

