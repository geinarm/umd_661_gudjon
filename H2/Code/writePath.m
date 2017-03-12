function [ ] = writePath( FileName, Path )

    fileID = fopen(FileName,'w');
    for i = 1:length(Path)
       fprintf(fileID,'%i\n', Path(i)); 
    end

end

