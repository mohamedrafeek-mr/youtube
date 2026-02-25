from django.shortcuts import render, redirect
from django.db.models import Q, Count
from videos.models import Video

SORT_OPTIONS = {
    'views': '-views',
    'latest': '-created_at',
    'likes': '-likes_count',
}

def search(request):
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "latest")
    page_number = request.GET.get("page", 1)

    if not query:
        return redirect('core:home')

    results = Video.objects.filter(
        Q(title__icontains=query)
        | Q(description__icontains=query)
        | Q(uploader__username__icontains=query)
        | Q(category__name__icontains=query)
    ).annotate(likes_count=Count('likes')).order_by(SORT_OPTIONS.get(sort, '-created_at'))

    # paginate results (10 per page)
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(results, 10)
    try:
        videos = paginator.page(page_number)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(
        request,
        "search/results.html",
        {"results": videos, "query": query, "sort": sort, "paginator": paginator},
    )
