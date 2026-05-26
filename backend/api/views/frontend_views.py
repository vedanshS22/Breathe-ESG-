from pathlib import Path

from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View


class AnalystAppView(View):
    fallback_template_name = "api/analyst_app.html"

    def get(self, request, *args, **kwargs):
        react_index = finders.find("frontend/index.html")
        if react_index:
            return HttpResponse(Path(react_index).read_text(encoding="utf-8"))
        return HttpResponse(render_to_string(self.fallback_template_name, request=request))
