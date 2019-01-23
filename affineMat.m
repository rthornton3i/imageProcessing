function mat = affineMat(pts1,pts2)
%{
    Calculate affine warp matrix.

    Note: Points passed as array in form [row1,colm1;row2,colm2;row3,colm3]

    ref: "https://math.stackexchange.com/questions/1092002/how-to-define-an-affine-transformation-using-2-triangles"
%}

a = [transpose(pts1);1,1,1];
b = [transpose(pts2);1,1,1];

mat = b/a;
end