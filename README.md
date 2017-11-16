<h1>Logs Analysis Project<h1>
Retrieve data from a large database and display the top articles and authors.

<h2>Prerequisites</h2>
    <ul>
        <li>Python</li>
        <li>loganalysis.py</li>
        <li>newsdata.sql</li>
        <li>Virtual Machine</li>
    </ul>
	
<h2>Installing</h2>
	Download and install VirtualBox and Vagrant
	Inside the vagrant subdirectory run <code>vagrant up</code> and then <code>vagrant ssh</code>
	Add data from newsdata.sql into your local database using <code>psql -d newsdata.sql</code>
	
	
<h2>Run</h2>
	Run the <code>python loganalysis.py</code> command to run and display the log results
	