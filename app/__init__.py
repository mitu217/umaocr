import asyncio
import logging
import os

from flask import Flask

from app.driver.file_driver import LocalFileDriverImpl
from app.usecase.ability import AbilityInteractor
from app.usecase.character import CharacterInteractor
from app.usecase.skill_interactor import SkillInteractor
from app.usecase.status_interactor import StatusInteractor
from app.views.status import StatusResource
from app.views.web import WebResource


def create_app():
    logging.basicConfig(level=logging.INFO)
    debug = os.environ.get('ENABLE_DEBUG', True)

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("settings")

    web_resource = WebResource()
    status_resource = StatusResource(
        StatusInteractor(
            LocalFileDriverImpl(''),
            app.logger,
            debug=debug,
        ),
        CharacterInteractor(
            LocalFileDriverImpl(''),
            app.logger,
            debug=debug,
        ),
        AbilityInteractor(
            LocalFileDriverImpl(''),
            app.logger,
            debug=debug,
        ),
        SkillInteractor(
            LocalFileDriverImpl(''),
            app.logger,
            debug=debug,
        )
    )

    app.add_url_rule('/', view_func=web_resource.as_view('web_resource'))
    app.add_url_rule(
        '/api/v1/ocr/status',
        view_func=status_resource.index,
        methods=['POST'])

    return app