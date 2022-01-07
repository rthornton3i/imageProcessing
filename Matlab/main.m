clc;
clear;
close all;

addpath(genpath('Functions'));
addpath(genpath('../Images'));

file = Tiff('Andromeda.TIF','r');
img = im2double(read(file));
stretchedImg = imadjust(img,stretchlim(img),[]);

subplot(2,1,1)
histogram(img)
subplot(2,1,2)
histogram(stretchedImg)

% imshow(stretchedImg);
% pts1 = [240,333;221,1141;638,793];
% pts2 = [97,81;95,1117;797,807];
% 
% mat = affineMat(pts1,pts2);
% imgTrans = affineTransform(img,mat);

% imgInterp = imgInterpolation(imgTrans,8);
% 
% figure(1)
% imshow(imgTrans)
% figure(2)
% imshow(imgInterp)