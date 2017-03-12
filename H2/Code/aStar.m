function [ Path ] = aStar( Nodes, Edges, startId, goalId, w )

numNodes = length(Nodes);
Visited = false(numNodes, 1);
Parent = zeros(numNodes, 1);
Cost = Inf(numNodes, 1);
H = Inf(numNodes, 1);

Cost(startId) = 0;
H(startId) = norm(Nodes(startId, :) - Nodes(goalId, :));

%% Main loop
nodeId = startId;
while nodeId ~= goalId
    E = Edges(Edges(:, 1)==nodeId, :);
    Visited(nodeId) = true;
    
    % Evaluate node neighbors and add to queue
    for i = 1:size(E, 1)
        nid = E(i, 2);
        cost = Cost(nodeId) + E(i, 3);
        
        % Update cost to this node
        if cost < Cost(nid)
           Cost(nid) = cost;
           Parent(nid) = nodeId;
        end
        
        % Calculate heuristic
        h = norm(Nodes(nid, :) - Nodes(goalId, :));
        H(nid) = h;
    end
    
    % Pick node that has lowest expected cost to goal
    % and has not been visited already
    C = Cost + (H*w);
    Idx = 1:numNodes;
    
    Idx = Idx(~Visited);
    C = C(~Visited);
    [~, minIdx] = min(C);
    
    nodeId = Idx(minIdx);
end

fprintf('Nodes Visitied: %i\n', sum(Visited));

%% Trace parent pointers backwards
Path = [goalId];
id = goalId;
while id ~= startId
    id = Parent(id);
    Path(end+1) = id;
end

Path = flip(Path);

end

