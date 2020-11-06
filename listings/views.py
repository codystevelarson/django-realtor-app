from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import state_choices, bedroom_choices, price_choices


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    # Pagination setup
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing,
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:  # check for empty string
            queryset_list = queryset_list.filter(
                description__icontains=keywords)  # __icontains = match on prop containing

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:  # check for empty string
            queryset_list = queryset_list.filter(
                city__iexact=city)  # __icontains = match on prop exactly (case insensitive) (use __exact for case sensitive)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:  # check for empty string
            queryset_list = queryset_list.filter(
                state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:  # check for empty string
            queryset_list = queryset_list.filter(
                bedrooms__gte=bedrooms)  # __gte = greater than or equal to

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:  # check for empty string
            queryset_list = queryset_list.filter(
                price__lte=price)  # __lte = less than or equal to

    context = {
        'listings': queryset_list,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'values': request.GET  # to sustain the form values
    }
    return render(request, 'listings/search.html', context)
