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
