import os
import uuid
import json

import cherrypy


class DeadParrot:
    """
    http://www.youtube.com/watch?v=4vuW6tQ0218

    A server that just parrots back the content you send to it.
    """

    data = {}
    exposed = True

    def POST(self):
        """
        We're all out of parrots, but we do have a slug.
        """
        slug = uuid.uuid4()
        data = dict(
            content=cherrypy.request.body.read(),
            type=cherrypy.request.headers['Content-Type'],
        )
        self.data[str(slug)] = data
        url = cherrypy.url(f'/{slug}')
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return json.dumps(dict(url=url))

    def GET(self, slug):
        if slug not in self.data:
            raise cherrypy.NotFound()
        data = self.data.pop(slug)
        cherrypy.response.headers['Content-Type'] = data['type']
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return data['content']

    @classmethod
    def helloooooo(cls):
        config = {
            'global': {
                'server.socket_host': '::0',
                'server.socket_port': int(os.environ.get('PORT', 8080)),
                'environment': os.environ.get('CP_ENVIRONMENT', 'production'),
            },
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.decode.on': False,
            },
        }
        cherrypy.quickstart(cls(), config=config)


if __name__ == '__main__':
    DeadParrot.helloooooo()
