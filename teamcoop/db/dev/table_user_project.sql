create table user_project (id integer primary key,
						   projectId integer not null references project(id) on delete cascade deferrable initially deferred,
						   userId integer not null references user(id) on delete cascade deferrable initially deferred,
						   level integer not null default 2,
						   unique(projectId,userId));