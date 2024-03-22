select *
from matches;

-- @block xdd
select * from stats where match_id = 922;

-- @block duplicate table, create backup
CREATE TABLE matches_backup AS SELECT * FROM matches;
CREATE TABLE stats_backup AS SELECT * FROM stats;
CREATE TABLE players_backup AS SELECT * FROM players;

