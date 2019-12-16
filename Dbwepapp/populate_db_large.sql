\copy teams from 'data/teams.csv' DELIMITER ',';

\copy players from 'data/players.csv' DELIMITER ',';

\copy tournaments from 'data/tournaments.csv' DELIMITER ',';

\copy tournamentwinners from 'data/tournamentwinners.csv' DELIMITER ',';

insert into patches
values ('7.15', '2019-06-26'),
('7.14', '2019-05-26'),
('7.13', '2019-04-26'),
('7.12', '2019-03-26'),
('7.11', '2019-02-26'),
('7.10', '2019-01-26'),
('7.09', '2018-06-26'),
('7.08', '2018-04-26'),
('7.06', '2018-03-26'),
('7.05', '2018-02-26'),
('7.04', '2018-01-26'),
('7.03', '2017-07-26'),
('7.02', '2017-04-26'),
('7.01', '2017-03-26'),
('7.00', '2016-06-26'),
('6.83', '2016-01-26'),
('6.82', '2015-06-26'),
('6.81', '2014-06-26'),
('6.80', '2013-06-26'),
('6.79', '2012-06-26'),
('6.78', '2011-06-26');

\copy coaches from 'data/coaches.csv' DELIMITER ',';

\copy commentators from 'data/commentators.csv' DELIMITER ',';

\copy matches from 'data/matches.csv' DELIMITER ',';

\copy matchteams from 'data/matchteams.csv' DELIMITER ',';

\copy matchcommentators from 'data/matchcommentators.csv' DELIMITER ',';

\copy matchwinner from 'data/matchwinners.csv' DELIMITER ',';

\copy heroes from 'data/heroes.csv' DELIMITER ',';

\copy matchplayerresults from 'data/matchplayerresults.csv' DELIMITER ',';
