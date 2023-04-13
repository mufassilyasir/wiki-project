from flask import request, redirect
from urllib.parse import urlparse, urlunparse
# from waitress import serve
from main import create_app

app = create_app()


# @app.before_request
# def redirect_nonwww():
#     urlparts = urlparse(request.url)
#     if urlparts.netloc == 'www.DOMAIN.com':
#         urlparts_list = list(urlparts)
#         urlparts_list[1] = 'DOMAIN.com'
#         return redirect(urlunparse(urlparts_list), code=301)
    

if __name__ == "__main__":
    # serve(app, host='0.0.0.0', threads=8)
    app.run(debug=True)