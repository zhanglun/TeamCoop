create table task_comment (id integer primary key autoincrement,
						   content text not null default '',
						   taskId integer not null references project(id) on delete cascade deferrable initially deferred,
						   userId integer not null references user(id) on delete cascade deferrable initially deferred,
						   createtime timestamp not null default (datetime(current_timestamp,'localtime')));