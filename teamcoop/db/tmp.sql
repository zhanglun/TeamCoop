PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (id integer primary key unique,
				   username text not null unique,
				   password text not null,
				   level integer not null default 2,
				   name text not null default '',
				   gender text not null default '',
				   email text not null default '',
				   createtime timestamp not null default (datetime(current_timestamp,'localtime')));
INSERT INTO "user" VALUES(1,'admin','123456',1,'','','','2014-12-03 05:53:17.380000');
INSERT INTO "user" VALUES(2,'zhanglun','123456',2,'','','','2014-12-04 01:17:44.124000');
INSERT INTO "user" VALUES(3,'','123456',2,'','','','2014-12-04 01:19:25.412000');
INSERT INTO "user" VALUES(4,'mute','123456',2,'','','','2014-12-04 02:04:21.948000');
CREATE TABLE department (id integer primary key unique,
						 depName text not null default '',
						 parentId integer not null default 0);
CREATE TABLE project (id integer primary key unique,
					  title text not null,
					  description text not null,
					  level integer not null default 1,
					  deadline date not null default (datetime(current_date,'localtime')),
					  status integer not null default 1,
					  isPublic integer not null default 1,
					  createUserId integer not null,
					  createtime timestamp not null default (datetime(current_timestamp,'localtime')),
					  unique(title));
/**** ERROR: (11) database disk image is malformed *****/
/**** ERROR: (11) database disk image is malformed *****/
CREATE TABLE task (id integer primary key unique,
				   title text not null,
				   description text not null default '',
				   deadline timestamp not null default (datetime(current_timestamp,'localtime')),
				   executeUserId integer not null references user(id) on delete cascade deferrable initially deferred,
				   createUserId integer not null references user(id) on delete cascade deferrable initially deferred,
				   status integer not null default 1,
				   createtime timestamp not null default (datetime(current_timestamp,'localtime')));
CREATE TABLE user_department (id integer primary key unique,
							  departmentId integer not null references department(id) on delete cascade deferrable initially deferred,
							  userId integer not null references user(id) on delete cascade deferrable initially deferred,
							  unique(departmentId,userId));
CREATE TABLE user_project (id integer primary key unique,
						   projectId integer not null references project(id) on delete cascade deferrable initially deferred,
						   userId integer not null references user(id) on delete cascade deferrable initially deferred,
						   level integer not null default 2,
						   unique(projectId,userId));
INSERT INTO "user_project" VALUES(1,25,2,2);
INSERT INTO "user_project" VALUES(2,26,4,2);
INSERT INTO "user_project" VALUES(3,27,2,2);
INSERT INTO "user_project" VALUES(4,28,3,2);
CREATE TABLE project_comment (id integer primary key unique,
							  content text not null default '',
							  projectId integer not null references project(id) on delete cascade deferrable initially deferred,
							  userId integer not null references user(id) on delete cascade deferrable initially deferred,
							  createtime timestamp not null default (datetime(current_timestamp,'localtime')));
CREATE TABLE task_comment (id integer primary key unique,
						   content text not null default '',
						   taskId integer not null references project(id) on delete cascade deferrable initially deferred,
						   userId integer not null references user(id) on delete cascade deferrable initially deferred,
						   createtime timestamp not null default (datetime(current_timestamp,'localtime')));
COMMIT;
