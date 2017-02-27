
M = [0 0 0 1; 1 1 1 1; 0 0 1 0; 3 2 1 0];

Hx = [2; 3.5; 1.2; 1];
Hy = [3; 9; 1; 2];
Hz = [8; 5; 2; 0.5];

Cx = M\Hx;
Cy = M\Hy;
Cz = M\Hz;

S = 0:0.01:1;
s = 0.8;
Sx = polyval(Cx, s)
Sy = polyval(Cy, s)
Sz = polyval(Cz, s)