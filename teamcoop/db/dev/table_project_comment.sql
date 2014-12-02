create table project_comment (id integer primary key unique,
							  content text not null default '',
							  projectId integer not null references project(id) on delete cascade deferrable initially deferred,
							  userId integer not null references user(id) on delete cascade deferrable initially deferred,
							  createtime timestamp not null default (datetime(current_timestamp,'localtime')));