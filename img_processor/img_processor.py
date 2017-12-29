from prometheus_client import start_http_server, Summary

import concurrent.futures
from nose.tools import *
from uvhttp.utils import HttpServer
from uvhue.rgb import is_grey
from sanic.response import json
import io
import colorthief
import asyncio
import logging
import time

PROCESSING_TIME = Summary('img_processing_time', 'Time spent processing images')

@PROCESSING_TIME.time()
def process_img(image):
    quality = 1

    start = time.time()

    cimage = colorthief.ColorThief(io.BytesIO(image))

    colors = []
    try:
        colors = cimage.get_palette(color_count=10, quality=quality)

        for color in colors:
            if not is_grey(color, 25):
                return color
    finally:
        logging.error("Processed album cover ({} bytes) in {} seconds at quality {}.".format(len(image), time.time() - start, quality))

class ImgProcessor(HttpServer):
    def add_routes(self):
        super().add_routes()
        self.app.add_route(self.process, '/image', methods=['POST'])
        self.app.add_route(self.health, '/health')
        self.executor = concurrent.futures.ProcessPoolExecutor()
        self.loop = asyncio.get_event_loop()

    async def process(self, request):
        """
        Return the rgb values of an image posted.
        """
        image = self.loop.run_in_executor(self.executor, process_img, request.body)
        rgb = await image
        return json({"rgb": rgb})

    async def health(self, request):
        return json({})

    def stop(self):
        super().stop()
        self.executor.shutdown()

async def run():
    img = ImgProcessor(host='0.0.0.0', port=8092, https_host='0.0.0.0', https_port=8093)
    await img.start()
    return img

if __name__=='__main__':
    start_http_server(8000)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.run_forever()
