from django.shortcuts import render, get_object_or_404
from .models import Event, EventType 

def event_list(request):
    # 获取所有赛事类型，并为每个类型查询对应的赛事
    event_types = EventType.objects.all()
    grouped_events = {}
    for event_type in event_types:
        events = Event.objects.filter(event_type=event_type).order_by('-start_time')
        if events.exists():  # 只显示有赛事的类型
            grouped_events[event_type] = events

    context = {
        'grouped_events': grouped_events,  # 传分组数据到模板
    }
    return render(request, 'events/index.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/detail.html', {'event': event})

# 在原有两个视图下面添加
def event_bracket(request, pk):
    event = get_object_or_404(Event, pk=pk)
    quarterfinals = event.matches.filter(round='quarter').order_by('match_number')
    semifinals = event.matches.filter(round='semi').order_by('match_number')
    finals = event.matches.filter(round='final')
    
    context = {
        'event': event,
        'quarterfinals': quarterfinals,
        'semifinals': semifinals,
        'finals': finals,
    }
    return render(request, 'events/bracket.html', context)
