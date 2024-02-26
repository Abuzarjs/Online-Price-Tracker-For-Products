# views.py

from django.shortcuts import render, HttpResponse, redirect
from .forms import PriceTrackerForm
from .utils import track_price
from .models import PriceTracker
from urllib3.exceptions import MaxRetryError  # Updated import

def track_price_view(request):
    if request.method == 'POST':
        form = PriceTrackerForm(request.POST)
        if form.is_valid():
            price_tracker = form.save()
            success_message = track_price_with_retry(price_tracker)
            if success_message:
                return redirect('tracker:price_tracker_list')
            else:
                # Handle the case when tracking fails
                # You can customize this part based on your needs
                return render(request, 'tracker/track_price.html', {'form': form, 'error_message': 'Failed to track the price. Please try again later.'})
    else:
        form = PriceTrackerForm()

    return render(request, 'tracker/track_price.html', {'form': form})

def track_price_with_retry(price_tracker, max_retries=3):
    url = price_tracker.url
    for _ in range(max_retries):
        try:
            track_price(price_tracker)
            return 'Price tracked successfully'
        except MaxRetryError:
            pass
        except Exception as e:
            # Log or handle other exceptions as needed
            print(f"Error tracking price: {e}")

    return None

def price_tracker_list_view(request):
    price_trackers = PriceTracker.objects.all()
    return render(request, 'tracker/price_tracker_list.html', {'price_trackers': price_trackers})

def home_view(request):
    return render(request, 'tracker/home.html')
