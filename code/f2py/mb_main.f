c code/f2py/mb_main.f
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
c gfortran -Ofast mb_main.f

      integer function nIter(c, imax)
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
      implicit none
      integer nR, nC, nIter, imax, i, j, ij
      integer(kind=2) img(nR*nC)
      real*8 Re(nR), Im(nC)
      complex*16 c
      do i = 1,nR
        do j = 1,nC
          c = cmplx(Re(j), Im(i))
          ij = (i-1)*nC+j
          img(ij) = nIter(c,imax)
c         write(6,*) 'MB[',i,',',j,'] c=',c,'  nIter=',img(ij)
        enddo
      enddo
      end

      subroutine linspace(x_start, x_end, n, X)
      implicit none
      integer n, i
      real*4 x_start, x_end
      real*8 delta, X(n)

      delta = (x_end - x_start)/(n-1)
      do i = 0,n-1
        X(i+1) = x_start + i*delta
c       write(6,*) 'X(',i+1,')=',X(i+1)
      enddo
      return
      end

      program main
      implicit none
      integer NMAX
      parameter(NMAX=5000)
      integer imax, nIter, nR, nC, i, ij
      integer(kind=2) img(NMAX*NMAX)
      complex*16 c
      real*8 Re(NMAX), Im(NMAX), t_start, t_end
      real elapsed_s, etime, TM(2)
      integer case(5)

      imax = 255

      case(1) =  500
      case(2) = 1000
      case(3) = 2000
      case(4) = 5000

      do i = i,4

      nR = case(i)
      nC = case(i)

      img = 0
      elapsed_s = etime( TM )
      call linspace(-0.7440, -0.7433, nC, Re)
      call linspace( 0.1315,  0.1322, nR, Im)
      call MB(nR, nC, Re, Im, img, imax)
      elapsed_s = etime( TM )
      write(6,*) 'N=',nR,'  elapsed seconds =',elapsed_s

c     open(unit=9, file='f_image.bin',form='unformatted',
c    .     access='stream', status='replace')
c     write(9) (img(ij),ij=1,nC*nR)
c     close(9)

      enddo

c     do i = 1,nR
c       write(6,'( 10i4)') (img(ij),ij=(i-1)*nC+1,(i-1)*nC+nC)
c     enddo
      
      end
