c code/f2py/mb.f
c {{{
c This code accompanies the book _Python for MATLAB Development:
c Extend MATLAB with 300,000+ Modules from the Python Package Index_ 
c ISBN 978-1-4842-7222-0 | ISBN 978-1-4842-7223-7 (eBook)
c DOI 10.1007/978-1-4842-7223-7
c https://github.com/Apress/python-for-matlab-development
c 
c Copyright © 2022 Albert Danial
c 
c MIT License:
c Permission is hereby granted, free of charge, to any person obtaining a copy
c of this software and associated documentation files (the "Software"), to deal
c in the Software without restriction, including without limitation the rights
c to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
c copies of the Software, and to permit persons to whom the Software is
c furnished to do so, subject to the following conditions:
c 
c The above copyright notice and this permission notice shall be included in
c all copies or substantial portions of the Software.
c 
c THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
c IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
c FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
c THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
c LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
c FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
c DEALINGS IN THE SOFTWARE.
c }}}
      integer function nIter(c, imax)
cf2py intent(in)   :: c, imax
cf2py intent(out)  :: nIter
      implicit none
      complex*16 z, c
      integer i, imax
      nIter = imax
      z = 0
      do i = 0,imax - 1
        z = z*z + c
c       write(6,*) '   niter i=',i,'  c=',c,'  z=',z
        if (zabs(z) .gt. 2.0) then
          nIter = i
          return
        endif
      enddo
      nIter = imax
      end

      subroutine MB(nR, nC, Re, Im, img, imax)
cf2py intent(in)   :: Re, Im, imax
cf2py intent(out)  :: img
cf2py intent(hide) :: nR, nC
      implicit none
      integer nR, nC, nIter, imax, i, j, ij
      integer(kind=2) img(nR*nC)
      real*8 Re(nR), Im(nC)
      complex*16 c
      do i = 1,nR
        do j = 1,nC
          c = cmplx(Re(i), Im(j))
          ij = (i-1)*nC+j
          img(ij) = nIter(c,imax)
c         write(6,*) 'MB[',i,',',j,'] Re(',i,')=',Re(i),' Im(',j,')=',
c    .               Im(j),'  nIter=',img(ij)
        enddo
      enddo
      end
