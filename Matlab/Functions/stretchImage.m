function img = stretchImage(img,scales)
    img(img<scales(1)) = scales(1);
    img(img>scales(2)) = scales(2);
    img = rescale(img);
end