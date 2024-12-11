-- Creating table player_history (CDC will be UP)
CREATE TABLE public.player_history (
    player_id integer, signed_date date, team_full_name char(30), team_acr char(5)
);

-- Creating table goal_history (CDC will be UP)
CREATE TABLE public.goal_history (
    player_id integer, scorer_team_acr char(5), opp_team_acr char(5)
);

-- Creating table points_table (CDC will not be UP)
CREATE TABLE public.points_table (
    team_id integer, team_acr char(5), games_won integer, games_lost integer, games_drawn integer 
);

-- Adding logical replication to all the tables
ALTER TABLE public.player_history REPLICA IDENTITY FULL;

ALTER TABLE public.goal_history REPLICA IDENTITY FULL;

ALTER TABLE public.points_table REPLICA IDENTITY FULL;


-- First insert, right after creating the connector

INSERT INTO public.player_history
(player_id, signed_date, team_full_name, team_acr) 
VALUES (1, '1999-07-12', 'Manchester United', 'MUFC');

INSERT INTO public.goal_history
(player_id, scorer_team_acr, opp_team_acr) 
VALUES (1, 'MUFC', 'RM');

INSERT INTO public.points_table
(team_id, team_acr, games_won, games_lost, games_drawn) 
VALUES (1, 'MUFC', 2, 1, 2);


-- Insert after starting the CDC
INSERT INTO public.player_history
(player_id, signed_date, team_full_name, team_acr) 
VALUES (2, '2004-11-19', 'Paris Saint-Germain', 'PSG');

INSERT INTO public.goal_history
(player_id, scorer_team_acr, opp_team_acr) 
VALUES (2, 'PSG', 'MUFC');

INSERT INTO public.points_table
(team_id, team_acr, games_won, games_lost, games_drawn) 
VALUES (1, 'PSG', 3, 1, 1);

-- updating records in the two tables to capture updates
UPDATE public.player_history
SET signed_date = '2006-11-19'
WHERE player_id = 2;

UPDATE public.goal_history
SET opp_team_acr = 'RM'
WHERE player_id = 2;