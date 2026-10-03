from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates 
from data import posts

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


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

@app.get("/posts/{post_id}", name="post", include_in_schema=False)
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return templates.TemplateResponse(
                request,
                "post.html",
                {"post": post, "title": post["title"]},
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="requested post not found")

@app.get("/api/posts/{post_id}", name="api_post")
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="requested post not found")