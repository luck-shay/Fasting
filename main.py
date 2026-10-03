from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from data import posts
from schemas import PostCreate, PostResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def render_posts(request: Request):
    return templates.TemplateResponse(
        request, 
        "posts.html", 
        {"posts": posts, "title": "Home"})

@app.get("/", name="home", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html"
    )

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
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The requested post could not be found.",
    )

@app.get("/api/posts/{post_id}", name="api_post")
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="requested post not found")


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request,  exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code, 
            content= {"detail": message}, 
        )
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": f"Error {exception.status_code}",
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": "Invalid request",
            "message": "The request could not be processed. Please check the URL and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )

@app.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "October 3, 2026",
    }
    posts.append(new_post)
    return new_post