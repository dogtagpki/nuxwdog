Nuxwdog is a watchdog daemon that can be used to start, stop, monitor and reconfigure server programs. 
It is based on the uxwdog code that is used to start the Netscape Enterprise Server (NES).

Nuxwdog is used in Red Hat Certificate System 8 to start all of the Java-based and C/C++ based servers.
These servers require passwords to access security databases in order to start, but there was a requirement
that no unencrypted password files be stored on the system. In this case, nuxwdog is used to prompt the user
for the relevant passwords during server startup. These passwords are then cached by the nuxwdog, so that
nuxwdog can restart the server without human intervention. This is particularly important for automatically
restarting the server in case of a server crash.

More details on how nuxwdog works and how to configure it can be found on the Dogtag wiki:
http://pki.fedoraproject.org/wiki/Nuxwdog 
