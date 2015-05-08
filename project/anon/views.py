from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from anon.models import AnonPost, AnonCommit
from anon.forms import AnonPostForm, AnonCommitForm


class AnonFrontView(ListView):
	template_name = 'anon/front.html'
	queryset = AnonPost.objects.published()
	paginate_by = 5

	def get(self, request, *args, **kwargs):
		if request.is_ajax(): self.template_name = 'content/ajax/posts.html'
		return super(AnonFrontView, self).get(request, *args, **kwargs)

class AnonPostView(DetailView):
	template_name = 'anon/post_detail.html'

	def get_queryset(self):
		pk, slug = self.kwargs['pk'], self.kwargs['slug']
		queryset = AnonPost.objects.by_post(pk, slug)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(AnonPostView, self).get_context_data(**kwargs)
		context['form'] = AnonCommitForm
		return context


class AnonCreatePostView(CreateView):
	template_name = 'anon/post_create.html'
	form_class = AnonPostForm


class AnonPostCommitView(CreateView):
	form_class = AnonCommitForm

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.post = AnonPost.objects.get(post_id=self.kwargs['pk'])
		obj.save()
		obj.post.last_commited = obj.created
		obj.post.commit_number += 1
		obj.post.save()
		return HttpResponseRedirect(obj.get_absolute_url())