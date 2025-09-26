#!/usr/bin/env python3

import os
import sys
import cgitb

# Enable CGI error reporting
cgitb.enable()

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sampleauthapp.settings')

def application():
    try:
        import django
        django.setup()
        
        from django.core.wsgi import get_wsgi_application
        
        # Get Django WSGI application
        wsgi_app = get_wsgi_application()
        
        # Parse CGI environment
        method = os.environ.get('REQUEST_METHOD', 'GET')
        script_name = os.environ.get('SCRIPT_NAME', '/index.py')
        path_info = os.environ.get('PATH_INFO', '/')
        query_string = os.environ.get('QUERY_STRING', '')
        
        # Clean up path_info - remove script name if it's at the beginning
        if path_info.startswith('/index.py'):
            path_info = path_info[9:]  # Remove '/index.py'
        elif path_info.startswith('index.py'):
            path_info = path_info[8:]  # Remove 'index.py'
            
        if not path_info or path_info == '/':
            path_info = '/'
        
        # Ensure path_info starts with '/'
        if not path_info.startswith('/'):
            path_info = '/' + path_info
        
        # Read POST data
        content_length = int(os.environ.get('CONTENT_LENGTH', 0))
        wsgi_input = sys.stdin.buffer if hasattr(sys.stdin, 'buffer') else sys.stdin
        
        # Build WSGI environ
        environ = {
            'REQUEST_METHOD': method,
            'SCRIPT_NAME': '',  # Important: empty for Django
            'PATH_INFO': path_info,
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': os.environ.get('CONTENT_TYPE', ''),
            'CONTENT_LENGTH': str(content_length) if content_length else '',
            'SERVER_NAME': os.environ.get('SERVER_NAME', os.environ.get('HTTP_HOST', 'localhost').split(':')[0]),
            'SERVER_PORT': os.environ.get('SERVER_PORT', '80'),
            'SERVER_PROTOCOL': os.environ.get('SERVER_PROTOCOL', 'HTTP/1.1'),
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https' if os.environ.get('HTTPS') == 'on' else 'http',
            'wsgi.input': wsgi_input,
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': True,
        }
        
        # Add all HTTP headers to environ
        for key, value in os.environ.items():
            if key.startswith('HTTP_'):
                # Convert HTTP_HEADER_NAME to HTTP_Header-Name format
                header_key = key[5:].replace('_', '-').title()
                if header_key not in ['Content-Type', 'Content-Length']:
                    environ[key] = value
            elif key in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
                environ[key] = value
        
        # Capture response
        response_status = None
        response_headers = []
        
        def start_response(status, headers, exc_info=None):
            nonlocal response_status, response_headers
            response_status = status
            response_headers = headers
            return lambda x: None  # write function (not used in CGI)
        
        # Get response from Django
        try:
            response = wsgi_app(environ, start_response)
            
            # Output HTTP headers
            print(f"Status: {response_status}")
            for header_name, header_value in response_headers:
                print(f"{header_name}: {header_value}")
            print()  # Empty line between headers and content
            
            # Output response content
            try:
                for data in response:
                    if data:
                        if isinstance(data, str):
                            sys.stdout.write(data)
                        else:
                            sys.stdout.buffer.write(data)
            finally:
                # Close response if it has close method
                if hasattr(response, 'close'):
                    response.close()
                    
        except Exception as e:
            print("Content-Type: text/html")
            print(f"Status: 500 Internal Server Error")
            print()
            print(f"<h1>Django Application Error</h1>")
            print(f"<p>Error: {e}</p>")
            print(f"<p>Path Info: {path_info}</p>")
            print(f"<p>Method: {method}</p>")
            import traceback
            print(f"<pre>{traceback.format_exc()}</pre>")
            
    except ImportError as e:
        print("Content-Type: text/html")
        print("Status: 500 Internal Server Error")
        print()
        print(f"<h1>Django Import Error</h1>")
        print(f"<p>{e}</p>")
        print(f"<p>Python path: {sys.path}</p>")
        print(f"<p>Current dir: {current_dir}</p>")
        
    except Exception as e:
        print("Content-Type: text/html")
        print("Status: 500 Internal Server Error")
        print()
        print(f"<h1>Setup Error</h1>")
        print(f"<p>{e}</p>")
        print(f"<p>Environment: PATH_INFO={os.environ.get('PATH_INFO', 'None')}</p>")
        import traceback
        print(f"<pre>{traceback.format_exc()}</pre>")

if __name__ == '__main__':
    application()