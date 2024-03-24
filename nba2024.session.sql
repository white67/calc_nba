select *
from matches
order by match_date;

-- @block xdd
select * from stats where match_id = 922;

-- @block duplicate table, create backup
CREATE TABLE matches_backup AS SELECT * FROM matches;
CREATE TABLE stats_backup AS SELECT * FROM stats;
CREATE TABLE players_backup AS SELECT * FROM players;

-- @block
SELECT *
FROM stats
where match_id is null;

-- @block odds
create table odds (
    bet_id int not null auto_increment primary key,
    match_id int,
    refers_single_player boolean,
    refers_multiple_players boolean,
    player_id int,
    bet_name varchar(255),
    bet_outcome varchar(255),
    odd_value DECIMAL(10, 2),
    active_status boolean,


);
