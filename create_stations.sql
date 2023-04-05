-- Create temporary table for Tools
CREATE TEMP TABLE IF NOT EXISTS Tools(
    ToolID INT,
    Name VARCHAR(250),
    JsonFile VARCHAR(100),
    StationName VARCHAR(100)
);
DO $$
-- Declare variables
DECLARE 
    SName VARCHAR(250);
    SID INT; 
    TID INT;
BEGIN
    -- Set values for variables
    SName := 'Station 1';
    
    -- Get max StationID and ToolID from parent tables
    SELECT MAX("StationID") + 1 INTO SID FROM public.servicemanager_station;
    SELECT MAX("ToolID") + 1 INTO TID FROM public.servicemanager_tool;
    
    IF(SELECT id FROM public.servicemanager_station WHERE "Name" = SName) IS NULL THEN
        -- Insert data into servicemanager_station
        INSERT INTO public.servicemanager_station(
            id, "StationID", "Name", "Desc", "CreatedBy", "IsActive")
        VALUES (SID, SID, SName, SUBSTRING(SName,0,3), null, true)
        RETURNING id INTO SID;

        -- Insert data into Tools temporary table
        INSERT INTO Tools(ToolID,Name,JsonFile,StationName) 
        VALUES (TID, 'Tool1', 'Tool1.json', SName),
               (TID + 1, 'Tool2', 'Tool2.json', SName),
               (TID + 2, 'Tool3', 'Tool3.json', SName);

        -- Insert data into servicemanager_tool from Tools temporary table
        INSERT INTO public.servicemanager_tool(
            "ToolID", "Name", "JsonFile", "StationName")
        SELECT ToolID, Name, JsonFile, StationName FROM Tools;

        -- Print the inserted identity (StationID)
        RAISE NOTICE 'Inserted StationID: %', SID;
        DROP TABLE Tools;
    ELSE
        RAISE NOTICE 'Station already exists: %', SName;
    END IF;
END $$;