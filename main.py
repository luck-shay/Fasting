from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates 

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


posts: list[dict] = [
    {
        "id": 1,
        "author": "ABC",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    { 
        "id": 2,
        "author": "XYZ",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it better",
        "date_posted": "April 21, 2025",
    },
]
def render_posts(request: Request):
    return templates.TemplateResponse(
        request, 
        "home.html", 
        {"posts": posts, "title": "Home"})

@app.get("/", name="home", include_in_schema=False)
@app.get("/posts", name="posts", include_in_schema=False)
def posts_page(request: Request):
    return render_posts(request)

@app.get("/api/posts", name="api_posts")
def get_posts():
    return posts
