"""Smart Mirror User Settings Web Services (API)

Module dedicated for creating web services to enable CRUD operations
to the Smart Mirror database, through a consistent and easy to deploy
web service build with CherryPy.

Author: Alessandro Chávez
"""

import cherrypy
import cherrypy_cors
import json

@cherrypy.expose
class WebPageWebService(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        'Servicio GET por si se requiere...'
        return str('data')

    @cherrypy.expose
    def POST(self, data_json):
        """POST operation that enables the interaction with the MySQL database
        through a JSON file
        
        Arguments:
            data_json {json} -- Arguments specifying the type of operation to
            apply in the MySQL database (it could be any kind of CRUD 
            operation). In must cases it also needs to have more arguments to
            be able to query some specific things in the database.
        
        Returns:
            json -- Results from the database in JSON format
        """

        # 
        # data = json.loads(data_json)
        # fingers = dp.Fingers()
        # operations = {
        #     'get_tables': fingers.get_tables
        # }
        # try:
        #     func = operations.get(data['operation'], lambda: {
        #                       'res': 'Error durante operación'})
        # except KeyError:
        #     return json.dumps({'res': 'Operación inválida.'})
        # response = {'res': func()}
        # return json.dumps(response, ensure_ascii=False)
        return None


if __name__ == '__main__':
    cherrypy_cors.install()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'cors.expose.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [
                ('Content-Type', 'text/plain'), 
                ('Access-Control-Allow-Origin', '*')
            ]
        }
    }
    cherrypy.config.update({'server.socket_host': '127.0.0.1'})
    # cherrypy.config.update({'server.socket_host': '192.168.43.180'})
    cherrypy.config.update({'server.socket_port': 8086})
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.quickstart(WebPageWebService(), '/', conf)