#define locations relative to this file 
import sys,os
webapp_parent_dir=os.path.dirname(os.path.abspath(__file__))
root_dir=os.path.dirname(webapp_parent_dir)
###

#Start the API 
from fastapi import FastAPI,Request,Form
# use lifespan to have processes running in the background
#such as DB updates etc.
#variuos create_lifespan functions will be kept in life_span folder
from life_spans.life_span_no_mailing_list import create_lifespan

# Use getenv to control if
# the background updates are done
# For docker runs the ENVs are set to true
# For local run all is controlled by local_run.env

background_run=bool(int(os.getenv("RUN_IN_BACKGROUND")))
webapp_lifespan=create_lifespan(background_run)
webapp=FastAPI(lifespan=webapp_lifespan)
    
# Necessary to enforce HTTPS in headers - IF NEEDED
handle_https=bool(int(os.getenv("HANDLE_HTTPS")))
if handle_https:
    from fastapi.middleware.trustedhost import TrustedHostMiddleware
    from starlette.middleware.base import BaseHTTPMiddleware
    class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            # To mówi FastAPI: "Traktuj wszystkie zapytania jak HTTPS"
            request.scope["scheme"] = "https"
            response = await call_next(request)
            return response
    webapp.add_middleware(HTTPSRedirectMiddleware)


# Mount location of static data like pictures etc. ...
from fastapi.staticfiles import StaticFiles
webapp.mount("/static",
             StaticFiles(directory=os.path.join(webapp_parent_dir,"static")),
             name="static"
             )

# Mount the templates for home- and sub-, pages 
# All handled by Jinja2
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(
    directory=os.path.join(webapp_parent_dir,"page_templates")
    )

### HOME PAGE #####
# import list of show types and
# display them in buttons -> controlled by 
# template-home page
from app.main import event_type_list
from fastapi.responses import HTMLResponse # import HTML respose

@webapp.get("/",response_class=HTMLResponse)
async def welcome_page(request: Request):
    dict_for_template={          
        "request": request,
        "event_list": event_type_list,
        "url_for": request.url_for
    }
    return templates.TemplateResponse("home.html",dict_for_template)

### Redirect to ticketing subpages
### depending on the decission that the 
### user made
from fastapi.responses import RedirectResponse
@webapp.post("/pick_event")
async def handle_event_pick(request:Request,
                            event_num: int=Form(...)):
    # Redirect to subpage handling the chosen event-type
    url_to_pass=request.url_for("print_tickets",event_num=event_num)
    return RedirectResponse(url=url_to_pass, status_code=303)

# Genereate Subpages with tickets
# get the subpage handling from
# functions definde in API_modules directory
from API_modules import ticket_subpage
webapp.include_router(ticket_subpage.router)

