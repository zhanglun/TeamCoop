create table task (id integer primary key unique,
				   title text not null default '',
				   description text not null default '',
				   deadline timestamp not null default (datetime(current_timestamp,'localtime')),
				   executeUserId integer not null references user(id) on delete cascade deferrable initially deferred,
				   createUserId integer not null references user(id) on delete cascade deferrable initially deferred,
				   status integer not null default 1,
				   createtime timestamp not null default (datetime(current_timestamp,'localtime')));