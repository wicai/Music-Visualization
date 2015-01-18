drop table if exists features;
create table features (
	"song_id" text primary key not null,
	"name" text not null,
	"artist" text not null,
	"acousticness" real not null,
	"danceability" real not null,
	"duration" integer not null,
	"energy" real not null,
	"liveness" real not null,
	"loudness" real not null,
	"mode" integer not null,
	"speechiness" real not null,
	"tempo" integer not null
);