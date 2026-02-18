import pytest


@pytest.fixture
def minimal_latex():
    """The simplest valid LaTeX document (1 page)."""
    return r"""\documentclass{article}
\begin{document}
Hello, world!
\end{document}
"""


@pytest.fixture
def two_page_latex():
    """A LaTeX document that produces exactly 2 pages."""
    return r"""\documentclass{article}
\begin{document}
\mbox{}
\newpage
\mbox{}
\end{document}
"""


@pytest.fixture
def invalid_latex():
    """LaTeX source that will fail to compile."""
    return r"""\documentclass{article}
\begin{document}
\undefinedcommand
\end{document}
"""


@pytest.fixture
def realistic_resume():
    """A realistic single-page resume."""
    return r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=0.5in]{geometry}
\begin{document}
\begin{center}
{\Large\textbf{Jane Doe}} \\
jane@example.com \textbar{} (555) 123-4567
\end{center}
\section*{Experience}
\textbf{Software Engineer} -- Acme Corp \hfill 2020--Present
\begin{itemize}
\item Built distributed systems serving 10M users
\item Led migration from monolith to microservices
\item Reduced API latency by 40\% through caching optimization
\end{itemize}
\textbf{Junior Developer} -- StartupCo \hfill 2018--2020
\begin{itemize}
\item Developed RESTful APIs in Python and Go
\item Implemented CI/CD pipelines with 95\% test coverage
\end{itemize}
\section*{Education}
\textbf{B.S. Computer Science} -- MIT \hfill 2014--2018
\section*{Skills}
Python, Go, Rust, PostgreSQL, Redis, Docker, Kubernetes, AWS
\end{document}
"""
