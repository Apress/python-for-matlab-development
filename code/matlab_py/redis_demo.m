% code/matlab_py/redis_demo.m
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
main()

function [clean] = redis_str(x)
  % Input is a Python byte array returned by the Python Redis module.
  % Returns a MATLAB string.
  % example   x = py.bytes([uint8(56), uint8(46), uint8(57), uint8(53)])
  %       clean = "8.95"
  clean = char( x );
  clean = string(clean(3:end-1));  % strip leading 'b' and trailing '
end

function main()
  redis = py.importlib.import_module('redis');
  R = redis.Redis(pyargs('host','localhost','port',int64(6379)));
  try
    R.ping();
  catch EO
    fprintf('Is Redis running?  Unable to connect: %s\n', EO.message)
    return
  end
  
  fprintf('Connected to server.')
  R.config_set('notify-keyspace-events', 'KEA');
  mapping = struct;
  mapping.X = 8.9655;
  mapping.month = 'Feb';
  R.mset(mapping)
  
  retrieved_X     = redis_str(R.get('X'));
  retrieved_month = redis_str(R.get('month'));
  
  fprintf('Got X = %s\n', retrieved_X);
  fprintf('Got month = %s\n', retrieved_month);
  
  Sub = R.pubsub();
  Sub.psubscribe('__keyspace@0__:*')
  i = 1;
  while 1
   try
       message = Sub.get_message();
   catch EO
       fprintf('lost connection to server: %s\n', EO.message)
       break
   end
   if message == py.None
     pause(0.01)
     continue
   end
   keyname = replace(redis_str(message{'channel'}), '__keyspace@0__:', '');
   if keyname == '*'
     % initial subscription value
     continue
   end
   value = redis_str(R.get(keyname));
   fprintf('%s = %s\n', keyname, value)
  end

end
