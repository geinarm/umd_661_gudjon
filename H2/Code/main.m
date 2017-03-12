
OutputPath = '../Output/';
Nodes = csvread('../Data/rand1_nodes.txt');
Edges = csvread('../Data/rand1_edges.txt');


%% Problem 1
start = 772;
goal = 386;
w = 1.0;

Path = aStar(Nodes, Edges, start, goal, w);
writePath([OutputPath, 'problem1.txt'], Path);

%% Problem 2
start = 643;
goal = 608;
w = 10.0;

Path = aStar(Nodes, Edges, start, goal, w);
writePath([OutputPath, 'problem2.txt'], Path);

%% Problem 3
start = 596;
goal = 609;
w = 2.0;

Path = aStar(Nodes, Edges, start, goal, w);
writePath([OutputPath, 'problem3.txt'], Path);

%% Problem 4
start = 772;
goal = 386;
w = 100.0;

Path = aStar(Nodes, Edges, start, goal, w);
writePath([OutputPath, 'problem4.txt'], Path);

%% Problem 5
start = 643;
goal = 608;
w = 100.0;

Path = aStar(Nodes, Edges, start, goal, w);
writePath([OutputPath, 'problem5.txt'], Path);

%% Problem 6
start = 596;
goal = 609;
w = 100.0;

Path = aStar(Nodes, Edges, start, goal, w);
writePath([OutputPath, 'problem6.txt'], Path);