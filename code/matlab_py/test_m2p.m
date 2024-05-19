% A. Danial 2023-09-15
% Test mat2py() conversions via circular trip to py2mat().
T = py.importlib.import_module('test_p2m');
py_tuple = T.a_tuple();
py_list = T.a_list();
py_dict = T.a_dict();
py_nested_dict = T.nested_dict();
py_i32_array   = T.i32_array();  
py_i64_array   = T.i64_array();
py_f32_array   = T.f32_array();
py_f64_array   = T.f64_array();
py_c64_array   = T.c64_array();
py_c128_array  = T.c128_array();

MAR1 = datetime(2022,3,1,12,13,14,654.321);

ref_R = {12, "three", 4.4, MAR1 };
R = py2mat(mat2py(ref_R));
for i = 1:length(ref_R)
    assert(ref_R{i} == R{i}, sprintf("cell item %d", i))
end
fprintf('cell......................PASS\n')

R = py2mat(mat2py(ref_R));   % expect same result as tuple
for i = 1:length(ref_R)
    assert(ref_R{i} == R{i}, sprintf("py_list item %d", i))
end
fprintf('list......................PASS\n')

ref_R = struct;
ref_R.a = 12;
ref_R.b = "three";
ref_R.c = 4.4;
ref_R.d = MAR1;
R = py2mat(mat2py(ref_R));   % pre 2023a returns a struct
keys = fieldnames(ref_R);
for i = 1:length(keys)
    assert(ref_R.(keys{i}) == R.(keys{i}), sprintf("py_dict key %s", keys{i}))
end
fprintf('dict......................PASS\n')

ref_R = int32(fix(reshape(-12.5:2.1:12.5, 4,3)'));
R = py2mat(mat2py(ref_R));
assert( max(abs(R - ref_R), [], 'all') == 0)
fprintf('int32 matrix..............PASS\n')

ref_R = int64(fix(reshape(-12.5:2.1:12.5, 4,3)'));
R = py2mat(mat2py(ref_R));
assert( max(abs(R - ref_R), [], 'all') == 0)
fprintf('int64 matrix..............PASS\n')

ref_R = single(reshape(-12.5:2.1:12.5, 4,3)');
R = py2mat(mat2py(ref_R));
assert( max(abs(R - ref_R), [], 'all') < 4.0e-6)
fprintf('single matrix.............PASS\n')

ref_R = reshape(-12.5:2.1:12.5, 4,3)'; % default type is double
R = py2mat(mat2py(ref_R)); 
assert( max(abs(R - ref_R), [], 'all') < 8.0e-15, 'double matrix')
fprintf('double matrix.............PASS\n')

ref_R =   single(reshape(-12.5:2.1:12.5, 4,3)') - ...
        j*single(reshape(-12.5:2.1:12.5, 4,3)');
R = py2mat(mat2py(ref_R));
assert( (max(abs(real(R-ref_R)), [], 'all') < 4.0e-6) && ...
        (max(abs(imag(R-ref_R)), [], 'all') < 4.0e-6), ...
        'complex single matrix')
fprintf('complex single matrix.....PASS\n')

ref_R =   reshape(-12.5:2.1:12.5, 4,3)' - ...
        j*reshape(-12.5:2.1:12.5, 4,3)';
R = py2mat(mat2py(ref_R));
assert( (max(abs(real(R-ref_R)), [], 'all') < 8.0e-15) && ...
        (max(abs(imag(R-ref_R)), [], 'all') < 8.0e-15), ...
        'complex double matrix')
fprintf('complex double matrix.....PASS\n')

fprintf('Performance test...\n')
n_iter = 1024;
n_rand = 32768;
x_mat = randn(n_rand, 1);
tic;
for i = 1:n_iter
    x_py = mat2py(x_mat);
end
elapsed_s = toc;
fprintf('%d passes of mat2py() of a %d array took %.3f seconds\n', ...
          n_iter, n_rand, elapsed_s)
