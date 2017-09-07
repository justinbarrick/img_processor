from nose.tools import *
from uvhttp.utils import http_server
from uvhttp.dns import Resolver
from uvhttp.http import Session
from img_processor.img_processor import ImgProcessor

@http_server(ImgProcessor)
async def test_img_processor(server, loop):
    resolver = Resolver(loop)
    resolver.add_to_cache(b'img-processor', 80, server.host.encode(), 60, port=server.port)

    session = Session(10, loop, resolver=resolver)
    response = await session.post(b'http://img-processor/image', data=open('tests/test_data/image', 'rb').read())

    assert_equal(response.json(), {"rgb": [220, 212, 190]})

@http_server(ImgProcessor)
async def test_img_processor_partial_white(server, loop):
    resolver = Resolver(loop)
    resolver.add_to_cache(b'img-processor', 80, server.host.encode(), 60, port=server.port)

    session = Session(10, loop, resolver=resolver)
    response = await session.post(b'http://img-processor/image', data=open('tests/test_data/mostly_grey', 'rb').read())

    assert_equal(response.json(), {"rgb": [111, 96, 70]})
