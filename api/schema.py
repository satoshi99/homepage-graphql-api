from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import pytz
from .models import Tag, Blog
import markdown


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            'username': ['exact', 'icontains'],
        }
        interfaces = (relay.Node,)


class TokyoDateTime(graphene.types.Scalar):
    @staticmethod
    def serialize(obj):
        timezone = pytz.timezone('Asia/Tokyo')
        return obj.astimezone(tz=timezone).strftime("%Y/%m/%d")


class Markdown(graphene.types.Scalar):
    @staticmethod
    def serialize(obj):
        return markdown.markdown(
            obj,
            extensions=[
                'markdown.extensions.fenced_code',
                'toc',
                'tables',
            ])


class TagNode(DjangoObjectType):
    class Meta:
        model = Tag
        filter_fields = {
            'name': ['icontains'],
        }
        interfaces = (relay.Node,)


class BlogNode(DjangoObjectType):
    class Meta:
        model = Blog
        filter_fields = {
            'title': ['icontains'],
            'content': ['icontains'],
            'tags__name': ['exact'],
            'is_public': ['exact'],
        }
        interfaces = (relay.Node,)
    published_at = graphene.Field(TokyoDateTime)
    content = graphene.Field(Markdown)

    @classmethod
    def get_queryset(cls, queryset, info):
        if info.context.user.is_anonymous:
            return queryset.filter(is_public=True)
        return queryset


class Query(graphene.ObjectType):
    login_user = graphene.Field(UserNode)
    tag = relay.Node.Field(TagNode)
    blog = relay.Node.Field(BlogNode)
    all_tags = DjangoFilterConnectionField(TagNode)
    all_blogs = DjangoFilterConnectionField(BlogNode)

    @login_required
    def resolve_login_user(self, info, **kwargs):
        return User.objects.get(id=info.context.user.id)
