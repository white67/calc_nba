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

-- @block bets
create table bets (
    bet_id int not null auto_increment primary key,
    bet_name varchar(255),
    outcome varchar(255),
    odds_value DECIMAL(10, 2),
    player_id int,
    match_id int,
    refers_single_player boolean,
    refers_multiple_players boolean,
    active_status boolean,
    bet_full_info text,
    foreign key (player_id) references players(player_id),
    foreign key (match_id) references matches(match_id)
);

-- @block xdd
ALTER TABLE bets
ADD bet_full_info text;

-- @block deleting
drop table bets_assigned;
drop table bets;

-- @block new
CREATE TABLE bets_assigned (
    bet_id INT,
    player_id INT,
    FOREIGN KEY (bet_id) REFERENCES bets(bet_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- @block drop
drop table matches_backup;
drop table players_backup;
drop table stats_backup;