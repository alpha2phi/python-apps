import sys
import base64
import logging
import graphene
import uvicorn
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from io import BytesIO
from playwright.sync_api import sync_playwright

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Query(graphene.ObjectType):
    screenshot = graphene.String(
        url=graphene.String(default_value="http://www.google.com"),
        width=graphene.Int(default_value=1024),
        height=graphene.Int(default_value=768),
    )

    def resolve_screenshot(self, info, url, width, height):
        with sync_playwright() as p:
            browser_type = p.chromium
            browser = browser_type.launch()
            page = browser.new_page()
            page.set_viewport_size({"width": width, "height": height})
            page.goto(url)
            img_byte = page.screenshot(full_page=True)
            # encoded_img = "data:image/png;base64," + base64.b64encode(
            # img_byte).decode()
            encoded_img = base64.b64encode(img_byte).decode()
            browser.close()
            return encoded_img


app = FastAPI(
    title="Grabber App",
    description="""Visit port 8088/docs for the Swagger documentation.""",
    version="0.0.1")

app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
