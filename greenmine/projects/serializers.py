# -*- coding: utf-8 -*-

from rest_framework import serializers

from greenmine.base.serializers import PickleField

from . import models


class AttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField("get_url")
    size = serializers.SerializerMethodField("get_size")

    class Meta:
        model = models.Attachment
        fields = ("id", "project", "owner", "attached_file", "size", "created_date",
                  "modified_date", "object_id", "url")
        read_only_fields = ("owner",)

    def get_url(self, obj):
        return obj.attached_file.url if obj and obj.attached_file else ""

    def get_size(self, obj):
        if obj.attached_file:
            return obj.attached_file.size
        return None


# User Stories common serializers

class PointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Points


class UserStoryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserStoryStatus


# Task common serializers

class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskStatus


# Issues common serializers

class SeveritySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Severity


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Priority


class IssueStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IssueStatus


class IssueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IssueType


# Questions common serializers

class QuestionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionStatus


# Projects

class MembershipSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', required=False)
    full_name = serializers.CharField(source='user.get_full_name', required=False)

    class Meta:
        model = models.Membership


class ProjectSerializer(serializers.ModelSerializer):
    tags = PickleField(required=False)

    class Meta:
        model = models.Project
        read_only_fields = ("created_date", "modified_date", "owner")
        exclude = ("last_us_ref", "last_task_ref", "last_issue_ref")


class ProjectDetailSerializer(ProjectSerializer):
    list_of_milestones = serializers.SerializerMethodField("get_list_of_milestones")
    memberships = MembershipSerializer(many=True, required=False)
    us_statuses = UserStoryStatusSerializer(many=True, required=False)       # User Stories
    points = PointsSerializer(many=True, required=False)
    task_statuses = TaskStatusSerializer(many=True, required=False)          # Tasks
    priorities = PrioritySerializer(many=True, required=False)               # Issues
    severities = SeveritySerializer(many=True, required=False)
    issue_statuses = IssueStatusSerializer(many=True, required=False)
    issue_types = IssueTypeSerializer(many=True, required=False)
    #question_statuses = QuestionStatusSerializer(many=True, required=False) # Questions

    def get_list_of_milestones(self, obj):
        milestones_list = []

        if obj and obj.memberships:
            milestones_list = [{
                "id": milestone.id,
                "name": milestone.name,
                "finish_date": milestone.estimated_finish,
                "closed_points": milestone.closed_points,
                "client_increment_points": milestone.client_increment_points,
                "team_increment_points": milestone.team_increment_points
            } for milestone in obj.milestones.all().order_by("estimated_start")]

        return milestones_list
