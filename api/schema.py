from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import pytz
from .models import Tag, Blog
import markdown
from graphql_relay import from_global_id


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
            'tags__name': ['exact', 'icontains'],
            'tags__slug': ['exact'],
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
    blog = graphene.Field(BlogNode, id=graphene.NonNull(graphene.ID))
    all_tags = DjangoFilterConnectionField(TagNode)
    all_blogs = DjangoFilterConnectionField(BlogNode)
    login_user = graphene.Field(UserNode)

    def resolve_blog(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Blog.objects.get(id=from_global_id(id)[1])

    def resolve_all_tags(self, info, **kwargs):
        return Tag.objects.all()

    def resolve_all_blogs(self, info, **kwargs):
        return Blog.objects.all()

    @login_required
    def resolve_login_user(self, info, **kwargs):
        return User.objects.get(id=info.context.user.id)
