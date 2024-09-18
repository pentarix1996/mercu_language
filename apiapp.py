import attr

from fastapi.applications import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware


@attr.s(auto_attribs=True)
class APIApp():

    title: str

    def __attrs_post_init__(self):
        self.app = FastAPI(title=self.title)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def get_app_instance(self) -> FastAPI:
        return self.app

    def get_title(self) -> str:
        return self.title

    def include_router(self, router: APIRoute) -> None:
        self.app.include_router(router)
