**Personal Income Tax Return Estimate (PITRE) System**
====================================================

This application is a three-tier distributed system designed to estimate personal income tax returns for users based on their income and tax data. It supports authenticated access, database integration, and tax computation using a client-server architecture built with Python, Flask, XML-RPC, and SQLite.

----------
Project Files:
- client.py - The client side application. Handling user authentication, input of TFN/manual income and tax entries, and displays the final estimated tax return result to the user.
- app_server.py - The server side application (Server 1). Receives data from the client, handles the business logic of tax calculations and communicates with the database server if a TFN is provided.
- data_server.py - The database server (Server 2). Retrieves stored biweekly income-tax data corresponding to the user's TFN from the SQLite database and sends it back to _app_server.py_.
- calculator.py - Contains tax logic, including rules for calculating the annual income and tax-withheld, annual tax, Medicare Levy, and Medicare Levy Surcharge.
- userauthentication.json - Stores client-side credentials used for authenticating users before allowing access to the tax estimation features.
- PITD.db - SQLite database file storing TFN-linked biweekly income and tax data and user's personal information.
- PITD.xlsx - Excel file that contains a sample data for the database, making it more user-friendly to be read.

----------
Running the System:
1. Ensure Python has been installed
2. Install dependencies in terminal "_pip install Flask requests_"
3. On the same terminal, run data_server.py to start the database "_python data_server.py_"
4. Open a new terminal and run app_server.py to start the server application "_python app_server.py_"
5. Open another new terminal and run client.py to start the client application "_python client.py_"
6. Enter credentials (stored in _userauthentication.json_) and provide a TFN or manual input to get your estimated tax return.

----------
Author:
Kenneth Esmond,
22 May 2025
