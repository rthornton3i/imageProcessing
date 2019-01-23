function imgTrans = affineTransform(img,mat)
%{
    Transform image using affine transformation.
%}

imgSize = size(img);
numCh = length(imgSize);

corners = [1,1;1,imgSize(2);imgSize(1),1;imgSize(1),imgSize(2)];
rowIndex = [];
colmIndex = [];
for n = corners'
    transMat = mat * [n(1);n(2);1];
    rowIndex = cat(1,rowIndex,round(transMat(1)));
    colmIndex = cat(1,colmIndex,round(transMat(2)));
end

rowBias = abs(min(rowIndex)) + 1;
colmBias = abs(min(colmIndex)) + 1;

for row = 1:size(img,1)
    for colm = 1:size(img,2)
        pixVal = img(row,colm,:);
        
        transMat = mat * [row;colm;1];
        tempRow = round(transMat(1)) + rowBias;
        tempColm = round(transMat(2)) + colmBias;
        
        imgTrans{tempRow,tempColm} = pixVal;
    end
end

imgTrans(cellfun(@isempty,imgTrans)) = {reshape([NaN,NaN,NaN],1,1,3)};
imgTrans = cell2mat(imgTrans);
end