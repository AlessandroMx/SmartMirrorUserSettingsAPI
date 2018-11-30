"""Smart Mirror User Settings Web Services (API)

Module dedicated for creating web services to enable CRUD operations
to the Smart Mirror database, through a consistent and easy to deploy
web service build with CherryPy.

Author: Alessandro Chávez
"""

import apple
import cherrypy
import cherrypy_cors
import json

from IPython import embed

@cherrypy.expose
class WebPageWebService(object):

    # @cherrypy.tools.accept(media='text/plain')
    # def GET(self):
    #     """Simple GET method for any future implementation

    #     Returns
    #     -------
    #     str
    #         Just a 'data' string that test that the GET method is working fine
    #     """

    #     return str('data')

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self, arg):
        """POST operation that enables the interaction with the MySQL database
        through a JSON file

        Parameters
        ----------
        data_json : json
            Arguments specifying the type of operation to
            apply in the MySQL database (it could be any kind of CRUD 
            operation). In must cases it also needs to have more arguments to
            be able to query some specific things in the database.

        Returns
        -------
        json
            Results from the database in JSON format
        """
        data_json = cherrypy.request.json
        apple_obj = apple.Apple(data_json)
        try:
            response = apple_obj.manage_operations()
        except Exception as catched_exception:
            response = str(catched_exception)
        response = {'response': response}
        return response


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
    cherrypy.config.update({'server.socket_port': 8086})
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.quickstart(WebPageWebService(), '/', conf)
