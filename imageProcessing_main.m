% clc;
% clear;
% 
% addpath(genpath('Functions'));
% 
% fileName = 'stars.jpg';
% img = im2double(imread(fileName));
% 
% pts1 = [240,333;221,1141;638,793];
% pts2 = [97,81;95,1117;797,807];
% 
% mat = affineMat(pts1,pts2);
% imgTrans = affineTransform(img,mat);

imgInterp = imgInterpolation(imgTrans,8);

figure(1)
imshow(imgTrans)
figure(2)
imshow(imgInterp)