pip install jupyter_ascending && \
jupyter nbextension    install jupyter_ascending --sys-prefix --py && \
jupyter nbextension     enable jupyter_ascending --sys-prefix --py && \
jupyter serverextension enable jupyter_ascending --sys-prefix --py

jupyter nbextension     list
jupyter serverextension list
