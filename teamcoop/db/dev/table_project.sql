create table project (id integer primary key unique,
					  title text not null,
					  description text not null,
					  level integer not null default 1,
					  deadline date not null default (datetime(current_date,'localtime')),
					  status integer not null default 1,
					  isPublic integer not null default 1,
					  createUserId integer not null,
					  createtime timestamp not null default (datetime(current_timestamp,'localtime')),
					  unique(title));