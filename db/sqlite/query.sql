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

create table phone_number(
    id integer primary key AUTOINCREMENT,
    command_id integer,
    phone_number text    
);

insert into phone_number (command_id, phone_number)
with phone_numbers as(
    select
        json_extract(value, '$.name') as name,
        json_extract(value, '$.phone_number') as phone_number
    from
        json_each(readfile('commands.json'))
)
select
    id,
    phone_number
from
    phone_numbers pn
    join command c on pn.name=c.name
;
