function imgInterp = imgInterpolation(img,neighbors)
%{
    Linearly interpolate an image to fill in missing data.
%}

imgSize = size(img);
imgInterp = zeros(imgSize);

near4 = [0,1;-1,0;0,-1;1,0];
near8 = [0,1;-1,0;0,-1;1,0;1,1;-1,1;1,-1;-1,-1];

if neighbors == 4, near = near4; elseif neighbors == 8, near = near8; end

for row = 2:imgSize(1)-1
    for colm = 2:imgSize(2)-1
        pixVal = img(row,colm,:);
        
        n = 1; 
        for index = near'
            nearVals(n,:) = [index(1),index(2),reshape(img(row+index(1),colm+index(2),:),1,[])];
            n = n + 1;
        end
        
        if isnan(mean(pixVal)) && any(mean(nearVals(:,3:5),2))
            avgVal = [];
            n = 1; 
            for nearVal = nearVals'
                tempRow = nearVal(1);
                tempColm = nearVal(2);

                val1 = nearVal(3:end);
                for compVal = nearVals'
                    compRow = compVal(1);
                    compColm = compVal(2);
                    
                    if [compRow,compColm] == [-tempRow,-tempColm]
                        val2 = compVal(3:end);
                    end
                end

                interpVal = mean([val1;val2]);
                avgVal = cat(1,avgVal,interpVal);
                
                n = n + 1;
            end

            pixVal = reshape(mean(avgVal),1,1,[]);
        end

        imgInterp(row,colm,:) = pixVal;
    end
    row
end
end