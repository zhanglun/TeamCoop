create table task (id integer primary key unique,
				   title text not null,
				   description text not null default '',
				   deadline timestamp not null default (datetime(current_timestamp,'localtime')),
				   executeUserId integer not null default 0 references user(id) on delete set default deferrable initially immediate,
				   createUserId integer not null default 0 references user(id) on delete set default deferrable initially immediate,
				   status integer not null default 1,
				   createtime timestamp not null default (datetime(current_timestamp,'localtime')));