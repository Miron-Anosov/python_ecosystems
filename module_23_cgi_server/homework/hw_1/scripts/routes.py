import json

GET_METHOD_HTTP = 'GET'
POST_METHOD_HTTP = 'POST'
ENV_PATH = '/env', '/env/'
DEF_PATH = '/hello', '/hello/',
DEF_MESSAGE = 'Hello World'
NOT_FOUND_MSG = "Not found"
ERROR_404 = "404 Not found"
STATUS_OK = '200 OK'
BAD_REQUEST_400 = '400 Bad Request'

json_404_response = json.dumps({ERROR_404: NOT_FOUND_MSG})
json_400_response = json.dumps({BAD_REQUEST_400: 'Not support'})
json_message_simple = json.dumps({STATUS_OK: DEF_MESSAGE})


def application(environ, start_response):
    """Simple application uWSGI"""
    path_info: str = environ.get('PATH_INFO')
    method_http = environ.get('REQUEST_METHOD')
    try:
        if method_http == GET_METHOD_HTTP:

            try:

                start_response(STATUS_OK, [('Content-Type', 'application/json')])

                if path_info in DEF_PATH:
                    """If the route is default."""
                    return [json_message_simple.encode(), ]

                elif path_info.startswith('/hello'):
                    """If the route has a deep path."""
                    query_string = environ.get('QUERY_STRING')
                    str_items_for_message_from_path = ' '.join(path_info.split('/')[1::])
                    if len(query_string) >= 3:  # key = value : example x=2
                        """If the route has params."""
                        query = ' '.join(query_string.split('&'))
                        json_msg = json.dumps(
                            {'status': STATUS_OK, 'message': str_items_for_message_from_path, 'params': query})
                        return [json_msg.encode(), ]

                    json_msg = json.dumps({'status': STATUS_OK, 'message': str_items_for_message_from_path})
                    return [json_msg.encode(), ]

                elif path_info in ENV_PATH:
                    environ_str = {key: str(value) for key, value in environ.items()}
                    response = json.dumps({'Environ': environ_str}, indent=4)
                    return [response.encode('utf-8'),]

                else:
                    """If the route break."""
                    raise Exception('Not exists page')

            except (Exception,):
                """If the route isn't found."""
                start_response(ERROR_404, [('Content-Type', 'application/json')])
                return [json_404_response.encode(), ]

        elif method_http == POST_METHOD_HTTP:
            """For example"""
            start_response('201 Created', [('Content-Type', 'text/plain')])
            return [b'default response', ]

        else:
            """If method isn't support"""
            raise Exception('Bad request')

    except (Exception,):
        """If Bad Request."""
        start_response(BAD_REQUEST_400, [('Content-Type', 'application/json')])
        return [json_400_response.encode(), ]
