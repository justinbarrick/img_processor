import concurrent.futures
from nose.tools import *
from uvhttp.utils import HttpServer
from sanic.response import json
import io
import colorthief
import asyncio

def process_img(image):
    image = colorthief.ColorThief(io.BytesIO(image))
    return image.get_color()

class ImgProcessor(HttpServer):
    def add_routes(self):
        super().add_routes()
        self.app.add_route(self.process, '/image', methods=['POST'])
        self.executor = concurrent.futures.ProcessPoolExecutor()
        self.loop = asyncio.get_event_loop()

    async def process(self, request):
        """
        Return the rgb values of an image posted.
        """
        image = self.loop.run_in_executor(self.executor, process_img, request.body)
        rgb = await image
        return json({"rgb": rgb})

async def run():
    img = ImgProcessor(port=8092, https_port=8093)
    await img.start()
    return img

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.run_forever()
