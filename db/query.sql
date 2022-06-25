create table command(
    id integer primary key AUTOINCREMENT,
    name text,
    helptext text,
    parent text,
    content text
);

insert into command (name, helptext, parent, content)
select
    json_extract(value, '$.name') as name,
    json_extract(value, '$.helptext') as helptext,
    json_extract(value, '$.parent') as parent,
    json_extract(value, '$.content') as content
from
    json_each(readfile('commands.json'))
;
