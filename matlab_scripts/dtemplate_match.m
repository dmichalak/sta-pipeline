% Based on the script https://github.com/builab/subtomo/blob/main/dynamo_template_matching/dtemplate_matching.m
%
% Script to template match in all tomograms listed in tomograms.vll
% Runs locally and on a cluster
%

tomogram = 'tilt114.mrc';
template = 'average48.em';
mask = 'mask48.em';
sizeOfChunk = [256, 256, 256]; % chunk size of tomogram volume to send to a CPU for matching
coneRange = 360;
coneSampling = 30;
inPlaneRotationRange = 0;
inPlaneRotationSampling = 1;
binning = 1;
crossCorrelationThreshold = 0.38;

tomogramListFile = 'tomograms.vll'; % file containing a list of all tomogram paths
JobStorageLocation = '/tmp';
NumWorkers = 6; % same as cpu-per-task in SBATCH
outputFolder = 'cs30'; % output folder will be named "outputFolder.TM"

% % % Read and parse the tomogram list file % % %
fileID = fopen(tomogramListFile); tomogramList = textscan(fileID, '%s'); fclose(fileID);
tomogramList = tomogramList{1};
nTomograms = length(tomogramList);

% % % Cluster related settings % % %
local_cluster = parcluster('local');
local_cluster.JobStorageLocation = '/tmp';
local_cluster.NumWorkers = NumWorkers;

for i = 1:nTomograms
	tomogram = tomogramList{i};
	[tomogramPath, tomogramName, ext] = fileparts(tomogram);

	tomogramName = strrep(tomogramName, '_rec', ''); % assuming the naming convention used in IMOD 4.11
	disp(tomogramName);

	% % % Begin template matching in tomogram % % %
	pts = dynamo_match(tomogram, template, 'mask', mask, 'outputFolder', outputFolder, 'sc', sizeOfChunk, 'cr', coneRange, 'cs', coneSampling, 'ir', inPlaneRotationRange, 'is', inPlaneRotationSampling, 'bin', binning, 'mw', local.NumWorkers);
	% Note: The results of matching can be read into memory in a new session with... pts = dread(outputFolder '/process.mat');

	%pts.peaks.plotCCPeaks('sidelength', 50);

	% % % Extract table... % % %
	%	The template is first aligned at highest correlation position, then is aligned with the second highest correlation position.
	%	If the second alignment overlaps with the previoues, the second is considered spurious and skipped. This procedure is repeated until
	%	a threshold cross correlation is reached.
	matchTable = pts.peaks.computeTable('mcc', crossCorrelationThreshold);
	
	% % % Sketch 3D positions of the particles % % %
	%dtplot(matchTable, 'pf', 'oriented_positions');

	% % % Not sure what this does % % %
	%save(gcf, TS_001.png')
	
	% % % Put table back into catalogue... % % %
	%	* Eases keeping tack of all the steps you've performed
	%	* Allows you to visualize the peaks on the tomogram interactively
	%		- so you can delete false positives or add peaks that were not found by template matching

	tableOriginalScale = dynamo_table_rescale(matchTable, 'factor', 2); % scale particles back to original size
	disp([outputFolder '/' tomogramName '_peaks.tbl' ]);
	dwrite(tableOriginalScale, [outputFolder '/' tomogramName '_peaks.tbl']); % write table to file
end
