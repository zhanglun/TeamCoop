create table user (id integer primary key unique,
				   username text not null unique,
				   password text not null default '123456',
				   level integer not null default 2,
				   name text not null default '',
				   gender text not null default '',
				   email text not null default '',
				   createtime timestamp not null default (datetime(current_timestamp,'localtime')));