create table user_department (id integer primary key unique,
							  departmentId integer not null references department(id) on delete cascade deferrable initially immediate,
							  userId integer not null references user(id) on delete cascade deferrable initially immediate,
							  createtime timestamp not null default (datetime(current_timestamp,'localtime')),
							  unique(departmentId,userId));