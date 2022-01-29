% code/mesh/FE_model.m
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
classdef FE_model
    properties
        E
        R
        rho
        nodes
        conn
        ndof
        nelem
        elem
    end
    methods
        function M = FE_model(model_file_base, E, rho)
            Tstart = tic;
            M.E = E;
            M.rho = rho;
            x = load_model(model_file_base);
            fprintf('FE_model load triangle : %7.3f sec (%s)\n',...
                toc(Tstart), model_file_base);
            Tstart = tic;
            M.nodes = x.vertices;
            M.conn  = connectivity(M, x.triangles);
            M.ndof  = 2*size(M.nodes,1);
            M.R = sqrt(sqrt(2/M.ndof));  % rod cross section edge length
            M.nelem = size(M.conn, 1);
            null_elem = Rod_Elem(0,Node(0,0,0),Node(0,0,0),0,0,0);
            M.elem = repmat(null_elem, M.nelem, 1);  % preallocate
            for k = 1:M.nelem
                IJ = M.conn(k,:);
                nA = Node( IJ(1), M.nodes(IJ(1),1),  M.nodes(IJ(1),2) );
                nB = Node( IJ(2), M.nodes(IJ(2),1),  M.nodes(IJ(2),2) );
                M.elem(k) = Rod_Elem(k, nA, nB, M.R, M.E, rho);
            end
            fprintf('FE_model triangle->rod : %7.3f sec\n', toc(Tstart));
        end
        function pair = ascending(~, i,j)
            if i < j
                pair = [i j];
            else
                pair = [j i];
            end
        end
        function conn = connectivity(self, tri)
            % Given an n x 3 array of triangle node ID's,
            % return an m x 2 array of rod node ID's.
            n_tri = size(tri,1);
            conn = zeros(3*n_tri, 2); % will have duplicates
            i = 0;
            for j = 1:n_tri
                conn(i+1,:) = ascending(self, tri(j,1), tri(j,2));
                conn(i+2,:) = ascending(self, tri(j,2), tri(j,3));
                conn(i+3,:) = ascending(self, tri(j,3), tri(j,1));
                i = i + 3;
            end
            conn = unique(conn, 'rows');
        end
        function [kV, I, J, M, ptr] = add_element(self, eid, kV, I, J, M, ptr)
            nid_A = self.elem(eid).node_a.id;
            nid_B = self.elem(eid).node_b.id;

            % nAx,nAy,nBx,nBy are global row and column indices
            % (aka degree of freedom IDs).  Their values are
            % based on node ID (integers from 1..nNodes) where
            % each node has two degrees of freedom.
            nAx = 2*nid_A - 1; nAy = nAx + 1;
            nBx = 2*nid_B - 1; nBy = nBx + 1;
            I(ptr   ) = nAx; J(ptr   ) = nAx;
            I(ptr+ 1) = nAx; J(ptr+ 1) = nAy;
            I(ptr+ 2) = nAx; J(ptr+ 2) = nBx;
            I(ptr+ 3) = nAx; J(ptr+ 3) = nBy;

            I(ptr+ 4) = nAy; J(ptr+ 4) = nAx;
            I(ptr+ 5) = nAy; J(ptr+ 5) = nAy;
            I(ptr+ 6) = nAy; J(ptr+ 6) = nBx;
            I(ptr+ 7) = nAy; J(ptr+ 7) = nBy;

            I(ptr+ 8) = nBx; J(ptr+ 8) = nAx;
            I(ptr+ 9) = nBx; J(ptr+ 9) = nAy;
            I(ptr+10) = nBx; J(ptr+10) = nBx;
            I(ptr+11) = nBx; J(ptr+11) = nBy;

            I(ptr+12) = nBy; J(ptr+12) = nAx;
            I(ptr+13) = nBy; J(ptr+13) = nAy;
            I(ptr+14) = nBy; J(ptr+14) = nBx;
            I(ptr+15) = nBy; J(ptr+15) = nBy;

            k = self.elem(eid).stiffness_matrix();
            kV(ptr:ptr+15) = k(:); % as a linear array
            ptr = ptr + 16;
            dof = [2*nid_A-1, 2*nid_A, 2*nid_B-1, 2*nid_B ];
%fprintf('Aid= %d  Bid= %d dof=',nid_A, nid_B); dof
            M(dof) = M(dof) + self.elem(eid).mass_matrix();
        end
        function [I_cst, J_cst, V_cst, n_cst_DOF, u_to_c] = constrain_dof(self, fixed_dof, I, J, V)
            c_to_u = []; % c_to_u[ constrained set dof   ] = unconstrained set dof
            u_to_c = containers.Map('KeyType','uint64','ValueType','uint64');
            % u_to_c[ unconstrained set dof ] = constrained set dof
            I_cst = []; J_cst = []; V_cst = [];
            seen_it = containers.Map('KeyType','uint64','ValueType','logical');
            c_dof = 0;
            ic2u = 1;
            for i = 1:length(I)
                if isKey(fixed_dof, I(i)) || ...
                   isKey(fixed_dof, J(i)) || isKey(seen_it, I(i))
                    continue
                end
                c_dof = c_dof + 1;
                c_to_u(ic2u) = I(i);
                ic2u = ic2u + 1;
                u_to_c(I(i)) = c_dof;
                seen_it(I(i)) = true;
            end
            clear seen_it;
            n_cst_DOF = length(c_to_u);
            n = 1;
            for i = 1:length(I)
                if isKey(fixed_dof, I(i)) || isKey(fixed_dof, J(i))
                    continue
                end
                I_cst(n) =  u_to_c(I(i));
                J_cst(n) =  u_to_c(J(i));
                V_cst(n) =  V(i);
                n = n + 1;
            end
        end
        function [K, M, u_to_c] = KM(self, constrained_dof_list)
            % Return global stiffness and mass matrices, K and M.
            % Iterates over each element & adds its k & m to the
            % global matrices.
            Tstart = tic;
            nDof  = 2*size(self.nodes, 1);
            nElem =   size(self.elem , 1);
            nonZeros = 4*4*nElem;
            fprintf('KM(): %d dof, %d elements\n', nDof, nElem)
            I  = zeros(nonZeros,1); % sparse row indices
            J  = zeros(nonZeros,1); % sparse col indices
            kV = zeros(nonZeros,1); % sparse stiffness terms
            M  = zeros(nDof,1);     % diagonal mass matrix

            ptr= 1;                 % offset into I,J,kV
            for eid = 1:size(self.elem,1)
                [kV, I, J, M, ptr] = self.add_element(eid, kV, I, J, M, ptr);
            end
            if length(constrained_dof_list)
                fixed_dof = containers.Map('KeyType','uint64','ValueType','logical');
                for dof = constrained_dof_list
                    fixed_dof(dof) = true;
                end
                [I_cst, J_cst, V_cst, n_cst_Dof, u_to_c] = self.constrain_dof(fixed_dof, I, J, kV);
                K = sparse(I_cst, J_cst, V_cst, n_cst_Dof, n_cst_Dof);
                M = spdiags(M(I_cst), 0, n_cst_Dof, n_cst_Dof);
            else
                K = sparse(I, J, kV, nDof, nDof);
                M = spdiags(M, 0, nDof, nDof);
                u_to_c = [];
            end
            fprintf('FE_model generate K,M  : %7.3f sec\n', toc(Tstart));
        end
    end
end
