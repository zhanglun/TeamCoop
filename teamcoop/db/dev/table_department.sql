create table department (id integer primary key unique,
						 depName text not null default '',
						 parentId integer not null default 0);