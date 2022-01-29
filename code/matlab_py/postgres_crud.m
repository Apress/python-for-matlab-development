% code/matlab_py/postgres_crud.m
% {{{
% This code accompanies the book _Python for MATLAB Development:
% Extend MATLAB with 300,000+ Modules from the Python Package Index_ 
% ISBN 978-1-4842-7222-0 | ISBN 978-1-4842-7223-7 (eBook)
% DOI 10.1007/978-1-4842-7223-7
% https://github.com/Apress/python-for-matlab-development
% 
% Copyright © 2022 Albert Danial
% 
% MIT License:
% Permission is hereby granted, free of charge, to any person obtaining a copy
% of this software and associated documentation files (the "Software"), to deal
% in the Software without restriction, including without limitation the rights
% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
% copies of the Software, and to permit persons to whom the Software is
% furnished to do so, subject to the following conditions:
% 
% The above copyright notice and this permission notice shall be included in
% all copies or substantial portions of the Software.
% 
% THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
% THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
% FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
% DEALINGS IN THE SOFTWARE.
% }}}
Im = @py.importlib.import_module;
psycopg2 = Im('psycopg2');

conn = psycopg2.connect(pyargs('host','143.198.155.245', ...
             'user','al','password','SuperSecret', ...
             'database','pet_store'));
cur = conn.cursor();

% delete the table if already exists
try
  cur.execute('drop table myvalues');
  conn.commit();
catch EO
  fprintf('Table "myvalues" did not exist, skipping drop.\n')
end

populate_table(conn, cur);
query_results(cur);

rename_pets(cur, 'bunny', 'rabbit');
query_results(cur);

remove_pets(cur, 'cat');
query_results(cur);

cur.execute('drop table myvalues');

conn.close();

function [n, price, pet] = record()
    n = int64(randi([1,15]));
    price = 10.0 + 30*rand();
    pets = {'dog', 'cat','bunny', 'fish', 'horse'};
    pet = pets{randi([1,5])};
end

function populate_table(conn, cur)
    tic;
    cur.execute(['create table myvalues (id serial primary key, ' ...
                'n integer, price float, pet varchar)']);
    batch_size = 300;
    n_records  = 1000;
    batch = py.list();
    insert = 'insert into myvalues (n,price,pet) values(%s,%s,%s)';
    for i = 1:n_records
        [n,price,pet] = record();
        batch.append(py.list({n, price, pet}));
        if ~(mod(i,100))
            fprintf('i = %5d\r', i);
        end
        if length(batch) < batch_size
            continue
        end
        fprintf('i = %5d inserting batch\n', i);
        cur.executemany(insert, batch)
        conn.commit()
        batch = py.list();
    end
    if ~isempty(batch)
        cur.executemany(insert, batch)
        conn.commit()
    end
    fprintf('inserted %d rows in %.3f sec\n', n_records, toc)
end

function query_results(cursor)
    query = 'select sum(price), sum(n), pet from myvalues group by pet';
    cursor.execute(query);
    fprintf('Result of %s:\n', query)
    all = py2mat(cursor.fetchall());
    for i = 1:length(all)
        sum_price = all{i}{1};
        sum_n     = all{i}{2};
        pet       = all{i}{3};
        fprintf('  %.2f  %6d  %7s\n', sum_price, sum_n, pet)
    end
    fprintf(repmat('-',1,60)); fprintf('\n')
end

function rename_pets(cursor, before, after)
    update_cmd = sprintf("update myvalues set pet='%s' where pet='%s'",...
                         after, before);
    cursor.execute(update_cmd);
    fprintf('Did:  %s\n', update_cmd)
end

function remove_pets(cursor, pet)
    delete_cmd = sprintf("delete from myvalues where pet='%s'",pet);
    cursor.execute(delete_cmd)
    fprintf('Did:  %s\n', delete_cmd)
end
