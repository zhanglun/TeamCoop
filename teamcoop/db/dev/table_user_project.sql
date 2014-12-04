create table user_project (id integer primary key unique,
						   projectId integer not null references project(id) on delete cascade deferrable initially immediate,
						   userId integer not null references user(id) on delete cascade deferrable initially immediate,
						   level integer not null default 2,
						   unique(projectId,userId));