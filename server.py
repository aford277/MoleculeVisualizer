import sys
import urllib
from http.server import HTTPServer, BaseHTTPRequestHandler
import MolDisplay
import molsql
import json
import cgi
import tempfile
import molecule

currentMol = MolDisplay.Molecule()

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            with open("homepage.html", "r") as f:
                html_content = f.read()
            
            self.send_response( 200 )
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len(html_content) )
            self.end_headers()

            self.wfile.write( bytes( html_content, "utf-8" ) )

        elif self.path == "/homeScript.js":
            with open("homeScript.js", "r") as f:
                js_content = f.read()
            
            self.send_response( 200 )
            self.send_header( "Content-type", "text/javascript" )
            self.send_header( "Content-length", len(js_content) )
            self.end_headers()

            self.wfile.write( bytes( js_content, "utf-8" ) )
        
        elif self.path == "/elements":
            with open("elements.html", "r") as f:
                element_page_content = f.read()
            
            self.send_response( 200 )
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len(element_page_content) )
            self.end_headers()

            self.wfile.write( bytes( element_page_content, "utf-8" ) )

        elif self.path == "/elementScript.js":
            with open("elementScript.js", "r") as f:
                js_content = f.read()
            
            self.send_response( 200 )
            self.send_header( "Content-type", "text/javascript" )
            self.send_header( "Content-length", len(js_content) )
            self.end_headers()

            self.wfile.write( bytes( js_content, "utf-8" ) )

        # elif self.path == "/display":
        #     with open("moleculedisplay.html", "r") as f:
        #         display_page = f.read()

        #     # Parse the request URL to extract the title parameter
        #     parsed_url = urllib.parse.urlparse(self.path)
        #     title = urllib.parse.parse_qs(parsed_url.query)['value'][0]

        #     # Process the title parameter as needed
        #     print('Title:', title)
            
        #     self.send_response( 200 )
        #     self.send_header( "Content-type", "text/html" )
        #     self.send_header( "Content-length", len(display_page) )
        #     self.end_headers()

        #     self.wfile.write( bytes( display_page, "utf-8" ) )

        elif self.path == "/molecules.db/Elements":
            parts = self.path.split("/")
            table_name = parts[2]

            db.cur.execute("SELECT * FROM {}".format(table_name))
            rows = db.cur.fetchall()
            
            data = []
            for row in rows:
                data.append({'ELEMENT_NO': row[0], 'ELEMENT_CODE': row[1], 'ELEMENT_NAME': row[2], 'COLOUR1': row[3], 'COLOUR2': row[4], 'COLOUR3': row[5], 'RADIUS': row[6]})

            self.send_response(200)
            self.send_header('Content-type', 'applications/json')
            self.end_headers()

            self.wfile.write(json.dumps(data).encode('utf-8'))

        elif self.path == "/molecules.db/Molecules":
            parts = self.path.split("/")
            table_name = parts[2]

            db.cur.execute("SELECT * FROM {}".format(table_name))
            rows = db.cur.fetchall()

            data = []
            for row in rows:
                data.append({'NAME': row[1], 'ATOM_NO': row[2], 'BOND_NO': row[3]})

            self.send_response(200)
            self.send_header('Content-type', 'applications/json')
            self.end_headers()

            self.wfile.write(json.dumps(data).encode('utf-8'))

        elif self.path == "/elements.css":
            with open("elements.css", "r") as f:
                content = f.read()
            
            self.send_response( 200 )
            self.send_header( "Content-type", "text/css" )
            self.send_header( "Content-length", len(content) )
            self.end_headers()

            self.wfile.write( bytes( content, "utf-8" ) )

        elif self.path == "/home.css":
            with open("home.css", "r") as f:
                content = f.read()
            
            self.send_response( 200 )
            self.send_header( "Content-type", "text/css" )
            self.send_header( "Content-length", len(content) )
            self.end_headers()

            self.wfile.write( bytes( content, "utf-8" ) )

        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )
    
    def do_POST(self):
        global currentMol

        if self.path == "/add_element":
            
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            postvars = urllib.parse.parse_qs(body.decode('utf-8'))
            valid_input = True
            key_list = list(postvars.keys())

            # this next bit looks really ugly but its just about the only way i could make this work
            if("num" in key_list):
                pass
            else:
                valid_input = False
            if("code" in key_list):
                pass
            else:
                valid_input = False
            if("name" in key_list):
                pass
            else:
                valid_input = False
            if("colour1" in key_list):
                pass
            else:
                valid_input = False
            if("colour2" in key_list):
                pass
            else:
                valid_input = False
            if("colour3" in key_list):
                pass
            else:
                valid_input = False
            if("radius" in key_list):
                pass
            else:
                valid_input = False
            if(valid_input == True):
                if(postvars['num'][0].isdigit() == False):
                    valid_input = False
                elif (len(postvars['code'][0]) > 2):
                    valid_input = False
                elif (len(postvars['name'][0]) > 31):
                    valid_input = False
                elif (len(postvars['colour1'][0]) != 6):
                    valid_input = False
                elif (len(postvars['colour2'][0]) != 6):
                    valid_input = False
                elif (len(postvars['colour3'][0]) != 6):
                    valid_input = False
                elif (isfloat(postvars['radius'][0]) == False):
                    valid_input = False

            if(valid_input):
                db['Elements'] = (postvars['num'][0], postvars['code'][0], postvars['name'][0], postvars['colour1'][0], postvars['colour2'][0], postvars['colour3'][0], postvars['radius'][0])
                message = "got it"
                self.send_response(200)
            else:
                message = "incorrect values"
                self.send_response(404)
            
            self.send_header('Content-type', 'text/plain')
            self.send_header('Content-length', len(message))
            self.end_headers()

            self.wfile.write(bytes(message, "utf-8"))

        elif self.path == "/remove_element":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            postvars = urllib.parse.parse_qs(body.decode('utf-8'))
            valid_input = True
            key_list = list(postvars.keys())

            if("code" in key_list):
                pass
            else:
                valid_input = False

            if(valid_input):
                db.cur.execute("""DELETE
                                    FROM Elements
                                    WHERE Elements.ELEMENT_CODE = '{}'""".format(postvars['code'][0]))
                db.conn.commit()
                message = "deleted"
                self.send_response(200)
            else:
                message = "incorrect values"
                self.send_response(404)
            
            self.send_header('Content-type', 'text/plain')
            self.send_header('Content-length', len(message))
            self.end_headers()

            self.wfile.write(bytes(message, "utf-8"))

        elif self.path == "/molecule":
            content_length = int(self.headers['Content-Length'])
            content_type = self.headers['Content-Type']
            boundary = content_type.split("=")[1].encode()

            # Read the request body as a multi-part form data
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                        'CONTENT_TYPE': content_type})

            # Get the molecule name and SDF file object from the form data
            molecule_name = form_data.getvalue('moleculeName')
            sdf_file = form_data.getvalue('sdfFile')

            db.add_molecule(molecule_name, sdf_file)

            mol = db.load_mol(molecule_name)
            response_data = {
                'name': molecule_name,
                'atoms': mol.atom_no,
                'bonds': mol.bond_no
            }


            # Do something with molecule_name and sdf_file

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))


            # ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
            # if ctype == 'multipart/form-data':
            #     pdict['boundary'] = pdict['boundary'].encode()
            #     fields = cgi.parse_multipart(self.rfile, pdict)
            #     molecule_name = fields["moleculeName"][0]

            #     # Save the uploaded file to a temporary file
            #     with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            #         tmp_file.write(fields['sdfFile'][0])
            #         sdf_file_path = tmp_file.name
                
            #     fp = open(sdf_file_path)
            #     db.add_molecule(molecule_name, fp)

            #     mol = db.load_mol( molecule_name )
            #     # Send the response back to jQuery with the three variables
            #     response_data = {
            #         'name': molecule_name,
            #         'atoms': mol.atom_no,
            #         'bonds': mol.bond_no
            #     }
                
            #     self.send_response(200)
            #     self.send_header('Content-type', 'application/json')
            #     self.end_headers()
            #     self.wfile.write(json.dumps(response_data).encode('utf-8'))
                
                
            # else:
            #     self.send_response(400)
            #     self.send_header('Content-type', 'text/plain')
            #     self.end_headers()
            #     self.wfile.write(b'Bad request')

        elif self.path == "/display":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_data_dict = urllib.parse.parse_qs(post_data)

            if 'name' in post_data_dict:
                mol_name = post_data_dict['name'][0]
                molname = mol_name
                
                MolDisplay.radius = db.radius()
                MolDisplay.element_name = db.element_name()
                MolDisplay.header += db.radial_gradients()

                currentMol = db.load_mol(mol_name)
                currentMol.sort()

                # Send the SVG data back to the client
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.end_headers()
                self.wfile.write(bytes(currentMol.svg(), 'utf-8'))
            else:
                # If name is not present in the POST data, return a 400 Bad Request response
                self.send_error(400, 'Name parameter not found')

        elif self.path == "/rotate":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            postvars = urllib.parse.parse_qs(body.decode('utf-8'))

            if(int(postvars['xrot'][0]) != 0):
                mx = molecule.mx_wrapper(int(postvars['xrot'][0]),0,0)
                currentMol.xform( mx.xform_matrix )

            if(int(postvars['yrot'][0]) != 0):
                mx = molecule.mx_wrapper(0,int(postvars['yrot'][0]),0)
                currentMol.xform( mx.xform_matrix )

            if(int(postvars['zrot'][0]) != 0):
                mx = molecule.mx_wrapper(0,0,int(postvars['zrot'][0]))
                currentMol.xform( mx.xform_matrix )

            currentMol.sort()

            # Send the SVG data back to the client
            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.end_headers()
            self.wfile.write(bytes(currentMol.svg(), 'utf-8'))

        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )


db = molsql.Database()
db.create_tables()
httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
httpd.serve_forever()
