create table task_comment (id integer primary key unique,
						   content text not null default '',
						   taskId integer not null references project(id) on delete cascade deferrable initially immediate,
						   userId integer not null references user(id) on delete cascade deferrable initially immediate,
						   createtime timestamp not null default (datetime(current_timestamp,'localtime')));