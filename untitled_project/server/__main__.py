#!/usr/bin/env python3

import connexion

from untitled_project.server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'UntitledAPI'}, pythonic_params=True)
    app.run(port=8080)


if __name__ == '__main__':
    main()
