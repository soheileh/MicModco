from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from django import forms

# keep the definition of BlogIndexPage model, and add the BlogPage model:
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )
class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),

            FieldPanel('tags'),
        ],heading='Blog information'),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    # content_panels = Page.content_panels + [
    #     FieldPanel('date'),
    #     FieldPanel('intro'),
    #     FieldPanel('body'),
    #     InlinePanel('gallery_images', label="Gallery images"),
    # ]

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

    @register_snippet
    class Author(models.Model):
        name = models.CharField(max_length=255)
        author_image = models.ForeignKey(
            'wagtailimages.Image', null=True, blank=True,
            on_delete=models.SET_NULL, related_name='+'
        )

        panels = [
            FieldPanel('name'),
            FieldPanel('author_image'),
        ]

        def __str__(self):
            return self.name

        class Meta:
            verbose_name_plural = 'Authors'

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )