myCatalogue = 'ribos_21tomos';

for i = 1:21
    % Get the file name
    file_name = files(i).name;
    
    % Import the model
    m = dynamo_model_import('table', file_name);
    
    % Assign the model to the tomogram in the catalogue
    dcm('-c', myCatalogue, '-i', i, '-am', m);
end

