# Errata for *Python for MATLAB Development*

On **page 178** [Python code can be debugged in MATLAB with VS Code]:

The sentence "Troubleshooting hybrid MATLAB/Python code can be a challenge
because the MATLAB debugger won’t step into Python code."
should be amended to read
"The VS Code IDE can be used to debug
hybrid MATLAB/Python code; details are explained at
https://www.mathworks.com/matlabcentral/answers/1645680-how-can-i-debug-python-code-using-matlab-s-python-interface-and-visual-studio-code?s_tid=srchtitle"

[Sean de Wolski, MathWorks]

***

On **page 598** [``parfor`` is included with the core MATLAB product]:

MATLAB's parallel for-loop construct ``parfor`` was added to
the core MATLAB product sometime after release 2018a.

[Sean de Wolski, MathWorks]

***

On **page 138** [``datestr`` should be replaced by the newer ``datetime``]:

MATLAB's ``datetime`` function has improved handling of date formatting
and should replace ``datestr``.  Section 5.1.2 and Table 5-1 will need
updates to show the preferred usage.

[Sean de Wolski, MathWorks]

***

On **page 213** [MATLAB has newer XML functions]:

MATLAB has better XML reading and writing capability than shown
in Section 7.1.6.1.
``readstruct``, ``readtable``, ``writestruct``, ``writetable``
and ``matlab.io.xml.*`` are easier to use than working with
the XML document object model (DOM) directly.

[Sean de Wolski, MathWorks]

***
