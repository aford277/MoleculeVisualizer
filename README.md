This project uses a combination of C, Python, and Javascript to run a website to visualize molecules. Users can upload sdf files to the website and view what the molecule in that sdf file looks like. Users have the option to customize the appearance of atoms and can add their own atoms (only some are available by default).

To run the project run the following commands:
make
export LD_LIBRARY_PATH=`pwd`
python3 server.py (PORT NUMBER)

where port number is the port you wish to view the page on. Then go to localhost:PORT NUMBER in your browser to access the website.

NOTE
This application is designed for linux based systems.
Python 3.7 or higher is needed. A different library path may needed to be set that's different than the one provided above.

Credits:
The design/structure of the application and the molecule.i file were created by Dr Stefan Kremer. 
