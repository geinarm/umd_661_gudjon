function [ ] = drawGraph( Nodes, Edges )

P1 = Edges(:, 1);
P2 = Edges(:, 2);

x1 = Nodes(P1, 1);
x2 = Nodes(P2, 1);
y1 = Nodes(P1, 2);
y2 = Nodes(P2, 2);

plot(Nodes(:, 1), Nodes(:, 2), '.', 'MarkerSize', 15);
line([x1,x2]', [y1,y2]');

end

