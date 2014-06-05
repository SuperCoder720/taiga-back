# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014 David Barragán <bameda@dbarragan.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from taiga.base import filters
from taiga.base import exceptions as exc
from taiga.base.api import ModelCrudViewSet
from taiga.base.decorators import list_route
from taiga.projects.models import Project
from taiga.mdrender.service import render as mdrender

from taiga.projects.notifications import WatchedResourceMixin
from taiga.projects.history import HistoryResourceMixin


from . import models
from . import permissions
from . import serializers


class WikiViewSet(HistoryResourceMixin, WatchedResourceMixin, ModelCrudViewSet):
    model = models.WikiPage
    serializer_class = serializers.WikiPageSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.IsProjectMemberFilterBackend,)
    filter_fields = ("project", "slug")

    @list_route(methods=["POST"])
    def render(self, request, **kwargs):
        content = request.DATA.get("content", None)
        project_id = request.DATA.get("project_id", None)

        if not content:
            raise exc.WrongArguments({"content": "No content parameter"})

        if not project_id:
            raise exc.WrongArguments({"project_id": "No project_id parameter"})

        project = get_object_or_404(Project, pk=project_id)
        data = mdrender(project, content)
        return Response({"data": data})

    def pre_conditions_on_save(self, obj):
        super().pre_conditions_on_save(obj)

        if (obj.project.owner != self.request.user and
                obj.project.memberships.filter(user=self.request.user).count() == 0):
            raise exc.PermissionDenied(_("You don't haver permissions for add/modify "
                                         "this wiki page."))
    def pre_save(self, obj):
        if not obj.owner:
            obj.owner = self.request.user

        super().pre_save(obj)


class WikiLinkViewSet(ModelCrudViewSet):
    model = models.WikiLink
    serializer_class = serializers.WikiLinkSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.IsProjectMemberFilterBackend,)
    filter_fields = ["project"]
