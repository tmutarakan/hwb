create table command(
    id integer primary key AUTOINCREMENT,
    name text,
    message text,
    parent text,
    content text
);

insert into command (name, message, parent, content)
select
    json_extract(value, '$.name') as name,
    json_extract(value, '$.message') as message,
    json_extract(value, '$.parent') as parent,
    json_extract(value, '$.content') as content
from
    json_each(readfile('commands.json'))
;

create table file_path(
    id integer primary key AUTOINCREMENT,
    command_id integer,
    path text    
);

insert into file_path (command_id, path)
with paths as(
    select
        json_extract(value, '$.name') as name,
        json_extract(value, '$.path') as path
    from
        json_each(readfile('files.json'))
)
select
    id,
    path
from
    paths p
    join command c on p.name=c.name
;
