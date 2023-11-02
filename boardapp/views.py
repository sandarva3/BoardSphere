from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Board, Topic, Post, User
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import ListView
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect

#The Below is the code of Generic-Class-Based-View, below that is FBV code. Both do the same thing.:
class HomeView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boardapp/home.html'
    #The below example is of classic Function-Based-View code:
''' 
def home_view(request):
        boards = Board.objects.all()
        return render(request, 'boardapp/home.html', {'boards':boards})   
    '''


#The 2nd chunk of code is class FBV(Function-Based-Views) method code. While the first chunk is code in GCBV(Generic-Class-Based-Views) method.
#In 1st Chunk we implement Pagination.
class BoardTopicsView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'boardapp/topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-topic_created').annotate(replies=Count('posts') - 1 )
        return queryset
        
'''
def board_topics_view(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-topic_created').annotate(replies=Count('posts')-1)
    context = {
        'board': board,
        'topics': topics,
    }
    return render(request, 'boardapp/topics.html', context)
'''
    

@login_required
def newTopic_view(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = request.user
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            #topic.subject = form.cleaned_data.get('subject')
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
        
        return redirect('posts', pk=board.pk, topic_pk=topic.pk)

    form = NewTopicForm()
    context = {
        'board': board,
        'form': form
    }
    return render(request, 'boardapp/newtopic.html', context)


#Two chunks of codes. First GCBV. Second FBV. Both do same thing. In First chunk there's little bit more addition of functionalities.
class PostView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boardapp/posts.html'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        user = request.user
        form = PostForm(request.POST)
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        if not user.is_authenticated:
            return redirect("login")
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = self.topic
            post.created_by = request.user
            post.save()
            return HttpResponseRedirect(reverse('posts', kwargs={'pk': self.kwargs.get('pk'), 'topic_pk': self.kwargs.get('topic_pk')}))
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        kwargs['form'] = PostForm()
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('-created_at')
        return queryset
        

'''
@login_required
def post_view_function(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    posts = topic.posts.order_by('-created_at')
    form = PostForm()

    # Logic for POST request to save a post
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return HttpResponseRedirect(reverse('posts', kwargs={'pk': pk, 'topic_pk': topic_pk}))

    # Logic to update topic view count
    session_key = 'viewed_topic_{}'.format(topic.pk)
    if not request.session.get(session_key, False):
        topic.views += 1
        topic.save()
        request.session[session_key] = True

    context = {
        'topic': topic,
        'posts': posts,
        'form': form
    }

    return render(request, 'boardapp/posts.html', context)
'''

# reply_view VIEW FUNCTION IS NOT NEEDED, IT WAS FOR TEST.
'''   @login_required
def reply_view(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit= False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    
    context = {
        'topic':topic,
        'form':form,
    }
    return render(request, 'boardapp/reply.html', context)   '''
    