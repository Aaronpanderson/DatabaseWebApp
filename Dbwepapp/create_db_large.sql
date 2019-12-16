drop table if exists teams cascade;
create table teams (
  teamname varchar(40),
  region varchar(5),
  primary key  (teamname)
);

drop table if exists players cascade;
create table players (
  playername varchar(40),
  teamname varchar(40),
  age int,
  primary key (playername),
  foreign key (teamname) references teams
);

drop table if exists tournaments cascade;
create table tournaments (
  tournamentname varchar(40),
  tournamentregion varchar(5),
  tournamentyear int,
  primary key (tournamentname)
);

drop table if exists tournamentwinners;
create table tournamentwinners (
  tournamentname varchar(40),
  teamname varchar(40) not null,
  primary key (tournamentname, teamname),
  foreign key (tournamentname) references tournaments,
  foreign key (teamname) references teams
);

drop table if exists patches cascade;
create table patches (
  patchID varchar(4),
  patchdate date not null,
  primary key (patchID)
);

drop table if exists coaches;
create table coaches (
  coachname varchar(40),
  teamname varchar(40),
  age int,
  primary key (coachname),
  foreign key (teamname) references teams
);

drop table if exists commentators cascade;
create table commentators (
  commentatorname varchar(40),
  commentatorlanguage varchar(15),
  primary key (commentatorname)
);

drop table if exists matches cascade;
create table matches (
  matchID int,
  tournamentname varchar(40),
  patchID varchar(4) not null,
  duration time not null,
  primary key (matchID),
  foreign key (tournamentname) references tournaments,
  foreign key (patchID) references patches
);

drop table if exists matchteams;
create table matchteams (
  matchID int,
  teamname varchar(40) not null,
  primary key (matchID, teamname),
  foreign key (matchID) references matches,
  foreign key (teamname) references teams
);

drop table if exists matchcommentators;
create table matchcommentators (
  matchID int,
  commentatorname varchar(40) not null,
  primary key (matchID, commentatorname),
  foreign key (matchID) references matches,
  foreign key (commentatorname) references commentators
);

drop table if exists matchwinner;
create table matchwinner (
  matchID int,
  teamname varchar(40) not null,
  primary key (matchID, teamname),
  foreign key (matchID) references matches,
  foreign key (teamname) references teams
);

drop table if exists heroes cascade;
create table heroes (
  heroname varchar(40),
  attribute varchar(15) not null,
  health int not null,
  damage int not null,
  primary key (heroname)
);

drop table if exists matchplayerresults;
create table matchplayerresults (
  matchID int,
  playername varchar(40) not null,
  heroname  varchar(40) not null,
  kills int not null,
  deaths int not null,
  primary key (matchID, playername),
  foreign key (matchID) references matches,
  foreign key (playername) references players,
  foreign key (heroname) references heroes
);
