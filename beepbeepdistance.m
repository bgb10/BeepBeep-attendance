function result = beepbeepdistance(filePath, groundTruth)

rate = 48000; % sampling rate

% A chirp signal of 1 second 
% with a freq range of [1, 18]kHz 
x = audioread('./chirp.wav');

% Load data received by two different devices
y = struct();
y(1).raw = audioread(...
    [filePath, 'beacon-', num2str(groundTruth), '.wav']);
y(2).raw = audioread(...
    [filePath, 'client-', num2str(groundTruth), '.wav']);

for i = 1:2
    y(i).h = xcorr(y(i).raw, x);

    [~, pks] = findpeaks(abs(y(i).h), 'MinPeakHeight', 1, 'MinPeakDistance', rate * 1);

    
    if i == 1
        y(i).tSelf = pks(1) / rate;
        y(i).tOther = pks(2) / rate;
    else
        y(i).tOther = pks(1) / rate;
        y(i).tSelf = pks(2) / rate;        
    end
end

c = 34000; % cm/s
beacon = jsondecode(fileread(fullfile(filePath, ['beacon-' num2str(groundTruth) '.json'])));
client = jsondecode(fileread(fullfile(filePath, ['client-' num2str(groundTruth) '.json'])));
dAA = beacon.micLength; % Spk-to-mic distance in devA
dBB = client.micLength; % Spk-to-mic distance in devB

distance = c * (y(2).tOther - y(1).tSelf) + ...
    c * (y(1).tOther - y(2).tSelf) + ...
    (dAA + dBB);

distance = distance / 2;

result = distance;
end