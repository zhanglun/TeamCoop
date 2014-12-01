create table user (id integer primary key autoincrement unique,
				   username text not null unique,
				   password text not null,
				   name text not null default '',
				   gender text not null default '',
				   phone text not null default '',
				   email text not null default '',
				   createtime timestamp not null default (datetime(current_timestamp,'localtime')),
				   check(length(phone) > 10));